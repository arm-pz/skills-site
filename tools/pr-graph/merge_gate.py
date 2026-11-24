#!/usr/bin/env python3
"""The PR graph's merge gate: a pass-or-fail check, run as code, not by the model.

    python tools/pr-graph/merge_gate.py <pr> --review <review-report.json>          # dry run
    python tools/pr-graph/merge_gate.py <pr> --review <review-report.json> --merge  # squash-merge on pass

A PR passes only if ALL of these hold for its current head:
  1. The review report is for this PR, head SHA, base branch and base SHA, and has no CRITICAL or HIGH finding.
  2. Every commit-status context succeeded, every check run on the head has finished, none failed, and the `check` job succeeded.
  3. GitHub says the PR merges cleanly into its base.
  4. It has no `hold` or `needs-owner` label.
  5. Its diff touches no protected path (CI, agent and gate config). Those always go to a human.

A draft PR that passes everything else is marked ready, then merged (with --merge).
The merge pins `sha` to the reviewed head, so a push after the review makes GitHub refuse it.

Prints one JSON verdict. Exit 0 = pass (and merged, with --merge), 1 = fail, 2 = error.
Uses the GitHub REST API through `gh api` (GraphQL is not available in Claude Code sessions).
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = "arm-pz/skills-site"
REQUIRED_CHECK = "check"
BLOCKING_LABELS = {"hold", "needs-owner"}
BLOCKING_SEVERITIES = {"CRITICAL", "HIGH"}
OK_CONCLUSIONS = {"success", "skipped", "neutral"}
# The gate never auto-merges a change to the machinery that decides merges.
PROTECTED_PREFIXES = (".github/", ".claude/", "tools/pr-graph/")
PROTECTED_FILES = {"CLAUDE.md", "tools/agent-skills/tests/test_merge_gate.py"}
SHA = re.compile(r"^[0-9a-f]{40}$")


class GateError(Exception):
    pass


def check_review_shape(review):
    """Return a list of problems with a review report; empty means usable."""
    problems = []
    if not isinstance(review, dict):
        return ["review is not a JSON object"]
    for key in ("pr", "head_sha", "base_ref", "base_sha", "round", "verdict", "findings"):
        if key not in review:
            problems.append(f"review is missing `{key}`")
    if problems:
        return problems
    if not isinstance(review["pr"], int):
        problems.append("review `pr` is not an integer")
    if not isinstance(review["head_sha"], str) or not SHA.match(review["head_sha"]):
        problems.append("review `head_sha` is not a full 40-character SHA")
    if not isinstance(review["base_ref"], str) or not review["base_ref"]:
        problems.append("review `base_ref` must name a branch")
    if not isinstance(review["base_sha"], str) or not SHA.fullmatch(review["base_sha"]):
        problems.append("review `base_sha` is not a full 40-character SHA")
    if review["verdict"] not in ("pass", "fail"):
        problems.append("review `verdict` is not pass or fail")
    if not isinstance(review["findings"], list):
        problems.append("review `findings` is not a list")
    else:
        for i, f in enumerate(review["findings"]):
            if not isinstance(f, dict) or f.get("severity") not in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
                problems.append(f"finding {i} has no valid severity")
    return problems


def is_protected(path):
    return path in PROTECTED_FILES or path.startswith(PROTECTED_PREFIXES)


def evaluate(state, review):
    """Decide pass or fail from plain data, so it can be tested without GitHub.

    state: {"number", "head_sha", "base_ref", "base_sha", "draft", "mergeable",
            "labels", "files", "checks", "statuses"}
      mergeable: True, False or None (GitHub still computing)
      checks: [{"name", "status", "conclusion"}]
    Returns {"pass": bool, "reasons": [...], "draft": bool}.
    """
    reasons = list(check_review_shape(review))
    if not reasons:
        if review["pr"] != state["number"]:
            reasons.append(f"review is for PR #{review['pr']}, not #{state['number']}")
        if review["head_sha"] != state["head_sha"]:
            reasons.append(f"stale review: reviewed {review['head_sha'][:7]}, head is {state['head_sha'][:7]}")
        if review["base_ref"] != state["base_ref"] or review["base_sha"] != state["base_sha"]:
            reasons.append("stale review: base branch or commit changed")
        if review["verdict"] != "pass":
            reasons.append("review verdict is fail")
        blocking = [f["id"] if "id" in f else "?" for f in review["findings"]
                    if f["severity"] in BLOCKING_SEVERITIES]
        if blocking:
            reasons.append("blocking findings: " + ", ".join(blocking))
        if review["verdict"] == "pass" and blocking:
            reasons.append("review says pass but lists CRITICAL/HIGH findings")

    checks = state["checks"]
    if not any(c["name"] == REQUIRED_CHECK for c in checks):
        reasons.append(f"required check `{REQUIRED_CHECK}` has not run on the head")
    for c in checks:
        if c["status"] != "completed":
            reasons.append(f"check `{c['name']}` still {c['status']}")
        elif c["conclusion"] not in OK_CONCLUSIONS:
            reasons.append(f"check `{c['name']}` {c['conclusion']}")
        elif c["name"] == REQUIRED_CHECK and c["conclusion"] != "success":
            reasons.append(f"required check `{REQUIRED_CHECK}` was {c['conclusion']}, not success")

    for context, status in state["statuses"].items():
        if status != "success":
            reasons.append(f"commit status `{context}` is {status}")

    if state["mergeable"] is None:
        reasons.append("GitHub has not finished computing mergeability; retry")
    elif not state["mergeable"]:
        reasons.append("merge conflict with base")

    for label in sorted(BLOCKING_LABELS & set(state["labels"])):
        reasons.append(f"labelled `{label}`")

    protected = sorted(p for p in state["files"] if is_protected(p))
    if protected:
        reasons.append("touches protected paths (human merge only): " + ", ".join(protected))

    return {"pass": not reasons, "reasons": reasons, "draft": bool(state["draft"])}


def gh(*args, method="GET", fields=None):
    cmd = ["gh", "api", "-X", method, *args]
    for k, v in (fields or {}).items():
        cmd += ["-f", f"{k}={v}"]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        raise GateError(f"gh api {' '.join(args)} failed: {out.stderr.strip() or out.stdout.strip()}")
    return json.loads(out.stdout) if out.stdout.strip() else {}


def paged(path):
    items, page = [], 1
    while True:
        sep = "&" if "?" in path else "?"
        batch = gh(f"{path}{sep}per_page=100&page={page}")
        batch = batch.get("check_runs", batch) if isinstance(batch, dict) else batch
        items += batch
        if len(batch) < 100:
            return items
        page += 1


def fetch_state(number):
    pr = gh(f"repos/{REPO}/pulls/{number}")
    if pr.get("state") != "open":
        raise GateError(f"PR #{number} is {pr.get('state')}, not open")
    sha = pr["head"]["sha"]
    changed = paged(f"repos/{REPO}/pulls/{number}/files")
    # A renamed file counts at its old path too, so moving a protected file out is still protected.
    files = [f["filename"] for f in changed] + [f["previous_filename"] for f in changed
                                                if f.get("previous_filename")]
    runs = paged(f"repos/{REPO}/commits/{sha}/check-runs")
    # GitHub lists statuses newest first and treats context names case-insensitively.
    statuses = {}
    for status in paged(f"repos/{REPO}/commits/{sha}/statuses"):
        statuses.setdefault(status["context"].casefold(), status["state"])
    return {
        "number": number,
        "head_sha": sha,
        "base_ref": pr["base"]["ref"],
        "base_sha": pr["base"]["sha"],
        "draft": pr.get("draft", False),
        "mergeable": pr.get("mergeable"),
        "labels": [l["name"] for l in pr.get("labels", [])],
        "files": files,
        "statuses": statuses,
        "checks": [{"name": r["name"], "status": r["status"], "conclusion": r.get("conclusion")}
                   for r in runs],
    }


def merge(state):
    if state["draft"]:
        gh(f"repos/{REPO}/pulls/{state['number']}/ccr/ready_for_review", method="POST")
    return gh(f"repos/{REPO}/pulls/{state['number']}/merge", method="PUT",
              fields={"merge_method": "squash", "sha": state["head_sha"]})


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("pr", type=int)
    ap.add_argument("--review", required=True, type=Path, help="review-report.json for the current head")
    ap.add_argument("--merge", action="store_true", help="squash-merge when the gate passes")
    args = ap.parse_args(argv)
    try:
        review = json.loads(args.review.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(json.dumps({"pr": args.pr, "pass": False, "error": f"cannot read review: {e}"}))
        return 2
    try:
        state = fetch_state(args.pr)
        verdict = evaluate(state, review)
        verdict.update(pr=args.pr, head_sha=state["head_sha"], merged=False)
        if verdict["pass"] and args.merge:
            result = merge(state)
            verdict["merged"] = bool(result.get("merged"))
            verdict["merge_sha"] = result.get("sha")
    except GateError as e:
        print(json.dumps({"pr": args.pr, "pass": False, "error": str(e)}))
        return 2
    print(json.dumps(verdict, indent=2))
    return 0 if verdict["pass"] and (verdict["merged"] or not args.merge) else 1


if __name__ == "__main__":
    sys.exit(main())

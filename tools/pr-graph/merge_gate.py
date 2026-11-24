#!/usr/bin/env python3
"""The PR graph's merge gate: a pass-or-fail check, run as code, not by the model.

    python tools/pr-graph/merge_gate.py <pr> --review <review-report.json>          # dry run
    python tools/pr-graph/merge_gate.py <pr> --review <review-report.json> --merge  # squash-merge on pass

A PR passes only if ALL of these hold for its current head:
  1. The review report is for this PR, head SHA, base branch and base SHA, and has no CRITICAL or HIGH finding.
  2. Every commit-status context succeeded, every check run on the head has finished, none failed, and the configured required checks succeeded.
  3. GitHub says the PR merges cleanly into its base.
  4. It has no `hold`, `hands-off`, or `needs-owner` label.
  5. Its diff touches no protected path (CI, agent and gate config). Those always go to a human.
  6. GitHub listed every changed file, so check 5 saw the whole diff.

A draft PR that passes everything else is marked ready, then merged (with --merge).
The merge pins `sha` to the reviewed head, so a push after the review makes GitHub refuse it.

Prints one JSON verdict. Exit 0 = pass (and merged, with --merge), 1 = fail, 2 = error.
Uses the GitHub REST API through `gh api` (GraphQL is not available in Claude Code sessions).
"""
import argparse
import base64
import os
import json
import re
import subprocess
import sys
from pathlib import Path

REPOSITORY = re.compile(r"[A-Za-z0-9-]+/[A-Za-z0-9_.-]+")
BLOCKING_LABELS = {"hold", "hands-off", "needs-owner"}
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
    inconclusive = review.get("inconclusive", [])
    if not isinstance(inconclusive, list) or not all(
            isinstance(i, dict) and isinstance(i.get("id"), str) for i in inconclusive):
        problems.append("review `inconclusive` must be a list of objects with an `id`")
    return problems


def is_protected(path):
    return path in PROTECTED_FILES or path.startswith(PROTECTED_PREFIXES)


def evaluate(state, review, required_checks=("check",)):
    """Decide pass or fail from plain data, so it can be tested without GitHub.

    state: {"number", "head_sha", "base_ref", "base_sha", "draft", "mergeable",
            "labels", "files", "files_listed", "files_expected", "checks", "statuses"}
      files_listed / files_expected: how many changed files GitHub listed vs. says the PR has
      mergeable: True, False or None (GitHub still computing)
      checks: [{"name", "status", "conclusion"}]
    Returns {"pass": bool, "reasons": [...], "draft": bool, "inconclusive": [ids]}.
    Inconclusive IDs never affect "pass"; they are passed through for the run summary.
    """
    reasons = list(check_review_shape(review))
    if not reasons:
        if str(review.get("repository", "")).casefold() != state["repository"].casefold():
            reasons.append("review belongs to a different repository or lacks repository identity")
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
    for name in required_checks:
        if not any(c["name"] == name for c in checks) and name.casefold() not in state["statuses"]:
            reasons.append(f"required check `{name}` has not run on the head")
    for c in checks:
        if c["status"] != "completed":
            reasons.append(f"check `{c['name']}` still {c['status']}")
        elif c["conclusion"] not in OK_CONCLUSIONS:
            reasons.append(f"check `{c['name']}` {c['conclusion']}")
        elif c["name"] in required_checks and c["conclusion"] != "success":
            reasons.append(f"required check `{c['name']}` was {c['conclusion']}, not success")

    for context, status in state["statuses"].items():
        if status != "success":
            reasons.append(f"commit status `{context}` is {status}")

    if state["mergeable"] is None:
        reasons.append("GitHub has not finished computing mergeability; retry")
    elif not state["mergeable"]:
        reasons.append("merge conflict with base")

    for label in sorted(BLOCKING_LABELS & {label.casefold() for label in state["labels"]}):
        reasons.append(f"labelled `{label}`")

    # The protected-path check is only as good as the file list. GitHub's files API stops at
    # 3,000 files, so a list shorter than the PR's own count fails closed.
    if state["files_listed"] != state["files_expected"]:
        reasons.append(f"incomplete file list: GitHub listed {state['files_listed']} of "
                       f"{state['files_expected']} changed files")

    protected = sorted(p for p in state["files"] if is_protected(p))
    if protected:
        reasons.append("touches protected paths (human merge only): " + ", ".join(protected))

    # Inconclusive findings never block; they ride along so the summary can show them to a human.
    inconclusive = []
    if isinstance(review, dict) and isinstance(review.get("inconclusive"), list):
        inconclusive = [i["id"] for i in review["inconclusive"]
                        if isinstance(i, dict) and isinstance(i.get("id"), str)]
    return {"pass": not reasons, "reasons": reasons, "draft": bool(state["draft"]),
            "inconclusive": inconclusive}


def cli(*args):
    out = subprocess.run(["gh", *args], capture_output=True, encoding="utf-8")
    if out.returncode:
        raise GateError(out.stderr.strip() or "GitHub CLI failed")
    return out.stdout.strip()


def gh(*args, method="GET", fields=None):
    cmd = ["api", "-X", method, *args]
    for k, v in (fields or {}).items():
        cmd += ["-f", f"{k}={v}"]
    return json.loads(cli(*cmd) or "{}")


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


def required_checks(repo, base_sha):
    """Read policy from the target's reviewed base, even for a remote --repo."""
    root = gh(f"repos/{repo}/git/trees/{base_sha}")
    if root.get("truncated"):
        raise GateError("cannot inspect complete repository root")
    folder = next((item for item in root["tree"] if item["path"] == ".github"), None)
    if folder is None:
        return ["check"]
    entries = gh(f"repos/{repo}/git/trees/{folder['sha']}")
    if entries.get("truncated"):
        raise GateError("cannot inspect complete .github directory")
    config = next((item for item in entries["tree"] if item["path"] == "pr-graph.json"), None)
    if config is None:
        return ["check"]
    blob = gh(f"repos/{repo}/git/blobs/{config['sha']}")
    names = json.loads(base64.b64decode(blob["content"]))["required_checks"]
    if not isinstance(names, list) or not names or not all(isinstance(n, str) and n.strip() for n in names):
        raise GateError("required_checks must be a nonempty list of check names")
    return names


def fetch_state(number, repo):
    pr = gh(f"repos/{repo}/pulls/{number}")
    if pr.get("state") != "open":
        raise GateError(f"PR #{number} is {pr.get('state')}, not open")
    sha = pr["head"]["sha"]
    changed = paged(f"repos/{repo}/pulls/{number}/files")
    # A renamed file counts at its old path too, so moving a protected file out is still protected.
    files = [f["filename"] for f in changed] + [f["previous_filename"] for f in changed
                                                if f.get("previous_filename")]
    runs = paged(f"repos/{repo}/commits/{sha}/check-runs")
    # GitHub lists statuses newest first and treats context names case-insensitively.
    statuses = {}
    for status in paged(f"repos/{repo}/commits/{sha}/statuses"):
        statuses.setdefault(status["context"].casefold(), status["state"])
    return {
        "number": number,
        "repository": repo,
        "head_sha": sha,
        "base_ref": pr["base"]["ref"],
        "base_sha": pr["base"]["sha"],
        "draft": pr.get("draft", False),
        "mergeable": pr.get("mergeable"),
        "labels": [l["name"] for l in pr.get("labels", [])],
        "files": files,
        "files_listed": len(changed),
        "files_expected": pr.get("changed_files"),
        "statuses": statuses,
        "checks": [{"name": r["name"], "status": r["status"], "conclusion": r.get("conclusion")}
                   for r in runs],
    }


def merge(state):
    repo = state["repository"]
    if state["draft"]:
        cli("pr", "ready", str(state["number"]), "--repo", repo)
    return gh(f"repos/{repo}/pulls/{state['number']}/merge", method="PUT",
              fields={"merge_method": "squash", "sha": state["head_sha"]})


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("pr", type=int)
    ap.add_argument("--repo", help="GitHub OWNER/REPO (default: Actions caller or current checkout)")
    ap.add_argument("--review", required=True, type=Path, help="review-report.json for the current head")
    ap.add_argument("--merge", action="store_true", help="squash-merge when the gate passes")
    args = ap.parse_args(argv)
    try:
        review = json.loads(args.review.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(json.dumps({"pr": args.pr, "pass": False, "error": f"cannot read review: {e}"}))
        return 2
    try:
        repo = args.repo or os.environ.get("GITHUB_REPOSITORY") or cli(
            "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner")
        if not REPOSITORY.fullmatch(repo) or repo.split("/")[1] in {".", ".."}:
            raise GateError("invalid repository; expected OWNER/REPO")
        state = fetch_state(args.pr, repo)
        required = required_checks(repo, state["base_sha"])
        verdict = evaluate(state, review, required)
        verdict.update(pr=args.pr, head_sha=state["head_sha"], merged=False)
        if verdict["pass"] and args.merge:
            result = merge(state)
            verdict["merged"] = bool(result.get("merged"))
            verdict["merge_sha"] = result.get("sha")
    except (GateError, OSError, KeyError, TypeError, ValueError) as e:
        print(json.dumps({"pr": args.pr, "pass": False, "error": str(e)}))
        return 2
    print(json.dumps(verdict, indent=2))
    return 0 if verdict["pass"] and (verdict["merged"] or not args.merge) else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Turn real evidence into candidate eval cases (JSONL), for the user to confirm.

Usage:
  python intake.py sessions SESSIONS_DIR --skill NAME [--limit 40]
  python intake.py papercuts QUEUE.jsonl|ISSUES.json [--skill NAME]
  python intake.py prs PRS.json --agent LOGIN[,LOGIN] [--branch-prefix claude/]
  python intake.py show CANDIDATES.jsonl

sessions   Claude Code session files where the skill ran (a Skill call naming it, or the user typed
           /NAME). Each becomes a `real` case: the user's prompt, plus the trajectory it took, as draft
           trajectory checks to confirm or correct.
papercuts  log-papercut's queue file, or `gh issue list --label papercut --json number,title,body,url,state`.
           Matching reports are grouped by fingerprint; each group becomes a `regression` case.
prs        `gh pr list --state all --json number,title,url,state,mergedAt,author,headRefName,body,reviews,comments,commits`.
           Agent PRs that were closed unmerged (rejected) or merged after change requests or human
           commits (edited) become `author` cases carrying the reviewer's words.
show       A markdown table of candidates, to show the user before writing the suite.

Prompts, review text and errors are masked for secrets and emails. Output goes to stdout. Standard library only.
"""
import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location("traces", Path(__file__).resolve().parent / "traces.py")
traces = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(traces)
mask = traces.mask


def short(text, n=300):
    text = mask(" ".join(str(text or "").split()))
    return text if len(text) <= n else text[:n] + "…"


def emit(cases):
    for c in cases:
        print(json.dumps(c, ensure_ascii=False))
    print(f"{len(cases)} candidates", file=sys.stderr)
    return 0


# ---------- sessions ----------

def invoked(tr, skill):
    for c in tr.get("calls", []):
        if c["name"] == "Skill" and re.search(rf"\b{re.escape(skill)}\b", c.get("input") or ""):
            return True
    prompt = tr.get("prompt") or ""
    return bool(re.search(rf"(^|<command-name>)/{re.escape(skill)}\b", prompt.strip()))


def from_sessions(folder, skill, limit):
    files = sorted(Path(folder).rglob("*.jsonl"), key=lambda f: f.stat().st_mtime, reverse=True)
    cases = []
    for f in files:
        try:
            tr = traces.load(f, raw=True)
        except OSError:
            continue
        if tr.get("format") != "jsonl" or not invoked(tr, skill):
            continue
        tools = []
        for c in tr["calls"]:
            if c["name"] not in tools:
                tools.append(c["name"])
        sid = tr.get("session_id") or f.stem
        checks = [{"type": "skill_used", "value": skill}, {"type": "finished"},
                  {"type": "max_tool_errors", "value": max(1, tr["tool_errors"])}]
        if len(tools) >= 2:
            checks.append({"type": "order", "value": tools[:6], "draft": True})
        cases.append({
            "id": f"r-{hashlib.sha1(str(sid).encode()).hexdigest()[:8]}", "tier": "real",
            "kind": "positive", "source": f"session {sid} ({(tr.get('started') or '')[:10]})",
            "status": "candidate", "prompt": short(tr.get("prompt"), 2000),
            "observed": {"tools": tools, "calls": len(tr["calls"]), "tool_errors": tr["tool_errors"],
                         "end": tr["end"], "flags": tr["flags"]},
            "checks": checks,
            "notes": "trajectory copied from this run: confirm it was a good run before keeping the order check"})
        if len(cases) >= limit:
            break
    return cases


# ---------- papercuts ----------

def papercut_records(path):
    data = Path(path).read_text(encoding="utf-8-sig")
    try:
        parsed = json.loads(data)
    except json.JSONDecodeError:
        parsed = None
    if isinstance(parsed, list):  # gh issue list --json ...
        out = []
        for issue in parsed:
            m = re.search(r"```json\s*(\{.*?\})\s*```", issue.get("body") or "", re.S)
            if not m:
                continue
            try:
                rec = json.loads(m.group(1))
            except json.JSONDecodeError:
                continue
            rec["issue"] = issue.get("url") or issue.get("number")
            rec["issue_state"] = issue.get("state")
            out.append(rec)
        return out
    recs = []
    for line in data.splitlines():
        try:
            recs.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return recs


def from_papercuts(path, skill):
    groups = {}
    for r in papercut_records(path):
        if skill and r.get("skill") != skill:
            continue
        fp = r.get("fingerprint") or hashlib.sha1(
            f"{r.get('skill')}|{r.get('tool')}|{r.get('happened')}".encode()).hexdigest()[:12]
        g = groups.setdefault(fp, {"first": r, "count": 0, "issues": set()})
        g["count"] += int(r.get("count", 1))
        if r.get("issue"):
            g["issues"].add(str(r["issue"]))
    cases = []
    for fp, g in sorted(groups.items(), key=lambda kv: -kv[1]["count"]):
        r = g["first"]
        checks = [{"type": "finished"}]
        if r.get("tool"):
            checks.append({"type": "max_tool_errors", "value": 0, "draft": True})
        if r.get("error_pattern"):
            checks.append({"type": "no_error_matching", "value": r["error_pattern"]})
        cases.append({
            "id": f"p-{fp[:8]}", "tier": "golden" if r.get("reproducible") else "real",
            "kind": "regression", "source": f"papercut {fp} x{g['count']}"
            + (f" ({', '.join(sorted(g['issues']))})" if g["issues"] else ""),
            "status": "candidate", "skill": r.get("skill"), "tool": r.get("tool"),
            "tried": short(r.get("tried")), "expected": short(r.get("expected")),
            "happened": short(r.get("happened")), "fix": short(r.get("fix")),
            "checks": checks,
            "notes": "needs the prompt that hits this path; add it once the fix lands so the case guards it"})
    return cases


# ---------- PRs ----------

def login(x):
    return ((x or {}).get("login") or "").lower()


def from_prs(path, agents, prefix):
    prs = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    agents = {a.strip().lower() for a in agents.split(",") if a.strip()}
    cases = []
    for pr in prs:
        mine = login(pr.get("author")) in agents or (prefix and (pr.get("headRefName") or "").startswith(prefix))
        if not mine:
            continue
        merged = bool(pr.get("mergedAt"))
        reviews = pr.get("reviews") or []
        changes = [r for r in reviews if r.get("state") == "CHANGES_REQUESTED"]
        human_commits = []
        for c in pr.get("commits") or []:
            authors = {login(a) for a in c.get("authors") or []}
            if authors and not authors & agents:
                human_commits.append(c.get("messageHeadline") or c.get("oid", "")[:7])
        if not merged and (pr.get("state") or "").upper() == "CLOSED":
            signal = "rejected"
        elif merged and (changes or human_commits):
            signal = "edited"
        else:
            continue
        feedback = [short(r.get("body"), 400) for r in changes + reviews if r.get("body")]
        feedback += [short(c.get("body"), 400) for c in pr.get("comments") or []
                     if c.get("body") and login(c.get("author")) not in agents]
        feedback = list(dict.fromkeys(f for f in feedback if f))[:5]
        rubric = (f"Would the reviewer's objection still apply to this output? Objection: {feedback[0][:200]}"
                  if feedback else "Would the reviewer accept this change without edits?")
        cases.append({
            "id": f"pr-{pr.get('number')}", "tier": "author", "kind": "regression",
            "source": f"{signal} PR {pr.get('url') or pr.get('number')}", "status": "candidate",
            "human_signal": signal, "title": short(pr.get("title"), 120),
            "feedback": feedback, "human_commits": human_commits[:5],
            "checks": [{"type": "judge", "rubric": rubric}],
            "notes": "needs the task prompt that produced this PR (PR body, linked issue or session)"})
    return cases


# ---------- show ----------

def show(path):
    rows = [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]
    print("| id | tier | intent | kind | source | what must be true |")
    print("| --- | --- | --- | --- | --- | --- |")
    for c in rows:
        what = "; ".join(f"{ch['type']} {json.dumps(ch.get('value', ch.get('rubric', '')))[:50]}"
                         for ch in c.get("checks", []))
        print(f"| {c.get('id')} | {c.get('tier')} | {c.get('intent') or 'to set'} | {c.get('kind', '')} | {short(c.get('source'), 60)} | "
              f"{what.replace('|', '/')} |")
    by = {}
    for c in rows:
        by[c.get("tier")] = by.get(c.get("tier"), 0) + 1
    print(f"\n{len(rows)} candidates: " + ", ".join(f"{k} {v}" for k, v in sorted(by.items())))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sessions"); s.add_argument("folder"); s.add_argument("--skill", required=True)
    s.add_argument("--limit", type=int, default=40)
    p = sub.add_parser("papercuts"); p.add_argument("path"); p.add_argument("--skill")
    r = sub.add_parser("prs"); r.add_argument("path"); r.add_argument("--agent", default="")
    r.add_argument("--branch-prefix", default="")
    w = sub.add_parser("show"); w.add_argument("path")
    a = ap.parse_args(argv)

    target = getattr(a, "folder", None) or a.path
    if not Path(target).exists():
        print(f"error: {target} not found", file=sys.stderr)
        return 2
    if a.cmd == "sessions":
        return emit(from_sessions(a.folder, a.skill, a.limit))
    if a.cmd == "papercuts":
        return emit(from_papercuts(a.path, a.skill))
    if a.cmd == "prs":
        if not a.agent and not a.branch_prefix:
            print("error: say which PRs are the agent's: --agent LOGIN or --branch-prefix", file=sys.stderr)
            return 2
        return emit(from_prs(a.path, a.agent, a.branch_prefix))
    return show(a.path)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""File and look up papercuts: structured reports of friction an agent hit in a skill, tool or doc.

Usage:
  python papercut.py file --skill NAME --tool TOOL --tried T --expected E --happened H --fix F
                          [--workaround W] [--severity blocked|slowed|cosmetic] [--error-pattern REGEX]
                          [--skill-version V] [--agent A] [--session ID] [--reproducible] [--repo OWNER/REPO]
  python papercut.py list [--skill NAME] [--tool TOOL] [--search TEXT] [--repo OWNER/REPO]

Every report goes to the local queue: --queue, else $PAPERCUT_QUEUE, else ~/.papercuts/queue.jsonl.
A report with the same fingerprint (skill + tool + what happened, with numbers and paths normalised)
raises the existing entry's count instead of adding a line.

With --repo or $PAPERCUT_REPO it also files a GitHub issue labelled `papercut` through `gh`, or comments
on the open issue that already has this fingerprint. That is where a nightly pipeline picks them up:
  gh issue list --repo OWNER/REPO --label papercut --state open --json number,title,body,url,state

Text is masked for secrets and emails, home directories become ~, and each field is capped, so a
report carries no prompt text or file contents. Standard library only.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

FIELD_MAX = 500
SEVERITIES = ("blocked", "slowed", "cosmetic")
SECRET_RES = [
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"xox[abpr]-[A-Za-z0-9-]{10,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
    re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}"),
    re.compile(r"(?i)\b(bearer|token|api[_-]?key|password|secret)\b(\s*[:=]\s*|\s+)['\"]?[^\s'\"]{8,}"),
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
]
HOME_RE = re.compile(r"(/home/|/Users/|C:\\Users\\)[^/\\\s]+")


def clean(text):
    text = " ".join(str(text or "").split())
    for rx in SECRET_RES:
        text = rx.sub("[masked]", text)
    text = HOME_RE.sub("~", text)
    return text if len(text) <= FIELD_MAX else text[:FIELD_MAX] + "…"


def fingerprint(skill, tool, happened):
    norm = happened.lower()
    norm = re.sub(r"~?[/\\][^\s'\"]+", "<path>", norm)
    norm = re.sub(r"\b[0-9a-f]{7,}\b", "<id>", norm)
    norm = re.sub(r"\d+", "#", norm)
    norm = re.sub(r"[^a-z#<>]+", " ", norm).strip()
    return hashlib.sha1(f"{skill}|{tool}|{norm}".encode()).hexdigest()[:12]


def queue_path(arg):
    return Path(arg or os.environ.get("PAPERCUT_QUEUE") or Path.home() / ".papercuts" / "queue.jsonl")


def read_queue(path):
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def gh(*args):
    p = subprocess.run(["gh", *args], capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def issue_body(rec):
    return "\n".join([
        f"**Skill:** {rec['skill']} {rec.get('skill_version') or ''}  ",
        f"**Tool:** {rec['tool']} · **Severity:** {rec['severity']} · **Agent:** {rec.get('agent') or 'unknown'}",
        "", f"**Tried:** {rec['tried']}", "", f"**Expected:** {rec['expected']}", "",
        f"**Happened:** {rec['happened']}", "", f"**Fix:** {rec['fix']}", "",
        f"**Workaround:** {rec.get('workaround') or 'none found'}", "",
        "```json", json.dumps(rec, indent=2, ensure_ascii=False), "```", "",
        f"<!-- papercut:{rec['fingerprint']} -->"])


def file_issue(repo, rec):
    code, out, err = gh("issue", "list", "--repo", repo, "--label", "papercut", "--state", "open",
                        "--search", f"{rec['fingerprint']} in:body", "--json", "number,url")
    if code != 0:
        return f"issue not filed: gh issue list failed ({err[:120]})"
    existing = json.loads(out or "[]")
    if existing:
        n = str(existing[0]["number"])
        code, _, err = gh("issue", "comment", n, "--repo", repo, "--body",
                          f"Seen again {rec['last_seen']} by {rec.get('agent') or 'an agent'}"
                          + (f" (session {rec['session']})" if rec.get("session") else "")
                          + (f". Workaround used: {rec['workaround']}" if rec.get("workaround") else "."))
        return f"commented on {existing[0]['url']}" if code == 0 else f"comment failed ({err[:120]})"
    title = f"[papercut] {rec['skill']}: {rec['happened'][:70]}"
    args = ["issue", "create", "--repo", repo, "--title", title, "--body", issue_body(rec), "--label", "papercut"]
    code, out, err = gh(*args)
    if code != 0 and "label" in err.lower():
        gh("label", "create", "papercut", "--repo", repo, "--color", "d4a72c",
           "--description", "Friction an agent reported while running a skill")
        code, out, err = gh(*args)
    return f"filed {out}" if code == 0 else f"issue not filed ({err[:120]})"


def cmd_file(a):
    if a.severity not in SEVERITIES:
        print(f"error: --severity must be one of {', '.join(SEVERITIES)}", file=sys.stderr)
        return 2
    if a.error_pattern:
        try:
            re.compile(a.error_pattern)
        except re.error as e:
            print(f"error: --error-pattern is not a regex ({e})", file=sys.stderr)
            return 2
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rec = {k: clean(getattr(a, k)) for k in ("skill", "tool", "tried", "expected", "happened", "fix", "workaround")}
    if not all(rec[k] for k in ("skill", "tool", "tried", "expected", "happened", "fix")):
        print("error: skill, tool, tried, expected, happened and fix are all required", file=sys.stderr)
        return 2
    if re.fullmatch(r"(?i)(just )?(try( it)? again|retry|re-?run)\.?", rec["fix"]):
        print("error: 'try again' is not a fix; say what should change in the skill, tool or doc", file=sys.stderr)
        return 2
    rec["workaround"] = rec["workaround"] or None
    rec.update({"severity": a.severity, "skill_version": clean(a.skill_version), "agent": clean(a.agent),
                "session": clean(a.session), "error_pattern": a.error_pattern or None,
                "reproducible": bool(a.reproducible),
                "fingerprint": fingerprint(rec["skill"], rec["tool"], rec["happened"]),
                "first_seen": now, "last_seen": now, "count": 1})
    path = queue_path(a.queue)
    path.parent.mkdir(parents=True, exist_ok=True)
    entries = read_queue(path)
    hit = next((e for e in entries if e.get("fingerprint") == rec["fingerprint"]), None)
    if hit:
        hit["count"] = int(hit.get("count", 1)) + 1
        hit["last_seen"] = now
        if rec["workaround"] and not hit.get("workaround"):
            hit["workaround"] = rec["workaround"]
        rec = {**hit, "agent": rec["agent"], "session": rec["session"], "workaround": hit.get("workaround")}
    else:
        entries.append(rec)
    path.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in entries), encoding="utf-8")
    print(f"papercut {rec['fingerprint']} {'seen again' if hit else 'filed'} (count {rec['count']}) in {path}")
    repo = a.repo or os.environ.get("PAPERCUT_REPO")
    if repo:
        print(file_issue(repo, rec))
    return 0


def cmd_list(a):
    rows = read_queue(queue_path(a.queue))
    repo = a.repo or os.environ.get("PAPERCUT_REPO")
    if repo:
        code, out, err = gh("issue", "list", "--repo", repo, "--label", "papercut", "--state", "all",
                            "--limit", "200", "--json", "number,body,url,state")
        if code == 0:
            seen = {r.get("fingerprint") for r in rows}
            for issue in json.loads(out or "[]"):
                m = re.search(r"```json\s*(\{.*?\})\s*```", issue.get("body") or "", re.S)
                if m:
                    try:
                        rec = json.loads(m.group(1))
                    except json.JSONDecodeError:
                        continue
                    if rec.get("fingerprint") not in seen:
                        rows.append({**rec, "issue": issue.get("url"), "issue_state": issue.get("state")})
        else:
            print(f"note: GitHub not read ({err[:120]}); local queue only", file=sys.stderr)
    s = (a.search or "").lower()
    hits = [r for r in rows
            if (not a.skill or r.get("skill") == a.skill) and (not a.tool or r.get("tool") == a.tool)
            and (not s or s in json.dumps(r).lower())]
    for r in sorted(hits, key=lambda r: -int(r.get("count", 1))):
        print(json.dumps({k: r.get(k) for k in ("fingerprint", "count", "skill", "tool", "happened",
                                                 "fix", "workaround", "issue", "issue_state")},
                         ensure_ascii=False))
    print(f"{len(hits)} matching papercuts", file=sys.stderr)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("file")
    for k in ("skill", "tool", "tried", "expected", "happened", "fix"):
        f.add_argument(f"--{k}", required=True)
    for k in ("workaround", "skill-version", "agent", "session", "error-pattern", "repo", "queue"):
        f.add_argument(f"--{k}")
    f.add_argument("--severity", default="slowed")
    f.add_argument("--reproducible", action="store_true")
    l = sub.add_parser("list")
    for k in ("skill", "tool", "search", "repo", "queue"):
        l.add_argument(f"--{k}")
    a = ap.parse_args(argv)
    return cmd_file(a) if a.cmd == "file" else cmd_list(a)


if __name__ == "__main__":
    sys.exit(main())

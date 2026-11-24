#!/usr/bin/env python3
"""Condense one agent run's trace into what a failure diagnosis needs.

Usage:
  python traces.py PATH [--max-text 600]

PATH is a Claude Code session file (~/.claude/projects/<project>/<id>.jsonl), the output of
`claude -p --output-format stream-json`, a folder of either (the newest file is read), or any
other log (error-looking lines are listed). Prints JSON. Secrets are masked. Standard library only.
"""
import argparse
import json
import re
import sys
from pathlib import Path

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
DENIAL_RE = re.compile(r"(?i)permission (was )?denied|not allowed|requires approval|was blocked|"
                       r"user (rejected|declined)|denied by")
ERROR_LINE_RE = re.compile(r"(?i)\b(error|exception|traceback|failed|failure|denied|timed? ?out|"
                           r"fatal|panic|refused|401|403|429|5\d\d)\b")


def mask(text):
    for rx in SECRET_RES:
        text = rx.sub("[masked]", text)
    return text


def clip(text, n):
    text = mask(text if isinstance(text, str) else json.dumps(text, ensure_ascii=False))
    return text if len(text) <= n else text[:n] + f"… [+{len(text) - n} chars]"


def content_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for c in content:
            if isinstance(c, dict):
                if c.get("type") == "text":
                    parts.append(c.get("text", ""))
                elif c.get("type") == "tool_result":
                    parts.append(content_text(c.get("content")))
            elif isinstance(c, str):
                parts.append(c)
        return "\n".join(p for p in parts if p)
    return ""


def pick_file(path):
    p = Path(path)
    if p.is_dir():
        files = sorted((f for f in p.iterdir() if f.is_file() and f.suffix in (".jsonl", ".json", ".log", ".txt")),
                       key=lambda f: f.stat().st_mtime)
        if not files:
            return None
        return files[-1]
    return p if p.is_file() else None


def parse_jsonl(lines, max_text):
    calls, by_id = [], {}
    first_prompt, final_text, end, meta = None, None, None, {}
    started = ended = None
    for raw in lines:
        try:
            ev = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(ev, dict):
            continue
        ts = ev.get("timestamp")
        if ts:
            started = started or ts
            ended = ts
        meta.setdefault("session_id", ev.get("sessionId") or ev.get("session_id"))
        etype = ev.get("type")
        if etype == "result":
            end = ev.get("subtype") or ("error" if ev.get("is_error") else "success")
            if ev.get("result"):
                final_text = ev["result"]
            for k in ("num_turns", "total_cost_usd", "duration_ms"):
                if k in ev:
                    meta[k] = ev[k]
            continue
        if etype == "system" and ev.get("subtype") == "init":
            meta["model"] = ev.get("model")
            continue
        msg = ev.get("message")
        if not isinstance(msg, dict):
            continue
        content = msg.get("content")
        if etype == "user" or msg.get("role") == "user":
            items = content if isinstance(content, list) else []
            results = [c for c in items if isinstance(c, dict) and c.get("type") == "tool_result"]
            for r in results:
                call = by_id.get(r.get("tool_use_id"))
                text = content_text(r.get("content"))
                err = bool(r.get("is_error"))
                if call is not None:
                    call["error"] = err
                    call["result"] = clip(text, 200)
                    call["denied"] = bool(err and DENIAL_RE.search(text))
            if not results and first_prompt is None:
                t = content_text(content)
                if t.strip():
                    first_prompt = clip(t, max_text)
        elif etype == "assistant" or msg.get("role") == "assistant":
            meta.setdefault("model", msg.get("model"))
            items = content if isinstance(content, list) else [{"type": "text", "text": content or ""}]
            for c in items:
                if not isinstance(c, dict):
                    continue
                if c.get("type") == "tool_use":
                    call = {"n": len(calls) + 1, "name": c.get("name"),
                            "input": clip(c.get("input"), 160), "error": False, "denied": False}
                    calls.append(call)
                    by_id[c.get("id")] = call
                elif c.get("type") == "text" and c.get("text", "").strip():
                    final_text = c["text"]
    errors = [c for c in calls if c["error"]]
    if end is None:
        end = "unknown" if calls or final_text else "empty"
    flags = []
    if not final_text:
        flags.append("no_final_text")
    if errors:
        flags.append("tool_errors")
    if any(c["denied"] for c in calls):
        flags.append("permission_denials")
    if end not in ("success", "unknown"):
        flags.append(f"ended_{end}")
    tool_counts = {}
    for c in calls:
        tool_counts[c["name"]] = tool_counts.get(c["name"], 0) + 1
    return {"format": "jsonl", **{k: v for k, v in meta.items() if v is not None},
            "started": started, "ended": ended, "end": end, "flags": flags,
            "prompt": first_prompt, "tool_counts": tool_counts,
            "tool_errors": len(errors), "permission_denials": sum(c["denied"] for c in calls),
            "calls": calls, "final_text": clip(final_text, max_text) if final_text else None}


def parse_plain(lines, max_text):
    hits = [{"line": i, "text": clip(l.strip(), 200)}
            for i, l in enumerate(lines, 1) if ERROR_LINE_RE.search(l)]
    tail = "\n".join(l for l in lines[-5:] if l.strip())
    return {"format": "plain", "lines": len(lines), "error_lines": hits[:50],
            "error_line_count": len(hits), "flags": ["error_lines"] if hits else [],
            "tail": clip(tail, max_text)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("path")
    ap.add_argument("--max-text", type=int, default=600)
    a = ap.parse_args(argv)
    f = pick_file(a.path)
    if f is None:
        print(json.dumps({"error": f"no trace found at {a.path}"}))
        return 2
    lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
    parsed = sum(1 for l in lines[:50] if l.strip().startswith("{"))
    nonblank = sum(1 for l in lines[:50] if l.strip())
    out = parse_jsonl(lines, a.max_text) if nonblank and parsed / nonblank > 0.8 else parse_plain(lines, a.max_text)
    out["file"] = str(f)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

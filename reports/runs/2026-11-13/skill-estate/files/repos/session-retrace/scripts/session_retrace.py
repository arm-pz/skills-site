#!/usr/bin/env python3
"""Search and print conversation transcripts from local AI coding agents.

Supported providers and default roots:
  qoder   $QODER_CONFIG_DIR/projects or ~/.qoder/projects   <slug>/<id>.jsonl
  claude  $CLAUDE_CONFIG_DIR/projects or ~/.claude/projects  <slug>/<id>.jsonl
  codex   $CODEX_HOME or ~/.codex                            sessions/**/rollout-*.jsonl + history.jsonl
  gemini  ~/.gemini/tmp                                      */chats/session-*.jsonl

Usage:
  python session_retrace.py search "terms..." [--provider qoder,claude]
        [--workspace SUB] [--since YYYY-MM-DD] [--limit N] [--exclude provider:id]
        [--keep-live] [--root PATH] [--json]
  python session_retrace.py show [provider:]SESSION [--provider ...] [--turns N]
        [--max-chars N] [--raw] [--root PATH] [--json]

Read-only. Encrypted state files (Qoder/Claude `state.json`) are never opened.
Credential-shaped strings are redacted from snippets and output unless `--raw`.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PROVIDERS = ("qoder", "claude", "codex", "gemini")
LIVE_WINDOW_SECONDS = 600
RECENT_WINDOW_SECONDS = 300
INJECTED_PREFIXES = (
    "<environment_context",
    "<skills_instructions",
    "<session_context",
    "<user_instructions",
    "<permissions",
    "<turn_aborted",
    "<command-message",
)
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "did", "do", "for",
    "from", "had", "has", "have", "i", "in", "is", "it", "me", "my", "of", "on",
    "or", "our", "so", "that", "the", "their", "then", "there", "this", "to",
    "was", "we", "were", "what", "when", "where", "which", "who", "why", "with",
    "you", "your", "session", "sessions", "chat", "chats", "conversation",
    "conversations", "talk", "talked", "discussed", "find", "look", "search",
}
SECRET_PATTERNS = (
    re.compile(r"(?i)\b(bearer)\s+[A-Za-z0-9._~+/=-]{12,}"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"(?i)\b(api[_-]?key|access[_-]?token|client[_-]?secret|password)\b(\s*[\"']?\s*[:=]\s*)[\"']?[A-Za-z0-9._~+/=-]{12,}[\"']?"),
)
SECRET_REPLACEMENT = "[redacted]"


def provider_root(name: str, override: str | None = None) -> Path:
    if override:
        return Path(override).expanduser()
    home = Path.home()
    if name == "qoder":
        config = os.environ.get("QODER_CONFIG_DIR")
        return (Path(config) if config else home / ".qoder") / "projects"
    if name == "claude":
        config = os.environ.get("CLAUDE_CONFIG_DIR")
        return (Path(config) if config else home / ".claude") / "projects"
    if name == "codex":
        config = os.environ.get("CODEX_HOME")
        return Path(config) if config else home / ".codex"
    return home / ".gemini" / "tmp"


def iter_paths(provider: str, root: Path):
    if not root.is_dir():
        return
    if provider in ("qoder", "claude"):
        yield from sorted(root.glob("*/*.jsonl"))
    elif provider == "codex":
        yield from sorted(root.glob("sessions/**/rollout-*.jsonl"))
    elif provider == "gemini":
        yield from sorted(root.glob("*/chats/*.jsonl"))


def iter_events(path: Path):
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue
    except OSError:
        return


def content_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                text = block.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(parts)
    return ""


def is_injected(text: str) -> bool:
    return text.lstrip().lower().startswith(INJECTED_PREFIXES)


def redact(text: str) -> str:
    """Blank out credential-shaped strings before they reach a chat or a log."""
    for pattern in SECRET_PATTERNS:
        if pattern.groups == 1:
            text = pattern.sub(lambda m: m.group(1) + " " + SECRET_REPLACEMENT, text)
        elif pattern.groups >= 2:
            text = pattern.sub(lambda m: m.group(1) + m.group(2) + SECRET_REPLACEMENT, text)
        else:
            text = pattern.sub(SECRET_REPLACEMENT, text)
    return text


def parse_iso(value) -> float:
    if not isinstance(value, str) or not value:
        return 0.0
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        try:
            return datetime.strptime(value[:10], "%Y-%m-%d").timestamp()
        except ValueError:
            return 0.0


def new_session(provider: str, session_id: str, path: Path) -> dict:
    return {
        "provider": provider,
        "session_id": session_id,
        "workspace": "",
        "title": "",
        "last_ts": "",
        "messages": [],
        "path": str(path),
    }


def add_message(session: dict, role: str, timestamp: str, text: str):
    text = " ".join(text.split())
    if not text:
        return
    for old_role, _, old_text in session["messages"]:
        if old_role == role and old_text == text:
            return
    session["messages"].append((role, timestamp or "", text))
    if timestamp and timestamp > session["last_ts"]:
        session["last_ts"] = timestamp


def parse_claude_family(path: Path, provider: str) -> dict | None:
    """Qoder and Claude Code share this event schema."""
    data = new_session(provider, path.stem, path)
    for event in iter_events(path):
        kind = event.get("type")
        if kind in ("user", "assistant"):
            timestamp = event.get("timestamp") or ""
            if isinstance(timestamp, str) and timestamp > data["last_ts"]:
                data["last_ts"] = timestamp
            text = content_text(event.get("message", {}).get("content"))
            if text.strip():
                add_message(data, kind, timestamp, text)
        elif kind == "last-prompt":
            prompt = event.get("lastPrompt")
            if isinstance(prompt, str) and prompt.strip():
                data["title"] = prompt.strip().splitlines()[0]
        elif kind == "workspace-directories":
            dirs = event.get("directories")
            if isinstance(dirs, list) and dirs and not data["workspace"]:
                data["workspace"] = str(dirs[0])
        cwd = event.get("cwd")
        if isinstance(cwd, str) and cwd and not data["workspace"]:
            data["workspace"] = cwd
    if not data["messages"]:
        return None
    if not data["title"]:
        user_texts = [text for role, _, text in data["messages"] if role == "user"]
        if user_texts:
            data["title"] = user_texts[0][:120]
    return data


def parse_codex_rollout(path: Path, provider: str) -> dict | None:
    data = new_session(provider, path.stem, path)
    meta = {}
    for event in iter_events(path):
        kind = event.get("type")
        payload = event.get("payload")
        timestamp = event.get("timestamp") or ""
        if not isinstance(payload, dict):
            continue
        if kind == "session_meta":
            meta = payload
            data["session_id"] = str(payload.get("session_id") or data["session_id"])
            data["workspace"] = str(payload.get("cwd") or "")
            continue
        role = None
        text = ""
        if kind == "response_item" and payload.get("type") == "message":
            role = payload.get("role")
            text = content_text(payload.get("content"))
        elif kind == "event_msg" and payload.get("type") == "item_completed":
            item = payload.get("item") or {}
            item_type = item.get("type")
            if item_type == "UserMessage":
                role = "user"
            elif item_type in ("AgentMessage", "AssistantMessage"):
                role = "assistant"
            text = content_text(item.get("content")) or content_text(item.get("text"))
        if role not in ("user", "assistant"):
            continue
        if not text or is_injected(text):
            continue
        if isinstance(timestamp, str) and timestamp > data["last_ts"]:
            data["last_ts"] = timestamp
        add_message(data, role, timestamp, text)
    if not data["messages"]:
        return None
    user_texts = [text for role, _, text in data["messages"] if role == "user"]
    if user_texts:
        data["title"] = user_texts[-1][:120]
    return data


def parse_codex_history(path: Path) -> dict:
    """history.jsonl holds user prompts only; group them into sessions."""
    sessions = {}
    if not path.is_file():
        return sessions
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                session_id = entry.get("session_id")
                text = entry.get("text")
                if not isinstance(session_id, str) or not isinstance(text, str):
                    continue
                if is_injected(text):
                    continue
                ts = entry.get("ts")
                try:
                    timestamp = datetime.fromtimestamp(float(ts), tz=timezone.utc).isoformat().replace("+00:00", "Z")
                except (TypeError, ValueError, OSError):
                    timestamp = ""
                data = sessions.get(session_id)
                if data is None:
                    data = new_session("codex", session_id, path)
                    sessions[session_id] = data
                add_message(data, "user", timestamp, text)
                data["title"] = " ".join(text.split())[:120]
    except OSError:
        return sessions
    return sessions


def parse_gemini(path: Path, provider: str) -> dict | None:
    data = new_session(provider, path.stem, path)
    data["workspace"] = path.parent.parent.name
    messages = None
    start = ""
    for event in iter_events(path):
        if "$set" in event and isinstance(event["$set"], dict):
            snapshot = event["$set"].get("messages")
            if isinstance(snapshot, list):
                messages = snapshot
        elif "startTime" in event and not start:
            start = str(event.get("startTime") or "")
    for message in messages or []:
        kind = message.get("type")
        role = "user" if kind == "user" else "assistant" if kind in ("gemini", "model") else None
        text = content_text(message.get("content")) or content_text(message.get("text"))
        if not role or not text or is_injected(text):
            continue
        add_message(data, role, message.get("timestamp") or start, text)
    if not data["messages"]:
        return None
    user_texts = [text for role, _, text in data["messages"] if role == "user"]
    if user_texts:
        data["title"] = user_texts[-1][:120]
    return data


PARSERS = {
    "qoder": parse_claude_family,
    "claude": parse_claude_family,
    "codex": parse_codex_rollout,
    "gemini": parse_gemini,
}


def load_provider(provider: str, root: Path) -> dict:
    """Parse one agent's transcripts, keyed by session ID. Codex history is merged in."""
    sessions = {}
    for path in iter_paths(provider, root):
        try:
            data = PARSERS[provider](path, provider)
        except Exception:
            continue
        if data:
            sessions[data["session_id"]] = data
    if provider == "codex":
        for session_id, data in parse_codex_history(root / "history.jsonl").items():
            existing = sessions.get(session_id)
            if existing is None:
                sessions[session_id] = data
                continue
            for role, timestamp, text in data["messages"]:
                add_message(existing, role, timestamp, text)
            if not existing["workspace"]:
                existing["workspace"] = data["workspace"]
    return sessions


def load_sessions(providers, root_override: str | None = None) -> dict:
    sessions = {}
    for provider in providers:
        root = provider_root(provider, root_override if len(providers) == 1 else None)
        for session_id, data in load_provider(provider, root).items():
            sessions[(provider, session_id)] = data
    return sessions


def parse_terms(query: str):
    raw = re.findall(r'"[^"]+"|\S+', query)
    terms = []
    for piece in raw:
        piece = piece.strip("\"'").lower()
        piece = re.sub(r"^[^\w]+|[^\w]+$", "", piece)
        if piece and piece not in STOPWORDS:
            terms.append(piece)
    if not terms:
        terms = [query.lower()]
    return terms


def count_occurrences(haystack: str, needle: str) -> int:
    total = 0
    start = 0
    while True:
        index = haystack.find(needle, start)
        if index < 0:
            return total
        total += 1
        start = index + len(needle)


def make_snippet(text: str, terms, limit: int = 150) -> str:
    low = text.lower()
    best_index = -1
    for term in terms:
        index = low.find(term)
        if index >= 0 and (best_index < 0 or index < best_index):
            best_index = index
    if best_index < 0:
        best_index = 0
    start = max(0, best_index - 60)
    snippet = " ".join(text[start:start + limit].split())
    if start > 0:
        snippet = "…" + snippet
    if start + limit < len(text):
        snippet += "…"
    return snippet


def score_messages(messages, terms, query_lower):
    user_score = 0
    assistant_score = 0
    best = None
    for role, _, text in messages:
        low = text.lower()
        distinct = 0
        total = 0
        for term in terms:
            hits = count_occurrences(low, term)
            if hits:
                distinct += 1
                total += min(hits, 3)
        if not total:
            continue
        weight = 3 if role == "user" else 1
        if role == "user":
            user_score += total * weight
        else:
            assistant_score += total * weight
        snippet = make_snippet(text, terms)
        candidate = (distinct, total, 0 if role == "user" else 1, snippet)
        if best is None or candidate > best:
            best = candidate
    phrase = query_lower.strip()
    if phrase and len(terms) > 1:
        for role, _, text in messages:
            if role == "user" and phrase in text.lower():
                user_score += 15
                break
    return user_score, assistant_score, best


def is_live(session: dict, terms, now: float) -> bool:
    when = parse_iso(session["last_ts"])
    if not when and session["path"]:
        try:
            when = Path(session["path"]).stat().st_mtime
        except OSError:
            when = 0.0
    if not when or now - when > LIVE_WINDOW_SECONDS:
        return False
    needed = max(1, (len(terms) * 3 + 4) // 5)
    user_texts = [text for role, _, text in session["messages"] if role == "user"][-3:]
    for text in user_texts:
        low = text.lower()
        if sum(1 for term in terms if term in low) >= needed:
            return True
    return False


def is_recent(session: dict, now: float) -> bool:
    when = parse_iso(session["last_ts"])
    if not when and session["path"]:
        try:
            when = Path(session["path"]).stat().st_mtime
        except OSError:
            return False
    return bool(when) and now - when <= RECENT_WINDOW_SECONDS


def fmt_date(ts: str) -> str:
    if not ts:
        return "unknown"
    return ts[:16].replace("T", " ")


def session_label(session: dict, short: bool = True) -> str:
    ident = session["session_id"][:8] if short else session["session_id"]
    return f"{session['provider']}:{ident}"


def select_providers(args) -> list:
    if not args.provider:
        return list(PROVIDERS)
    wanted = [p.strip().lower() for p in args.provider.split(",") if p.strip()]
    unknown = [p for p in wanted if p not in PROVIDERS]
    if unknown:
        raise SystemExit(f"Unknown provider(s): {', '.join(unknown)}. Choose from {', '.join(PROVIDERS)}.")
    return wanted


def cmd_search(args) -> int:
    providers = select_providers(args)
    terms = parse_terms(args.query)
    query_lower = " ".join(args.query.lower().split())
    since = args.since or ""
    now = time.time()
    sessions = load_sessions(providers, args.root)
    scanned = 0
    skipped_live = 0
    results = []
    for session in sessions.values():
        if args.workspace and args.workspace.lower() not in (session["workspace"] + " " + session["session_id"] + " " + session["path"]).lower():
            continue
        if since and session["last_ts"] and session["last_ts"][:10] < since:
            continue
        raw = " ".join(text for _, _, text in session["messages"]).lower()
        if not all(term in raw for term in terms):
            continue
        scanned += 1
        if args.exclude:
            wanted = args.exclude.split(":", 1)
            if len(wanted) == 2:
                if session["provider"] == wanted[0] and session["session_id"] == wanted[1]:
                    continue
            elif session["session_id"] == args.exclude:
                continue
        user_score, assistant_score, best = score_messages(session["messages"], terms, query_lower)
        if not best or user_score + assistant_score == 0:
            continue
        if not args.keep_live and is_live(session, terms, now):
            skipped_live += 1
            continue
        results.append({
            "provider": session["provider"],
            "session_id": session["session_id"],
            "label": session_label(session),
            "workspace": session["workspace"],
            "last_activity": session["last_ts"],
            "date": fmt_date(session["last_ts"]) + (" (live?)" if is_recent(session, now) else ""),
            "live_suspect": is_recent(session, now),
            "title": redact(session["title"]),
            "score": user_score + assistant_score,
            "user_score": user_score,
            "evidence": redact(best[3]),
            "evidence_role": "user" if best[2] == 0 else "assistant",
            "turns": sum(1 for role, _, _ in session["messages"] if role == "user"),
            "path": session["path"],
        })
    results.sort(key=lambda r: (r["score"], r["last_activity"]), reverse=True)
    results = results[: args.limit]
    if args.json:
        print(json.dumps({
            "query": args.query,
            "terms": terms,
            "providers": providers,
            "scanned": scanned,
            "skipped_live": skipped_live,
            "results": results,
        }, ensure_ascii=False, indent=2))
        return 0
    print(f'Query: {args.query}  (terms: {", ".join(terms)})')
    print(f"Searched {scanned} matching sessions across {', '.join(providers)}; skipped {skipped_live} live.")
    print()
    if not results:
        print("No matches. Try fewer terms, synonyms, --provider, or --keep-live.")
        return 0
    print("| # | Date | Agent | Workspace | Session | Score | Evidence |")
    print("|---|------|-------|-----------|---------|-------|----------|")
    for index, row in enumerate(results, 1):
        evidence = row["evidence"].replace("|", "\\|")
        workspace = row["workspace"] or "unknown"
        print(
            f"| {index} | {row['date']} | {row['provider']} | {workspace} | "
            f"{row['label']} | {row['score']} | "
            f"{row['evidence_role']}: {evidence} |"
        )
    top = results[0]
    print()
    print(f"Top pick: {top['label']} — {top['workspace'] or 'workspace unknown'}")
    if top["title"]:
        print(f"Last prompt: {top['title'][:160]}")
    return 0


def cmd_show(args) -> int:
    target = args.session
    provider_filter = args.provider
    if ":" in target and target.split(":", 1)[0].lower() in PROVIDERS:
        provider_filter, target = target.split(":", 1)
    if not re.fullmatch(r"[A-Za-z0-9._-]{4,128}", target):
        print("Session ID must be 4-128 letters, digits, dots, underscores, or hyphens.")
        return 2
    providers = [provider_filter.lower()] if provider_filter else list(PROVIDERS)
    unknown = [p for p in providers if p not in PROVIDERS]
    if unknown:
        print(f"Unknown provider(s): {', '.join(unknown)}")
        return 2
    matches = []
    for provider in providers:
        root = provider_root(provider, args.root if len(providers) == 1 else None)
        for session_id, data in load_provider(provider, root).items():
            if target in session_id:
                matches.append(data)
    if not matches:
        print(f"No transcript matching {target}.")
        return 2
    if len(matches) > 1:
        names = ", ".join(session_label(m, False) for m in matches[:5])
        print(f"Ambiguous prefix {target}; matches: {names}")
        return 2
    data = matches[0]
    clean = (lambda text: text) if args.raw else redact
    messages = data["messages"]
    user_indexes = [i for i, (role, _, _) in enumerate(messages) if role == "user"]
    start = user_indexes[-args.turns] if len(user_indexes) > args.turns else 0
    window = messages[start:]
    if args.json:
        print(json.dumps({
            "provider": data["provider"],
            "session_id": data["session_id"],
            "workspace": data["workspace"],
            "title": clean(data["title"]),
            "last_activity": data["last_ts"],
            "turns": [
                {"role": role, "time": fmt_date(ts), "text": clean(text[: args.max_chars])}
                for role, ts, text in window
            ],
        }, ensure_ascii=False, indent=2))
        return 0
    print(f"Session {data['provider']}:{data['session_id']}")
    print(f"Workspace: {data['workspace'] or 'unknown'}")
    print(f"Last activity: {fmt_date(data['last_ts'])}")
    if data["title"]:
        print(f"Last prompt: {clean(data['title'][:200])}")
    print()
    for role, ts, text in window:
        print(f"[{fmt_date(ts)}] {role}: {clean(text[: args.max_chars])}")
        print()
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    search = sub.add_parser("search", help="rank sessions across agents for a query")
    search.add_argument("query")
    search.add_argument("--provider", help="comma list: qoder,claude,codex,gemini (default: all)")
    search.add_argument("--workspace", help="substring of workspace or path")
    search.add_argument("--since", help="YYYY-MM-DD; keep sessions active on/after")
    search.add_argument("--limit", type=int, default=8)
    search.add_argument("--exclude", help="provider:id or bare id to drop")
    search.add_argument("--keep-live", action="store_true", help="include the live session")
    search.add_argument("--root", help="override the root of a single --provider")
    search.add_argument("--json", action="store_true")
    search.set_defaults(func=cmd_search)

    show = sub.add_parser("show", help="print the last turns of one session")
    show.add_argument("session", help="provider:id, id prefix, or a unique id shared by one agent")
    show.add_argument("--provider", help="restrict to one provider")
    show.add_argument("--turns", type=int, default=12)
    show.add_argument("--max-chars", type=int, default=500)
    show.add_argument("--raw", action="store_true", help="do not redact credential-shaped strings")
    show.add_argument("--root", help="override the root of a single provider")
    show.add_argument("--json", action="store_true")
    show.set_defaults(func=cmd_show)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

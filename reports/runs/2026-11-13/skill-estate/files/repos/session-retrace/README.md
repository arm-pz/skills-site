# session-retrace

An agent skill that finds a past AI coding conversation from a fuzzy memory — "the session where we
fixed the Spotter palette". It searches the transcripts Qoder, Claude Code, Codex and Gemini CLI
already keep on disk, ranks matches with verbatim evidence, and prints the chosen chat. It never
invents a session, and it says plainly when nothing matches.

```
npx skills add arm-pz/session-retrace --skill session-retrace
```

Ask it things like:

- "Find the session where we fixed the Spotter palette."
- "Which Claude Code chat had the marketplace plugin discussion?"
- "Where is that Codex session with the apinex curl test?"
- "Which chat did I brainstorm skill names in?"

Every one of those tools has a session picker with no content search. This skill is the search bar,
and it searches all four at once.

## What it reads

| Agent | Location | Notes |
| --- | --- | --- |
| Qoder | `~/.qoder/projects/<slug>/<id>.jsonl` | full turns; the sibling `state.json` is encrypted and never opened |
| Claude Code | `~/.claude/projects/<slug>/<id>.jsonl` | full turns |
| Codex | `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` | full turns, merged with `~/.codex/history.jsonl` for prompts whose rollout is gone |
| Gemini CLI | `~/.gemini/tmp/<alias>/chats/session-*.jsonl` | snapshot-format messages |

Environment overrides are honoured: `QODER_CONFIG_DIR`, `CLAUDE_CONFIG_DIR`, `CODEX_HOME`. `--root`
points a single `--provider` at a non-standard directory.

Not covered: Cursor keeps chats in SQLite, GitHub Copilot writes extension logs, and OpenCode had no
readable transcripts on the machine this was built against. The skill names those as unsupported
rather than silently returning nothing.

## Use

Search every agent (default), a subset, or one:

```
python scripts/session_retrace.py search "spotter palette" --limit 8
python scripts/session_retrace.py search "marketplace plugin" --provider claude,codex
python scripts/session_retrace.py search "redirect fix" --workspace spotter --since 2026-10-01
```

Rows carry an agent-qualified ID, the date, the workspace, a score and a verbatim snippet. Read a
winner by ID:

```
python scripts/session_retrace.py show claude:b862d5d6 --turns 12
```

A bare unique ID prefix works when only one agent matches. `show` prints the last N user turns with
their replies, not the whole transcript.

Flags: `--provider`, `--workspace`, `--since`, `--limit`, `--exclude agent:id`, `--keep-live`,
`--root`, `--json`; `show` takes `--turns`, `--max-chars`, `--raw`.

## Example

A real run, query `ayurvedic brand`, all four agents. About 1,460 local transcripts were read in about
seven seconds; two contained every term:

```
| # | Date | Agent | Workspace | Session | Score | Evidence |
|---|------|-------|-----------|---------|-------|----------|
| 1 | 2026-10-16 10:39 | qoder | public_html_crz | qoder:30dd7939 | 80 | user: …JSON-LD brand, all body text… |
| 2 | 2026-10-13 03:27 | claude | CLaudeTest\Websites | claude:b862d5d6 | 70 | assistant: …brand name options: Samhita… |
```

## How the pieces fit

- **No index.** Every run reads the files. On the corpus this was built against (96 Qoder, 63 Claude
  Code, 1 Codex, 1,304 Gemini files; 371 MB of it Qoder) a query takes 5–8 seconds. A raw-text
  prefilter was tried and removed: it read matching files twice and made runs slower.
- **Scoring.** Case-insensitive substring counts, user text ×3 and assistant text ×1, capped at three
  hits per message, plus a phrase bonus when the whole query appears in a user message. Ranked by
  score, then by last activity.
- **Live sessions.** The current conversation is skipped when its last message is under 600 s old and
  one of the last three user messages contains most query terms. Rows active in the last 300 s are
  marked `(live?)` so the caller can drop them manually. None of these tools exposes its session ID as
  an environment variable, so this is a heuristic.
- **Redaction.** Search snippets, titles and `show` output pass through a redactor: `Bearer …`,
  `sk-…`, GitHub and AWS token shapes, and `api_key=` / `access_token:` / `password=` values become
  `[redacted]`. Codex history stores whole shell commands, so this is not theoretical. `--raw` prints
  the original when you explicitly need it.

## Limits

- Exact words only. No stemming, embeddings or fuzzy matching: "auth" does not match
  "authentication" unless both are passed. Reframe synonyms instead of trusting a zero result.
- A Codex session recovered from `history.jsonl` alone has user prompts but no assistant replies.
- Gemini CLI on the build machine stored only `<session_context>` injections, so Gemini searches
  return nothing there until real chats exist. The parser is there; the corpus was empty.
- Not a memory system. For durable decisions use your workspace memory index; this skill finds the
  evidence, it does not keep it.

## Status

Written and tested on Windows against real local transcripts: multi-agent search, provider filters,
`--since`, prefix lookup, and `show` for Qoder, Claude Code and Codex. `check_skill.py` reports
0 fail / 0 warn. Trigger cases in `references/test-cases.md` were hand-evaluated; live triggering of
the skill by an agent has not been run. There is no CI.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Abdul Rahman P Z.

Not affiliated with `coding_agent_session_search`, `session-recall` or other past-session tools. Those
are standalone search programs with their own provider lists; this is a skill that runs inside the
agent, and as of 2026-10-31 it is the only one here that reads Qoder's transcripts.

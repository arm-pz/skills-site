---
name: session-retrace
description: Find a past AI coding conversation from a fuzzy memory — "the session where we fixed the redirect" — across Qoder, Claude Code, Codex and Gemini CLI. Searches the transcript files those tools already keep on disk, ranks sessions with verbatim evidence and a session ID, then prints the chosen chat. Use when the user cannot find an earlier session, asks which chat covered something, asks to search past sessions or conversation history, or wants to reopen a conversation from a rough recollection. Not for searching code or project files (use Grep), summarizing the conversation already open, or durable project memory (use the workspace memory index).
version: 1.0.0
---

# session-retrace

Each supported agent keeps its conversations as plaintext JSONL on disk, but their session pickers have no content search. This skill finds the session by what was said in it.

| Agent | Default location | Notes |
| --- | --- | --- |
| `qoder` | `~/.qoder/projects/<slug>/<id>.jsonl` | full turns; sibling `state.json` is encrypted — never read it |
| `claude` | `~/.claude/projects/<slug>/<id>.jsonl` | full turns; Claude Code writes the same event schema as Qoder |
| `codex` | `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` | full turns, plus `~/.codex/history.jsonl` for prompts whose rollout is gone |
| `gemini` | `~/.gemini/tmp/<alias>/chats/session-*.jsonl` | snapshot-format messages |

Environment overrides: `QODER_CONFIG_DIR`, `CLAUDE_CONFIG_DIR`, `CODEX_HOME`; `--root` points one `--provider` at a non-standard tree. Cursor (SQLite), GitHub Copilot (logs only) and OpenCode (no usable transcripts on this machine) are not covered — say so instead of pretending to search them.

## Workflow

1. Turn the memory into search terms. Drop filler ("the one where", "I think"), keep proper nouns and tool names verbatim, and add one synonym for a vague noun ("login problem" → redirect, auth, 401). If the user gives one generic word, ask once for the project, agent, or rough date — one question, not an interview.

2. Search every agent by default (resolve `<skill>` to the base directory you were given):

   ```
   python <skill>/scripts/session_retrace.py search "spotter palette" --limit 8
   ```

   Add `--provider claude,codex` when the user names an agent, `--workspace spotter` when they name a project, `--since 2026-10-01` when they name a time. Rows marked `(live?)` were written in the last five minutes; the current conversation is usually the newest — drop it unless that is what the user asked about. The script also skips the live session automatically when its last user messages contain most query terms.

3. Present at most three candidates as: date — agent — workspace — verbatim evidence — `agent:id` (the script prints an 8-character ID; show it with the agent prefix). Read a full transcript only after the user picks one or asks what was decided. If nothing matches, say so and show the two nearest rows; never present a session as the answer without evidence from it.

4. To read the winner:

   ```
   python <skill>/scripts/session_retrace.py show claude:b862d5d6 --turns 12
   ```

   A bare unique ID prefix also works when the user quotes one. Summarize decisions and open threads; quote at most one line per point. `--raw` disables credential redaction — use it only when the user asks for an exact transcript.

## Output contract

- Every candidate carries its agent label and session ID (`claude:04499362`); without both the user may open the wrong tool's chat.
- Evidence is a verbatim snippet, not a paraphrase. Credential-shaped strings (`Bearer …`, `sk-…`, `api_key=…`) are replaced with `[redacted]`; never reconstruct or print the original.
- Codex sessions recovered from `history.jsonl` alone hold user prompts only — say that when the excerpt has no assistant replies.
- State when the only match is the live conversation.

## Boundaries

- Exact substring search only: it finds words, not meaning. Reframe synonyms instead of trusting a zero result.
- Not for code search (Grep), web search, or recovering context lost to compaction in this conversation.
- Not durable memory: the workspace `MEMORY.md` and chief-of-staff's wiki own that. If the user wants the found decision preserved, offer to write it to the workspace memory index. Handoff: the memory note receives the decision, the agent-qualified session ID, and the date.
- Read `references/transcript-format.md` when a search returns nothing, a term should clearly match, or the script errors; this file wins where the two disagree.
- Read `references/test-cases.md` before changing the description or trigger wording; it records which requests must and must not trigger this skill.

# Transcript formats and search mechanics

Observed 2026-10-31 on this machine: 96 Qoder transcripts (371 MB), 63 Claude Code transcripts, 1 Codex rollout plus a 2-line `history.jsonl`, and 1,304 Gemini CLI files. If a search returns nothing when a term is clearly present, re-check the layout before blaming the query.

## Where each agent writes

| Agent | Root | File pattern | Root override |
| --- | --- | --- | --- |
| `qoder` | `~/.qoder/projects` | `<slug>/<sessionId>.jsonl` | `$QODER_CONFIG_DIR/projects` |
| `claude` | `~/.claude/projects` | `<slug>/<sessionId>.jsonl` | `$CLAUDE_CONFIG_DIR/projects` |
| `codex` | `~/.codex` | `sessions/YYYY/MM/DD/rollout-*.jsonl` + `history.jsonl` | `$CODEX_HOME` |
| `gemini` | `~/.gemini/tmp` | `<alias>/chats/session-*.jsonl` | none |

`--root` overrides the root for a single `--provider`; it is ignored when several providers are scanned at once, because one path cannot be four trees.

## Qoder and Claude Code

Same event schema, one JSON object per line:

| `type` | Useful fields | Use |
| --- | --- | --- |
| `user` | `message.content` (string or block list), `timestamp`, `isSidechain` | searchable, weight 3 |
| `assistant` | `message.content` (block list), `timestamp` | searchable, weight 1 |
| `last-prompt` | `lastPrompt` | session title / last user prompt |
| `workspace-directories` | `directories[]` | absolute workspace path |
| `runtime-config` | `model`, epoch-ms `timestamp` | ignored |
| `attachment` | file references | ignored |
| `active-leaf` | branch leaf UUID | ignored |

Content blocks: keep `type: "text"` only. Skip user `tool_result` blocks (file dumps, command output) and assistant `thinking` / `tool_use` blocks — they inflate scores with code and arguments the user never wrote. Slash-command invocations arrive as `<command-message>` text plus a separate skill-body message; both count as user text, which is why tool names find their sessions.

Message timestamps are ISO 8601 strings and sort lexically. `runtime-config` uses epoch milliseconds and must not be mixed in.

Layout facts: the workspace slug replaces every non-alphanumeric character of the cwd one for one (`C:\Users\abdul\Downloads\Qoder\spotter` → `C--Users-abdul-Downloads-Qoder-spotter`). Qoder's sibling `<sessionId>/state.json` holds encrypted blobs (`n`, `p`, `t`) and is never opened. Claude Code subagent transcripts under `<sessionId>/subagents/` are not read; only top-level `<slug>/*.jsonl` files are.

## Codex

A rollout file interleaves three event kinds:

- `session_meta` — `payload.session_id`, `payload.cwd`, and a large `base_instructions.text`. The instructions are agent boilerplate, not conversation; the parser ignores them.
- `response_item` with `payload.type: "message"` — `payload.role` plus `payload.content[]` blocks carrying `input_text`, `output_text` or `text`.
- `event_msg` with `payload.type: "item_completed"` — `payload.item.type` is `UserMessage` or `AgentMessage`; text sits in `item.content` or `item.text`. The same turn often appears as both `response_item` and `event_msg`; identical text is de-duplicated.

`~/.codex/history.jsonl` is separate and simpler: one object per prompt, `{session_id, ts (epoch seconds), text}`. It survives after the rollout is pruned, so the loader merges it into the rollout by session ID. History-only sessions contain user prompts and no assistant replies — a real limit, not a bug. `ts` is UTC.

## Gemini CLI

Each `chats/session-*.jsonl` starts with metadata lines, then contains one or more `{"$set": {"messages": [...]}}` snapshot records. Snapshots are cumulative, so the last one wins; earlier snapshots are stale copies. Message objects use `type: "user"` or `"gemini"` / `"model"`, with text in `content` or `text`. The workspace label is the parent of `chats/`. On this machine every one of the 1,304 files is a single `<session_context>` injection with no user turns, so Gemini searches legitimately return zero rows here; that is the corpus, not a parser failure.

## Injected blocks

All parsers skip text starting with `<environment_context`, `<skills_instructions`, `<session_context`, `<user_instructions`, `<permissions`, `<turn_aborted` or `<command-message`. These are tool-generated preambles that would match almost any query.

## Scoring

- Case-insensitive substring count per term, capped at 3 occurrences per message, user text ×3, assistant text ×1.
- Phrase bonus +15 when the whole query appears in a user message.
- Rank by score, then by last activity. There is no index; every run reads the files (about 5–8 seconds for roughly 1,460 transcripts, 371 MB of which is Qoder). A raw-text prefilter was tried and made it slower, because matching files then had to be read twice.

## Live-session handling

- Auto-skip: last message timestamp within 600 s **and** one of the last three user messages contains at least 60% of the terms. This is a heuristic, not an identity check — none of these tools exposes its session ID as an environment variable.
- `(live?)` marks any session active within 300 s, so the caller can drop it manually when the heuristic misses (common with one-term queries, where the current session matches via assistant text).
- `--keep-live` disables both filters; `--exclude provider:id` drops a known session.

## Credential redaction

Search evidence, titles and `show` output pass through `redact()`: `Bearer <token>`, `sk-…`, `ghp_/gho_/ghu_/ghs_/ghr_…`, AWS `AKIA…`, and `api_key|access_token|client_secret|password` followed by a long value are replaced with `[redacted]`. Codex history stores full shell commands, so this matters: one local prompt contains a live bearer token. `show --raw` prints the original text when the user explicitly needs it.

## Limits

- Exact words only. No stemming, embeddings, or fuzzy matching; "auth" does not match "authentication" unless both are passed.
- Subagent sidechains in Qoder/Claude parent files are included because they carry useful conclusions; they inflate counts slightly.
- Cursor keeps chats in SQLite, GitHub Copilot writes extension logs, and OpenCode had no readable transcripts here. None is parsed; the skill names them as unsupported instead of silently returning nothing.

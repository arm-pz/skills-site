# Trigger and boundary cases

Marked **run** only when the message was actually fed through triggering; **hand** means judged by reading descriptions. This draft: all trigger cases hand-evaluated. Script behaviour was exercised for cases 1–3 and 11 (multi-provider search, Claude `show`, Codex `show`, provider filters, `--since`, prefix `show`). Gemini returns zero rows here because its local corpus holds only context injections. Live triggering has not been run.

| # | Message | Expected skill | Expected mode or command | Pass condition |
|---|---------|----------------|--------------------------|----------------|
| 1 | "find the session where we fixed the Spotter palette" | session-retrace | `search "spotter palette"`, then present | ranked rows across agents, each with `agent:id` and verbatim evidence; live row dropped |
| 2 | "which Claude Code chat had the marketplace plugin discussion?" | session-retrace | `search "marketplace plugin" --provider claude` | searches Claude only; presents date, workspace, ID |
| 3 | "I used Codex for that apinex curl test — where is it?" | session-retrace | `search "apinex curl" --provider codex` | finds the Codex session, redacts the bearer token, notes prompts-only if history-backed |
| 4 | "which chat did I brainstorm skill names in? I think it was last week" | session-retrace | `search "skill names" --since <date>` | offers candidates, asks which one before dumping a transcript |
| 5 | "where did we discuss the dbt pipeline? I can't find that conversation anywhere" | session-retrace | `search "dbt pipeline"` | top three only; says "no match" honestly if empty |
| 6 | "search my Cursor chats for the license decision" | session-retrace, unsupported agent | none | says Cursor is not readable, offers Qoder/Claude/Codex/Gemini instead; does not fake a result |
| 7 | "where is the palette defined in the Spotter code?" | code search (Grep) | none | no transcript scan; answers from code |
| 8 | "what did we decide earlier in this conversation about the skill name?" | none (live context) | none | no script run; answers from the open conversation |
| 9 | "remember that I prefer brass themes" | workspace memory | none | writes/answers as memory; no transcript scan |
| 10 | "search the web for session recall tools" | web search | none | does not run the local transcript script |
| 11 | "search all my AI sessions — Qoder, Claude, whatever — for the redirect fix" | session-retrace | `search "redirect fix"` with default providers | all four agents scanned in one run; rows labelled by agent |

## Boundary pairs

| Message | Should trigger | Why |
|---------|----------------|-----|
| "Find the session where we made the SECURITY.md decisions" | session-retrace | retrieval of a past conversation |
| "Save that decision to project memory so I don't ask again" | workspace memory | durable storage, not retrieval |

| Message | Should trigger | Why |
|---------|----------------|-----|
| "Search past sessions for the license policy decision, then save it to memory" | session-retrace first, then memory | retrieval produces the evidence; memory receives the decision, agent-qualified session ID and date |

| Message | Should trigger | Why |
|---------|----------------|-----|
| "What does `session_retrace.py` do?" | none (answer directly) | a question about the skill, not a request to search history |

Known weak spots: a one-term query can surface the live conversation through assistant text — the `(live?)` marker exists for that. A Codex session known only from `history.jsonl` has user prompts but no assistant replies, so a decision discussed only in the reply is not recoverable there.

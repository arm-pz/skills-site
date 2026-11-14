# Sources

Checked 2026-11-14 against Claude Code documentation (code.claude.com/docs/en).

| Claim in SKILL.md | Result | Source |
|---|---|---|
| `/effort` opens a slider; `/effort <level>` sets it; `/effort auto` clears the saved level | Confirmed | model-config, "The /effort command" |
| `claude --effort <level>` sets one session | Confirmed | model-config, "The --effort flag" |
| Levels low, medium, high, xhigh, max | Confirmed for current models; Opus 4.6 and Sonnet 4.6 lack `xhigh` (falls back to `high`) | model-config, supported levels table |
| Unsupported level falls back silently | Corrected: falls back to highest supported level at or below it | model-config |
| Typed `/effort <level>` is saved as default | Confirmed (was "may save"); `s` in slider is session-only, v2.1.257+ | model-config |
| Subagents inherit session effort by default | Corrected: only on the main conversation's model; frontmatter `effort` overrides | model-config, "Subagents" |
| Agent teams | Added: experimental, off by default, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, significantly more tokens | agent-teams |
| `/usage`, `/goal` exist | Confirmed | commands |
| Default effort per model | Not stated as a fixed value; docs say new models default to `medium`, Opus 4.7 `xhigh`, others `high` | model-config, resolution order |

Not checked: the `npx skills add arm-pz/choose-effort --skill choose-effort` install command and the sibling repo link `arm-pz/diagnose-usage` (GitHub returned 403 to this session); the live About text and topics; the sibling skills' SKILL.md files (`diagnose-usage`, `product-self-knowledge`); `/goal` behaviour beyond its command entry.

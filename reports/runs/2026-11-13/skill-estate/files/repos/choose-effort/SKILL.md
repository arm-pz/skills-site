---
name: choose-effort
description: Asks the user how much effort a Claude Code task deserves before heavy work starts, then recommends an effort level, whether to fan out to subagents, goal mode, workflows or agent teams, how to set it, and when to check /usage. Use when the user is about to start a large, long or unattended Claude Code task, asks what effort level to use or whether to use xhigh or max, asks how to use less usage from now on, or is about to start /goal, a workflow or an agent team. Not for working out why usage already drained (use diagnose-usage), or for plan limits, prices and which models support which levels (use product-self-knowledge).
version: 1.0.0
---

# Choose effort

Effort is the setting most likely to turn one session into a heavy one, and Anthropic says subagents inherit it by default, so a high level multiplied across agents adds up fast. This skill asks a few questions before the work starts, then recommends a level and a plan for checking in. It recommends; the user sets.

## Ground rules

- **Ask before recommending.** The right level depends on the task and how much the user wants to spend. Guessing high wastes usage; guessing low wastes the run.
- **Never claim a setting is changed.** `/effort` is a built-in the user types. Give the exact command and wait for them to confirm; do not say "set to high" as though it happened.
- **Read the levels from the user's session.** Which levels exist, and the default, depend on the model, and an unsupported level can fall back silently. If unsure, ask the user to open `/effort` and tell you what the slider offers.
- **The table is a starting point.** Anthropic's effort guidance gives a different default and a different recommended start for each model, so the table is a rough default, not a rule. Check the docs for the user's model before stating a level as the right one.

## Workflow

1. Ask up to three questions in one message, using the interactive question tool if the host has one. Skip any already answered.
   - Task shape: quick fix, normal feature, large refactor or migration, hard debugging or design, or an unattended run.
   - Cost of being wrong: throwaway, or going to production.
   - Usage appetite: tight, normal, or no concern.
2. Pick a starting level from the table.
3. Check for fan-out. If the plan uses subagents, Agent Teams, workflows, `/goal` or a long SDK job, say so plainly: Anthropic says subagents inherit the session's effort by default. Recommend a lower session level when the fan-out is mechanical, and a first checkpoint.
4. Give the answer in the shape below.

| Task | Start at |
|---|---|
| Rename, summarise, small scoped edit | low |
| Normal feature work | medium, or the model default |
| Hard debugging, design, large refactor | high |
| Production-critical work where high already fell short | xhigh |
| One-off hardest problem, this session only | max |

`references/trigger-cases.md` holds the test cases. Open it only when tuning the description above.

## Answer shape

- **Read:** the task in one line.
- **Effort:** the level, and why in one clause.
- **Fan-out:** none, or what to watch.
- **Set it:** `/effort <level>`, or `claude --effort <level>` for one launched session. Tell the user to read the confirmation text, since `/effort` may save the level as their default; `/effort auto` undoes it.
- **Checkpoint:** run `/usage` after the first stage and at the end.

## Hand off

- A drain that has already happened goes to `diagnose-usage`.
- Plan allowances, prices, and which models support which levels go to `product-self-knowledge`.

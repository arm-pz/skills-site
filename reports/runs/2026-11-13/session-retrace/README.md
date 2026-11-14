# session-retrace: real-world run, 2026-11-13

**Verdict: PARTIAL** (5/10). The run searched with the bundled script and found one candidate, claude:eda1adb5 (2026-11-13, workspace /tmp/run-ship-second-brain-69r37__h/project), which matches the ground truth, but it gave no decisions because it never read beyond a 12-turn view.

Target: real Claude Code session files from this batch of runs. Run headless on sonnet in a clean project with only this skill installed (7 turns, 5 tool calls, 13 s, $0.08).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
I can't find the chat where we built a team second brain about split payments and the Stackwise call. Which session was it, and what did we decide in it?
```

## Rubric

- Searches the transcript files on disk with the bundled script
- Ranks at most three candidates with date, workspace, verbatim evidence and an agent:id
- The top candidate's id matches a session in the ground truth
- Summarises the chosen session's decisions without inventing any

## Hard checks


## Met

- Searched the transcript files on disk with the bundled session_retrace.py script
- Top candidate id (eda1adb5) matches the ground truth session
- Gave date, workspace and verbatim prompt evidence for the candidate, at no more than three candidates
- Invented no decisions; it said plainly that it could not recover the answers

## Missed

- Did not summarise the session's decisions on split payments, overpayments or the Stackwise promise; it stopped after a 12-turn view and only offered to read 40 turns
- Evidence is labelled with 'claude:eda1adb5' rather than the agent:id form (agent-aed7119ed04059d93), and the other ground-truth id was not surfaced
- Tried to read the vault on disk (ls, Glob) instead of reading further into the transcript, which is where the decisions would be
- Did not use the available follow-up (show with more turns) before giving up, so the user's second question went unanswered

## Defects to fix in the skill

- The skill does not tell the agent to read enough of the chosen session (e.g. the final assistant answer) to report decisions, so a shallow show --turns 12 can leave the second half of the question unanswered
- The skill does not make clear that the id to report is the agent:id form, so the output used claude:eda1adb5
- The skill does not steer the agent toward the transcript's final answer turns rather than re-reading workspace files that may no longer exist

## Ground truth

```
agent-aed7119ed04059d93
eda1adb5-d41a-45ea-b194-ed172aadf0d2
```

## What it did

1. `Skill: session-retrace`
1. `Bash: python /tmp/run-session-retrace-oekdksx9/project/.claude/skills/session-retrace/scripts/session_retrace.py search "Stackwise split payments second brain" --limi`
1. `Bash: python /tmp/run-session-retrace-oekdksx9/project/.claude/skills/session-retrace/scripts/session_retrace.py show claude:eda1adb5 --turns 12`
1. `Bash: cd /tmp/run-ship-second-brain-69r37__h/project 2>&1 && ls -R vault | head -30; cat vault/gaps.md 2>&1 | head -40`
1. `Glob: vault/**/*.md`

## Final output

I found the session, but I can't tell you what it decided about split payments or Stackwise. The transcript doesn't contain those answers, and the vault it built is no longer on disk.

**The session**
- **ID:** `claude:eda1adb5`, a Claude Code session.
- **Date:** 2026-11-13, around 18:21–18:22.
- **Workspace:** `/tmp/run-ship-second-brain-69r37__h/project`.
- **Evidence (your prompt):** "Build our team second brain in ./vault from the sources in this folder (issue-412.md, pr-431.md, call-2026-11-04.md). Then answer from the vault alone: 1) Are split payments handled? Since when? 2) Are overpayments handled? 3) Did we promise Stackwise anything about QuickBooks?"
- **Other matches:** it was the only match. The search also skipped one live session, probably this one.

**What the transcript shows**
- Claude built a markdown vault from the three source files, then had a fresh subagent answer your three questions from the vault alone.
- It also wrote a `gaps.md` listing what the test found missing.
- It did not run `check_vault.py`, because Bash was denied in don't-ask mode. So no raw-file snapshot was recorded.
- It checked every quote against its source by eye and marked 8 notes `verified`.
- The ninth note is marked `seen`: Sam's "probably in the next release". Engineering never confirmed it.

**What I couldn't recover**
- The transcript text I read doesn't include the answers to your three questions.
- The vault folder no longer exists. Its workspace directory is gone, and Bash is denied here, so I couldn't read the notes or `gaps.md`.

Two things could get the answers back. You could re-run the session's three source files through the vault build, or you could point me at a copy of the vault or the source files. I can also read more of the transcript with `show claude:eda1adb5 --turns 40`. That might surface the answers, which the 12-turn view didn't.

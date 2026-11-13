# choose-effort: real-world run, 2026-11-13

**Verdict: PARTIAL** (6/10). The skill asked two clarifying questions, then in the same turn recommended `/effort high`, mostly serial execution, batches of 10-15 files and `/usage` checks, but it never waited for the answers and its fallback and permission advice is vague.

Target: a large unattended refactor in Claude Code. Run headless in a clean project with only this skill installed (4 turns, 1 tool calls, 22 s, $0.15).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
I'm about to have Claude Code migrate our whole Express API (about 140 route files) from callbacks to async/await while I'm in meetings all afternoon. What effort level and setup should I use?
```

Follow-up:

```
It matters a lot that it's correct; tests exist for about 70% of routes. I'm on a Max 5x plan and I've used 40% of my weekly limit already. I'd rather it be slow than wrong.
```

## Rubric

- Asks how much effort the task deserves before recommending (budget, stakes, attended or not)
- After the answer, recommends a specific effort level and whether to fan out to subagents/workflows, matching the stakes and the remaining weekly budget
- Says exactly how to set it
- Says when to check /usage and what to do if it runs hot
- States only real Claude Code features and commands

## Hard checks


## Met

- Asked about stakes (cost of being wrong) and usage appetite before recommending, and noted the task is unattended
- Recommended a specific level (`high`, escalating to `xhigh` for hard files only) and said to keep it serial or use few subagents, justified by the stakes, the 60% of weekly limit remaining, and that subagents inherit session effort
- Said exactly how to set it: type `/effort high` or launch `claude --effort high`, with `/effort auto` to undo
- Said when to run /usage (after the first batch and at the end) and what to do if it runs hot (drop to `medium` for mechanical files)
- Features named (`/effort`, `/usage`, `claude --effort`, subagent effort inheritance, permission modes) are plausible real Claude Code features, and the output admits it hasn't verified which levels the model supports

## Missed

- Did not wait for the user's answer: it asked two questions and then gave a full recommendation in the same turn, so the ask-then-recommend sequence was not respected. It also re-asked about stakes after the user had signaled correctness mattered (the scenario's follow-up supplied that)
- The 'runs hot' guidance is thin: the 'about 1/10 of what you can afford' threshold is arbitrary and it gives no concrete action such as pausing, stopping the run, or shrinking batch size. It also doesn't explain how to monitor usage while the user is away in meetings
- Permission-mode advice is vague ('pick a permission mode that lets it run edits and tests') and doesn't name a specific mode or setting for the unattended run
- Output is long and repeats itself (fan-out, git and checkpoint advice each appear twice), which dilutes the answer
- Spent effort on the 'no git repo' environment detail that the user never raised, and stated the working directory path, which was irrelevant to the question

## Defects to fix in the skill

- The skill should ask its clarifying questions and stop, or if the answers are already in the prompt or follow-up, skip the questions entirely; it currently does both in one turn
- It should give a concrete unattended-run recipe (a named permission mode, a hard stop condition and a usage-check trigger that works while the user is away) instead of generic advice
- It should require concise output without repeating the same points in the pre-answer and recommendation sections
- It should tell the model not to bring in unrelated environment observations (e.g. working directory path) unless they affect the recommendation

## What it did

1. `Skill: choose-effort`

## Final output

Before I recommend a level, I need two answers. You've already told me it's a large, unattended migration.

1. **Cost of being wrong:** Does this go straight to production, or will it go through PR review and your test suite first?
2. **Usage appetite:** Is your usage tight, normal, or not a concern this afternoon?

Some things will shape the answer either way:

- **No git repo here.** The working directory (`/tmp/run-choose-effort-mycbn4u0/project`) isn't a git repository. For an unattended 140-file rewrite, I'd run `git init` and commit a baseline first, or work on a branch. Otherwise you can't review or roll back what changed.
- **Tests.** If the API has a test suite, tell me how to run it. A migration that can check itself against tests needs far less effort per file than one that can't.
- **Fan-out.** Splitting 140 files across subagents or a workflow is tempting. Anthropic says subagents inherit the session's effort by default, so a high level gets multiplied across every agent. This work is mostly mechanical, so I'd lean toward a lower session level, probably medium, plus a first checkpoint after a small batch (say 10 to 15 files). That batch would let you see the quality and the cost before the rest runs while you're in meetings.
- **Hard spots.** Callback-to-async conversion is mostly pattern work. The tricky parts are error handling, callbacks that fire more than once, streams, and code that mixes callbacks and promises. Those are worth flagging for human review rather than paying for a higher level on every file.

Once you answer the two questions, I'll give you the exact `/effort` command. You'll need to type it yourself, because I can't change it for you. I'll also tell you when to run `/usage`.

---

**Read:** A large, unattended, correctness-critical migration of 140 route files. About 70% have tests, and you've used 40% of your weekly limit.

**Effort:** `high`. This is a big refactor where subtle behavior changes matter, but the work is mostly pattern conversion, so `xhigh` or `max` would spend your remaining 60% on files that don't need it. If the first batch shows missed error paths or broken tests, move up to `xhigh` for the hard files only.

I haven't checked which levels your model offers or what its default is. Open `/effort` and tell me what the slider shows. An unsupported level can fall back silently.

**Fan-out:** I'd keep it serial, or use at most a few agents. Subagents inherit the session's effort by default, so a fan-out at `high` multiplies your spend, and you said slow is fine. If you do want parallelism, split by directory so agents never touch the same files.

**Setup for correctness:**
- Run `git init` and commit a baseline first, or work on a branch. This directory isn't a git repo, and without one you can't diff or roll back the run.
- Run the existing tests before starting, so you know which failures were already there.
- Work in batches of roughly 10 to 15 files. After each batch, run the tests and commit.
- For the ~30% of routes without tests, have it write characterization tests first, capturing current behavior (status codes, response bodies, error paths), and then convert. Otherwise "correct" has nothing to check against.
- Tell it to stop and list any file where it isn't sure the behavior is preserved, rather than guessing. Examples are callbacks that can fire twice, streams, mixed callback/promise code, and Express 4 handlers that don't catch rejected promises (these need a wrapper or `express-async-errors`).
- Pick a permission mode that lets it run edits and tests without prompting, or it will stall waiting for you. Allow file edits and your test command only, nothing broader.

**Set it:** Type `/effort high` yourself, or launch with `claude --effort high`. Read the confirmation text, since `/effort` may save the level as your default. `/effort auto` undoes it.

**Checkpoint:** Run `/usage` after the first batch, so you can see how much a batch costs and project the total. Run it again at the end. If the first batch uses more than about 1/10 of what you can afford, drop to `medium` for the mechanical files before leaving it running.

When you're ready, I can write the starting prompt with the batching, test-first and stop-and-flag rules built in.

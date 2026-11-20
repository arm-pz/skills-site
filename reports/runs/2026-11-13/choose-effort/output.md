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
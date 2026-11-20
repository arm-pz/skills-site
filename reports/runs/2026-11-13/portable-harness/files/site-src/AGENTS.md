## Rules

1. Think before coding: state assumptions, and ask rather than guess.
2. Simplicity first: write the minimum code, and nothing speculative.
3. Surgical changes: don't "improve" code next to what you're changing.
4. Goal-driven: define success criteria and loop until they're verified.
5. Use the model only for judgment calls. If code can answer, code answers.
6. Token budgets aren't advisory: 30k per session, then summarize and start fresh.
7. Surface conflicts instead of averaging them.
8. Read before you write: check exports, callers and shared utilities.
9. Tests verify intent, not just behaviour.
10. Checkpoint after every significant step.
11. Match the codebase's conventions, even if you disagree.
12. Fail loud. "Tests pass" is wrong if any were skipped.

<!-- Rules 1-4: Jiayuan Chang's write-up of Andrej Karpathy's thread on how coding agents go wrong. Rules 5-12: collected from posts on X, authors unknown. -->

Tests: `python3 -m unittest discover -s tools/agent-skills/tests`. Architecture and publish flow: `PROJECT.md`.

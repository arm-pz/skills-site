# Changelog

## 0.1.0 — 2026-11-24

First version. Level 3 of the agent ladder.

- `SKILL.md`: six-step workflow (read the loop, confirm cases, write `evals/`, score, read the trace, close the loop) and the level 3 exit test that `agent-ladder` reads.
- `scripts/score.py`: scores a run folder against a golden set or invariants file; ten check types including `not_in_previous` (dedup) and `judge` (pending until the agent writes `judgments.json`); baseline comparison; exit 0/1/2.
- `scripts/traces.py`: condenses a Claude Code session, `claude -p` stream-json output or a plain log into tool calls, errors, permission denials, how the run ended and the final text, with secrets masked.
- `references/golden-set.md`, `references/failure-taxonomy.md`.
- `tests/test_scripts.py`: 22 checks on both scripts, all passing.

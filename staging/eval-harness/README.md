# eval-harness

An AI agent skill that tells you whether a recurring agent loop is actually any good. It builds a
**golden set** of frozen inputs with checkable expectations, a **scorecard** that runs in one command and
fails when the loop gets worse, and a **trace reader** that walks a failed run back to its cause.

It is written for loops: a skill that runs on a schedule and reports (a nightly SEO sweep, an inbox
triage, a weekly digest). It works the same on any skill whose output you can save to a file.

Level 3 of the agent ladder: `loop-schedule` makes a loop run (level 2), this one says whether its
output is right, and `action-gate` lets it act only once this level's exit test passes (level 4).

## Install

```
npx skills add arm-pz/eval-harness --skill eval-harness
```

Or copy `skills/eval-harness/` into `~/.claude/skills/` (Claude Code), `~/.codex/skills/` (Codex) or
`~/.qoder/skills/` (Qoder), then start a new session. The scripts need Python 3.9+ and nothing else.

## Ask it things like

- "Build a golden set for my nightly SEO report so I know if it's any good."
- "Give the weekly digest a scorecard that fails when I make the prompt worse."
- "My scheduled competitor check reported nonsense last night. Why?"
- "Does my inbox-sweep loop pass level 3?"

## What it writes in your project

```
evals/
  golden.jsonl        12–20 cases: positive, negative, edge, regression, each with a source
  invariants.jsonl    checks every real scheduled run must pass (dedup included)
  fixtures/<id>/      frozen inputs
  runs/<run-id>/      outputs per case + judgments.json
  baseline.json       last accepted score
  calibration.md      LLM judge vs your labels, if any judge checks exist
  failures.md         diagnosed failures: class, trace evidence, fix
```

Expectations are written as checks first: `contains`, `regex`, `count`, `max_lines`, `json`,
`not_in_previous` (the dedup check) and a few more. An LLM-judge rubric is used only where no check fits,
and only after it agrees with your own grading on 8 of 10 outputs.

## The two scripts

```
python skills/eval-harness/scripts/score.py evals/golden.jsonl evals/runs/<run-id> --baseline evals/baseline.json --out evals/scorecard
python skills/eval-harness/scripts/traces.py ~/.claude/projects/<project>/<session>.jsonl
```

`score.py` exits 0 on pass, 1 on a regression or a failed critical case, 2 when judge checks are
pending. It never runs the loop itself, so a score can be recomputed without paying for another run.
`traces.py` reads Claude Code sessions, `claude -p --output-format stream-json` output, or any plain log,
and masks secrets and email addresses before printing.

## Boundaries

- **Handles:** golden sets, scorecards, regression gates and failure diagnosis for a loop or skill's output.
- **Does not handle:** scheduling a skill or checking that a run happened (`loop-schedule`), whether a
  description triggers (`tune-skill`), standing rules mined from many sessions (`harness-audit`), or
  benchmarking a model (that is what EleutherAI's `lm-evaluation-harness` is for).

## Status

`SKILL.md` passes tune-skill's `check_skill.py` with 0 FAIL and 0 WARN (929 description characters,
94 body lines). `python -I tests/test_scripts.py` runs 22 checks on both scripts, all passing; `traces.py`
was also run on a real Claude Code session. The trigger cases in `tests/test-cases.md` were judged by hand,
not run in a live agent, and the skill has not yet been run end to end on a real loop.

## License

MIT. See `LICENSE`.

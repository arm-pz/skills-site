# skill-eval-suite

Evals for agent skills and scheduled agent loops. An agent skill for Claude Code (and other Agent
Skills clients) that builds an eval suite from a loop's own history and tells you whether the skill is
any good: real prompts graded on trajectory, pass rates over 3+ trials, which cases a change fixed or
broke, token budgets as gates, a hidden holdout, and a known-bad set every judge must fail first.

```
npx skills add arm-pz/skill-eval-suite --skill skill-eval-suite
```

## Ask it things like

- "Build an eval suite for my nightly SEO report."
- "Is the new prompt actually better, or did I get a lucky run?"
- "Can we trust our LLM judge before we gate PRs on it?"
- "Does this skill earn its tokens, or should we cut it?"
- "My scheduled competitor check reported nonsense last night. Why?"

Not to be confused with EleutherAI's lm-evaluation-harness (benchmarks models) or hamelsmu/evals-skills
(helps you build evals for an AI product); this one evaluates agent skills and loops. Sibling:
[log-papercut](https://github.com/arm-pz/log-papercut) has agents file friction as they hit it, and
its fixed papercuts become regression cases here.

Level 3 of the agent ladder: `loop-schedule` makes a loop run (level 2), this one says whether its
output is right, and `action-gate` lets it act only once this level's exit test passes (level 4).

## Built on

- **Uber Engineering, "How Uber Evals 1 Million Agent Skill Invocations a Month" (2026-11-23):**
  the suite mix (about 5% golden with tool mocks, 80% real prompts graded on trajectory, 15% judged by
  the author), a 70–90% target pass rate, blind with-versus-without ablation, cost per skill
  invocation, papercuts and rejected PRs fed back as cases.
- **An eval-driven development cheat sheet:** pass rates over 3+ trials, must-do / must-not /
  keep-working cases, a hidden holdout, a known-bad set every judge must fail, same-case flips instead
  of averages, and cost as a pass/fail gate.

## Install options

The command above, or copy `skills/skill-eval-suite/` into `~/.claude/skills/`, `~/.codex/skills/` or
`~/.qoder/skills/`. Python 3.9+, nothing else. Trajectory and token checks read Claude Code session
traces.

## What it writes in your project

```
evals/
  suite.jsonl         cases by tier (golden, real, author) and intent (must_do, must_not, keep_working)
  fixtures/<id>/      frozen inputs for golden cases
  runs/<id>/t1..t3/   one trace per case per trial, plus judgments.json
  baseline.json       per-case pass rates, noise band, token median
  ab-log.jsonl        every comparison's fixed, broke and net, for the repeated-loss rule
  known-bad/          outputs every gating check and judge must fail
  calibration.md      30–50 outputs graded by the judge and the author
  failures.md         diagnosed failures: class, trace evidence, fix, owner
~/.eval-holdout/<loop>/holdout.jsonl   kept outside the project, scored with --hidden only
```

## The scripts

| Script | Does |
| --- | --- |
| `score.py` | scores trials (output, trajectory, token and pipeline-gate checks): pass rate per case, flaky cases, flips against the baseline, token bill and budget, `--hidden` holdout, `--expect-fail` known-bad, `--validate` mix and intents |
| `intake.py` | candidate cases from real Claude Code sessions, papercut issues, and agent PRs people rejected or edited |
| `ablation.py` | blind pairs for with-versus-without, win share with a 95% interval and noise band, trace stats per arm |
| `traces.py` | condenses a session or log: tool calls, errors, denials, ending, final text, secrets masked; tokens for the run, per skill invocation, for subagents, and the peak context |

`score.py` exits 0 on pass, 1 when blocked (a critical case failed a trial, a golden case broke, or a
second clear loss in a row), and 2 when verdicts or trials are missing. It never runs the loop.

## Boundaries

- **Handles:** eval suites, scoring, gates and failure diagnosis for a loop or skill's behaviour.
- **Does not handle:** scheduling (`loop-schedule`), description triggering (`tune-skill`), filing
  friction mid-task (`log-papercut`), standing rules from many sessions (`harness-audit`),
  benchmarking a model, or building evals for an AI product.

## Status

`SKILL.md` passes tune-skill's `check_skill.py` (0 FAIL, 0 WARN) and `--lint` (3 of 3).
`python -I tests/test_scripts.py` runs 60 checks, all passing; `traces.py` and the trajectory checks
were also run on a real Claude Code session. Trigger cases in `tests/test-cases.md` were judged by hand.
The skill has not yet been run end to end on a real loop.

## License

MIT. See `LICENSE`.

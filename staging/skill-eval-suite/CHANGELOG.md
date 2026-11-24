# Changelog

## 0.4.0 — 2026-11-24

- Pipeline gate checks for triage-and-PR loops, each reading a context file next to the suite: `triage_skips_open_pr` (duplicate PR work), `triage_trusted_source` (issues from non-owners without `pipeline-ok`), `diff_within_spec` (files outside the spec's Files list). `.diff` and `.patch` outputs are read.
- Token windows in `traces.py`: `tokens_by_skill` (each API message's tokens go to the skill active when it was sent, Uber's cost-per-invocation method; windows add up to the total), `tokens_subagents`, `peak_context`. Repeated log events of one API message count once, at their final usage.
- New checks `skill_tokens` (cost per invocation of one skill) and `max_context`.
- Known-bad entries now pair with controls that must pass.
- `tests/test_scripts.py`: 60 checks, all passing.

## 0.3.0 — 2026-11-24

Eval-driven development rules on top of 0.2.0.

- Trials: each case is scored as passes over trials (`--repeat` takes any number). A new case needs 3 trials and a critical one 5 before it counts (exit 2 until then); split trials mark it flaky and it is kept.
- Intents: every case is `must_do`, `must_not` or `keep_working`; `--validate` names any skill missing one.
- Flips, not averages: against the baseline the scorecard lists fixed and broken cases and the net. Fixed and broke together is reported as a trade-off. Only a repeated clear loss blocks (net worse ≥ max(2, 7% of cases) and above the noise, twice in a row in `ab-log.jsonl`). Golden and critical cases stay strict.
- Token budget as a gate: `--token-budget` fails a trial over budget even when correct; `max_tokens` per case; the token bill prints on every run. `traces.py` now sums token usage per run, counting each API message once.
- Hidden holdout: `--hidden` prints aggregates only; `--tuned` flags overfitting when the suite score beats the holdout by more than max(15 points, twice the noise). tune-skill gains a rule never to read a holdout.
- Known-bad set: `--expect-fail` requires every known-bad output to fail; a check or judge that lets one through is untrusted (exit 1).
- Free path (`"path": "free"`): trajectory checks become advice and only the end state gates.
- Judge calibration raised to 30–50 author-graded samples at 80%+ agreement.
- `references/gates.md`; SKILL.md now has 12 steps and still passes `check_skill.py --lint`.
- `tests/test_scripts.py`: 49 checks, all passing.

## 0.2.0 — 2026-11-24

Rebuilt on Uber's skill-eval approach ("How Uber Evals 1 Million Agent Skill Invocations a Month", 2026-11-23).

- Suite in three tiers: ~5% `golden` (fixed input, tool mocks), ~80% `real` (real prompts graded on trajectory), ~15% `author` (only the author's verdict counts). `score.py --validate` reports the mix.
- Eight trajectory checks on session traces: `skill_used` (Skill call or typed /command), `tool_called`, `tool_not_called`, `order`, `max_tool_errors`, `max_calls`, `no_error_matching`, `finished`.
- Every case runs twice (`--repeat`); the share of verdicts that flip is the noise band, and only a drop larger than it is a regression. Golden and critical cases stay strict. 70–90% is the target band; above 90% is flagged as too easy.
- `intake.py`: candidate cases from real Claude Code sessions, from log-papercut issues or queue, and from agent PRs that were rejected or edited by people.
- `ablation.py`: blind with-versus-without (or part-removed) comparison, Wilson 95% interval, noise band from two identical arms, and tool-call, error and duration means per arm.
- SKILL.md passes tune-skill's new `check_skill.py --lint`: ten numbered steps, each with a command and a result check, and an error recovery table.
- `tests/test_scripts.py`: 39 checks, all passing.

## 0.1.0 — 2026-11-24

First version: golden set, invariants, scorer with baseline, trace reader.

# Trigger test cases

Judged by hand from the descriptions of skill-eval-suite, tune-skill, harness-audit and log-papercut as they stand, and from the planned one-line scope of loop-schedule (not yet written). Not run in a live agent.

| # | Message | Expected skill | Pass condition | Hand result |
| --- | --- | --- | --- | --- |
| 1 | "Build me a golden set for my nightly SEO report so I know if it's any good" | skill-eval-suite | proposes a case table and waits before writing `evals/` | pass |
| 2 | "Write evals for the inbox-sweep loop" | skill-eval-suite | reads the loop's prompt and real outputs first | pass |
| 3 | "I need a scorecard that fails if the weekly digest gets worse after I change the prompt" | skill-eval-suite | saves a baseline; `score.py` exits 1 on regression | pass |
| 4 | "My scheduled competitor check reported nonsense last night, why?" | skill-eval-suite | runs `traces.py` and classifies with the taxonomy before suggesting a fix | pass |
| 5 | "How do I know this agent is right more often than not?" | skill-eval-suite | implicit; offers a golden set rather than an opinion | pass |
| 6 | "Make my seo-sweep skill run every morning and only report" | loop-schedule | skill-eval-suite does not trigger | pass |
| 7 | "The nightly job didn't run on Tuesday" | loop-schedule | skill-eval-suite does not trigger (taxonomy class 1 hands off here) | pass, closest call: "why did the run fail" is shared; "didn't run" decides it |
| 8 | "My recruiter-lens skill doesn't trigger when I ask about my CV" | tune-skill | skill-eval-suite does not trigger | pass |
| 9 | "Claude keeps making the same mistake across sessions, which rule is missing?" | harness-audit | skill-eval-suite does not trigger | pass |
| 10 | "Run lm-evaluation-harness on Llama for MMLU" | none | shares "eval harness"; this skill evaluates agent loops, not model benchmarks | pass by description; the name invites this miss |
| 11 | "Is the new prompt for my weekly digest actually better, or did I just get a lucky run?" | skill-eval-suite | runs 3 trials and reports flips, not one pass rate | pass |
| 12 | "My triage agent got cheaper but I think it now opens tickets it shouldn't" | skill-eval-suite | adds `must_not` cases and checks the token bill and flips together | pass |
| 13 | "Check whether our LLM judge can be trusted before we gate PRs on it" | skill-eval-suite | runs `--expect-fail` on the known-bad set and a 30+ sample calibration | pass |
| 14 | "Log that the deploy tool rejected --since even though the help lists it" | log-papercut | skill-eval-suite does not trigger | pass |

## Boundary pairs

| Message | Should trigger | Why |
| --- | --- | --- |
| "Is my daily report actually correct?" | skill-eval-suite | quality of what ran |
| "Did my daily report run?" | loop-schedule | whether it ran |
| "Write test cases for when my skill should fire" | tune-skill | triggering, not output quality |
| "Write test cases for what my skill's report must contain" | skill-eval-suite | output quality |
| Spanning: "Schedule this skill nightly and give it a quality bar" | loop-schedule → skill-eval-suite | schedule first; skill-eval-suite needs real outputs to build cases |

## Script tests (run)

`python -I tests/test_scripts.py`: 60 checks, all passing on 2026-11-24. Covers:

- **score.py:** tier mix and intent coverage; pending and author-only verdicts; new cases held until 3 trials and critical ones until 5; flaky cases and the noise band; fixed and broke reported as a trade-off; a single clear loss warning and a repeated one blocking; golden and critical strictness; the token budget failing correct runs; `max_tokens`; the free path; the hidden holdout leaking no ids and flagging overfitting; a known-bad set catching skills-site#24's repeated nightly report and marking a weak check untrusted; trajectory checks, slash-command skill use, per-file dedup and unusable suites.
- **pipeline gates:** duplicate PR work, an untrusted issue source and a diff outside the spec are each caught with evidence; the good outputs pass; unreadable output fails with a reason.
- **token windows:** a repeated message id counts once at its final usage, a typed /command and a Skill call each open a window, windows add up to the total, subagent tokens split out, peak context, and the `skill_tokens` and `max_context` checks.
- **intake.py:** sessions found by Skill call and by slash command, with prompts masked; agent PRs split into rejected and edited, with the reviewer's words in the rubric; papercuts grouped from GitHub issues and from the queue.
- **ablation.py:** blind pairs with the key kept outside the folder, randomised order, the win share with its noise band, and trace stats per arm.
- **traces.py:** tool calls, errors, denials, endings, masking, plain logs.

`traces.py` and the trajectory checks were also run on a real Claude Code session, including its token usage (12.8M tokens, mostly cache reads).

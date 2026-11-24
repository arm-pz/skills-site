# Trigger test cases

Judged by hand from the descriptions of eval-harness, tune-skill and harness-audit as they stand, and from the planned one-line scope of loop-schedule (not yet written). Not run in a live agent.

| # | Message | Expected skill | Pass condition | Hand result |
| --- | --- | --- | --- | --- |
| 1 | "Build me a golden set for my nightly SEO report so I know if it's any good" | eval-harness | proposes a case table and waits before writing `evals/` | pass |
| 2 | "Write evals for the inbox-sweep loop" | eval-harness | reads the loop's prompt and real outputs first | pass |
| 3 | "I need a scorecard that fails if the weekly digest gets worse after I change the prompt" | eval-harness | saves a baseline; `score.py` exits 1 on regression | pass |
| 4 | "My scheduled competitor check reported nonsense last night, why?" | eval-harness | runs `traces.py` and classifies with the taxonomy before suggesting a fix | pass |
| 5 | "How do I know this agent is right more often than not?" | eval-harness | implicit; offers a golden set rather than an opinion | pass |
| 6 | "Make my seo-sweep skill run every morning and only report" | loop-schedule | eval-harness does not trigger | pass |
| 7 | "The nightly job didn't run on Tuesday" | loop-schedule | eval-harness does not trigger (taxonomy class 1 hands off here) | pass, closest call: "why did the run fail" is shared; "didn't run" decides it |
| 8 | "My recruiter-lens skill doesn't trigger when I ask about my CV" | tune-skill | eval-harness does not trigger | pass |
| 9 | "Claude keeps making the same mistake across sessions, which rule is missing?" | harness-audit | eval-harness does not trigger | pass |
| 10 | "Run lm-evaluation-harness on Llama for MMLU" | none | shares "eval harness"; this skill evaluates agent loops, not model benchmarks | pass by description; the name invites this miss |

## Boundary pairs

| Message | Should trigger | Why |
| --- | --- | --- |
| "Is my daily report actually correct?" | eval-harness | quality of what ran |
| "Did my daily report run?" | loop-schedule | whether it ran |
| "Write test cases for when my skill should fire" | tune-skill | triggering, not output quality |
| "Write test cases for what my skill's report must contain" | eval-harness | output quality |
| Spanning: "Schedule this skill nightly and give it a quality bar" | loop-schedule → eval-harness | schedule first; eval-harness needs real outputs to build cases |

## Script tests (run)

`python -I tests/test_scripts.py`: 22 checks, all passing on 2026-11-24. Covers pending judge checks, baseline save and refusal on regression, critical cases, missing outputs, `match: "*"` invariants with per-file dedup, unusable case files, bad regexes, and trace parsing of a session with a 403, a permission denial, a max-turns ending and masked secrets. `traces.py` was also run on a real Claude Code session file.

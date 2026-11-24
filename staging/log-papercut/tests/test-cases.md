# Trigger test cases

Judged by hand from the descriptions of log-papercut, skill-eval-suite and harness-audit. Not run in a live agent. Most triggers happen mid-task, with no user message asking for a report, which a hand check cannot fully simulate.

| # | Situation | Expected skill | Pass condition | Hand result |
| --- | --- | --- | --- | --- |
| 1 | Deploy skill says seconds, API wants milliseconds; worked around | log-papercut | files with `--fix` naming the skill step, then finishes the deploy | pass |
| 2 | `gh pr checks` exits 0 with "no checks reported" on a repo with CI | log-papercut | severity `slowed`, `--error-pattern` set | pass |
| 3 | A skill reference points at a missing script | log-papercut | `--tool none`-style report against the skill, fix names the path | pass |
| 4 | User: "File a papercut for the flaky crawl timeout" | log-papercut | runs `list` first, then `file` | pass |
| 5 | Third attempt at the same MCP auth error | log-papercut | "keep fighting the same error" signal | pass |
| 6 | "My app's login form throws a 500, fix it" | none (the task) | no papercut: the user's own code | pass |
| 7 | Own typo in a bash command | none | no papercut: not friction in a skill or tool | pass, closest call: an error in a tool call; the Ground rules decide it |
| 8 | "Is my nightly report any good?" | skill-eval-suite | log-papercut does not trigger | pass |
| 9 | Same mistake across sessions | harness-audit | log-papercut does not trigger | pass |
| 10 | "Open a GitHub issue for the bug in our checkout page" | none | a bug report about the user's product, not agent friction | pass by description |

## Script tests (run)

`python -I tests/test_papercut.py`: 15 checks with a fake `gh` on PATH, all passing on 2026-11-24. Covers the local queue, grouping by fingerprint across different numbers and paths, masking of tokens and home paths, refusal of "try again", bad severity and bad regex, creating a GitHub issue with the JSON record and marker, commenting on an existing open issue, creating the missing label once, and `list` merging queue and GitHub records. No real issue was filed.

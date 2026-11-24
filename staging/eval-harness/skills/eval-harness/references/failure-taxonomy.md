# Failure taxonomy: reading a trace back to a cause

Open this at step 10, with the output of `traces.py` and the failing checks. Go top to bottom; the first class whose evidence matches is the cause. Lower classes are often symptoms of a higher one.

| # | Class | Evidence in the trace | Smallest fix | Owner |
| --- | --- | --- | --- | --- |
| 1 | **Did not run, or ran partly** | No session for the slot; `end` is `error_max_turns` or `error_during_execution`; no final text | Fix schedule, turn limit or the run-happened check | `loop-schedule` |
| 2 | **Bad input** | Fetch tool calls errored or returned empty; fixture missing; auth 401/403 in a tool result | Fix the fixture, credential or source; add an `edge` case for the empty input | this skill, or the user for credentials |
| 3 | **Tool failure** | `tool_errors` > 0 or `permission_denials` > 0 on a step the output depended on | Allow the tool, fix its arguments in the prompt, or add a fallback step | loop owner; `harness-audit` if it recurs across loops |
| 4 | **Instruction missed** | Inputs and tools fine; the output breaks a rule the prompt states plainly | Move the rule up, make it a numbered step, or make the output format enforce it | loop prompt / skill body |
| 5 | **Wrong judgement** | The right facts are in the tool results; the conclusion is wrong | Add a worked example of this case to the skill; split the decision into a check the loop runs itself | loop prompt / skill body |
| 6 | **Wrong skill or none** | The trace shows another skill loaded, or no skill at all | Description and boundaries | `tune-skill` |
| 7 | **Grader wrong** | Output is right by the user's judgement; the check or rubric says fail | Fix the check; log the change in `failures.md` so the score drop is explained | this skill |
| 8 | **Flaky** | The case's trials split (2 of 3, 3 of 5) | Keep the case, run more trials, count it in the noise band, not as a flip. If more than 20% of cases are flaky, lower variance (fixed order, explicit format, lower effort tier) before tuning anything else | loop prompt |

## Friction an agent already reported

Before classifying, check `gh issue list --label papercut --search "<tool>"` (or `papercut.py list --tool <tool>`). A matching papercut is evidence for class 2 or 3 and usually names the fix. Link it in the `failures.md` entry, and once the fix lands the case you add in step 11 is that papercut's regression case.

## Reading order in the trace

1. `end` and `final_text`: did it finish and say anything?
2. `tool_errors` and `permission_denials`: anything that broke before the model decided?
3. The tool call list in order: did it read what the case's fixture holds?
4. Only then the model's text: where did the reasoning leave the evidence?

## `failures.md` entry

```
## <date> <case-id> — <class>
Check failed: <type> <value>
Trace: <file>, <the one or two lines that prove the class>
Fix: <what changed, in which file>
Papercut or PR: <link, if any>
Case added: <regression case id, or "existing case">
Known-bad added: <evals/known-bad entry id for this failed output>
Re-score: <exit code, pass rate before → after>
```

Do not quote more of a trace than the entry needs, and never quote a value `traces.py` masked.

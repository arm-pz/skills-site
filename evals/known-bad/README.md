# Known-bad set

Outputs that are wrong on purpose. Every check, judge rubric or gate must **fail every entry here**
before it is trusted to gate anything (EDD: "every metric must fail the known-bad set before it gates").

    python <eval-harness>/scripts/score.py evals/known-bad/known-bad.jsonl evals/known-bad/outputs --previous evals/known-bad/previous --expect-fail

Exit 0 = caught all (trusted), 1 = a bad output passed (untrusted: fix the check), 2 = a judge has not graded yet.
To test a judge, copy its rubric into an entry's `checks` and have it grade `outputs/` blind, mixed in with real outputs.

Grow it from real failures: every failed run you diagnose adds its output (or trace) here. About ten makes a strong set.

## Entries

| id | source | why it is bad | status |
| --- | --- | --- | --- |
| kb-001-health-repeat | [skills-site#24](https://github.com/arm-pz/skills-site/issues/24) | the nightly health issue repeated the same items for days | seeded, caught by `not_in_previous` |
| kb-002 | "#24 vs #26" | to fill: which outputs, and why they are bad | **needs content from the owner** |
| kb-003 | off-spec files | to fill: example files that break the spec | **needs content from the owner** |
| kb-004 | stranger issues | to fill: issues the pipeline should not act on | **needs content from the owner** |

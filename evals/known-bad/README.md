# Known-bad set

Outputs that are wrong on purpose. Every check, judge rubric or gate must **fail every entry here**
before it is trusted to gate anything ("every metric must fail the known-bad set before it gates").
Each entry also has a **control**: a correct output the same check must pass, so a check that fails
everything cannot look trustworthy.

Run both from the repo root (`score.py` is eval-harness's, at `staging/eval-harness/skills/eval-harness/scripts/` until it has its own repo):

    python score.py evals/known-bad/known-bad.jsonl evals/known-bad/outputs --previous evals/known-bad/previous --expect-fail
    python score.py evals/known-bad/known-bad.jsonl evals/known-bad/controls --repeat evals/known-bad/controls --repeat evals/known-bad/controls --previous evals/known-bad/controls-previous

The first must exit 0 ("caught 4 of 4: trusted"); exit 1 names a bad output a check let through. The
second must exit 0 (every control passes; the folder is passed three times because a new case needs
three trials and these checks are deterministic).

To test a judge, put its rubric in an entry's `checks` and have it grade `outputs/` blind, mixed in with
real outputs. Grow the set from real failures: every failed run you diagnose adds its output here.
About ten make a strong set.

## Entries

| id | kind | source | what is wrong | gate that must fail it |
| --- | --- | --- | --- | --- |
| kb-001-duplicate-pr-work | real | arm-pz/caffeinity-skills #24 vs #26, 2026-11-22 | triage picked "add trigger cases for the four search-visibility skills" while open PR #24 already covered them; #26 merged and #24 conflicted | `triage_skips_open_pr` |
| kb-002-repeated-report | real | arm-pz/skills-site #24, nightly comments of 2026-11-19 and 2026-11-20 | the loop re-posted an unchanged finding | `not_in_previous` |
| kb-003-off-spec-diff | synthetic | — | the diff touches `scripts/build_evals.py`, outside the spec's Files list | `diff_within_spec` |
| kb-004-stranger-issue | synthetic | — | triage selected #32, opened by a non-owner without `pipeline-ok` | `triage_trusted_source` |

## Layout

```
known-bad.jsonl        entries: id, source, why, the checks under test
outputs/               the bad outputs (triage JSON, report, diff)
previous/              the run before, for not_in_previous
context/               what the gates read: open PRs, the spec, the issue list
controls/              a correct output per entry
controls-previous/     the run before each control
```

Triage output format the gates read: `{"selected": [{"issue": 23, "title": "...", "files": [...], "covers": [...]}], "dropped": [...]}`.

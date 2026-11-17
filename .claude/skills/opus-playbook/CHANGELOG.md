# Changelog

## 0.1.1 (2026-11-17)
- Made the text worker-neutral and runtime-neutral: Opus is the usual case, not a requirement;
  step 0 no longer names one runtime's tools; hand-offs to other skills are optional.
- No change to the description, so the trigger cases stand as recorded.

## 0.1.0 (2026-11-17)
- Initial release, drafted from an idea (no prompt list): how a lead model checks that work
  handed to Opus does the job that was asked.
- Tests: 10 trigger cases, 0 pass by execution, 0 fail, 10 reviewed-only (hand-read against the
  descriptions), 0 not run.
- `scripts/worker_diff.py` executed against a planted repository: 7 of 7 problems reported.
- Not yet used on a real hand-off to Opus.

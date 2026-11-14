# Claim check

Open when a claim is hard to judge in stage 3.

- **Supported:** the diff contains the code path, and nothing disables it (flag off by default, dead branch, test-only).
- **Partly supported:** works for a subset ("exports to CSV" but only for one screen), or sits behind a flag or config. Reword to the true scope and say so.
- **Not found:** nothing in the diff does it. The changelog may describe planned work or something merged before the tag. Remove it or ask the user.
- Tests, docs and comment changes alone do not support a feature claim.
- Version bumps and dependency updates are not features unless the changelog says users see a difference.
- If the diff is too large to read fully, check claims against the file list and stat first, read the relevant files, and state which claims were only checked at that level.

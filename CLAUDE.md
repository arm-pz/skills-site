## pr-merge-gate

When asked to “review and merge the open PRs”, list the open pull requests and process dependencies first. Run `consistent-code-review` on each PR diff and record the reviewed head SHA and findings.

Squash-merge a PR only when all four conditions hold at merge time:

- The review has zero CRITICAL and zero HIGH findings.
- CI is green for the reviewed head. Wait for pending checks. This repo's `check` job must pass. Its deployment `publish` job is expected to skip on pull requests.
- GitHub confirms the PR merges without conflicts into its current base.
- The PR has no `hold` label.

After a dependency lands, rebase dependent work as needed and re-review the updated diff. Preserve published history and never force-push. If the head changes, repeat the review and CI checks. Mark eligible drafts ready for review and squash-merge with `--match-head-commit` set to the reviewed SHA.

Leave held PRs open. Post a summary grouped by **merged**, **held**, and **needs-fix**, with the reason for each decision and any non-blocking findings.

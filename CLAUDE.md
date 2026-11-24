## pr-merge-gate

For adoption in other repositories, see [the reusable PR graph](tools/pr-graph/README.md).

When asked to “review and merge the open PRs”, run the **pr-graph** skill (`.claude/skills/pr-graph/SKILL.md`). It reviews each open PR with `consistent-code-review` in a fresh `pr-reviewer` subagent, fixes CRITICAL and HIGH findings with `address-findings` in a `pr-fixer` subagent, re-reviews them, and loops at most 3 rounds.

Only `tools/pr-graph/merge_gate.py <pr> --review <review-report.json> --merge` may merge. Never merge by calling the API or `gh pr merge` directly. The gate squash-merges, pinned to the reviewed head SHA, only when all of these hold:

- The review is for the current head and has zero CRITICAL and zero HIGH findings.
- CI is green for that head. This repo's `check` job must succeed. Its deployment `publish` job is expected to skip on pull requests.
- GitHub confirms the PR merges without conflicts into its current base.
- The PR has none of the merge-blocking labels: `hold`, `hands-off`, or `needs-owner`. A PR on `hold` still receives review, fixes, and re-review. Skip all work on PRs carrying `hands-off` or `needs-owner`, including when they also carry `hold`.
- The diff touches no protected path: `.github/`, `.claude/`, `tools/pr-graph/`, `CLAUDE.md`, or the gate's own tests. Those changes are always merged by a human.

After a merge, re-check the remaining PRs. Any whose head or base changed go back to review. Preserve published history and never force-push. Leave held PRs open. Post a summary grouped by **merged**, **held** and **needs-owner**, with the gate's reasons for each.

When a bad PR gets past the gate, add it to `KNOWN_BAD` in `tools/agent-skills/tests/test_merge_gate.py` before fixing anything else.

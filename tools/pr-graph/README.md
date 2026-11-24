# PR graph for GitHub repositories

The agent workflow reviews each open PR, fixes blocking findings on its head branch, requests a fresh review and calls the merge gate. Install the graph into a target checkout from a trusted revision of this repository:

```sh
python tools/pr-graph/install.py /path/to/target
```

Review and commit the installed files in the target. Install the [consistent-code-review skill](https://github.com/arm-pz/consistent-code-review) in the agent environment. The conductor needs an agent runner that supports fresh subagents, Python 3, Git and an authenticated GitHub CLI. In the target checkout, ask the agent to **run the pr-graph skill on the open PRs**. Use a trusted checkout of the graph and put proposed changes in separate worktrees. Keep local run records under `.pr-graph/runs/` out of commits.

The default required CI check is `check`. For other names, commit a policy on the target base branch, for example `.github/pr-graph.json`:

```json
{"required_checks": ["build", "unit tests"]}
```

Create the target’s `hold`, `hands-off` and `needs-owner` labels during adoption. Use the exact job or status context names in the policy. Missing required results block merging. The gate checks all observed runs and statuses, including when working remotely with `--repo OWNER/REPO`. The report must identify the same base repository, PR, head SHA, base branch and base SHA. Regenerate legacy reports before using the portable gate.

### GitHub Actions integration

A trusted manual or scheduled default-branch workflow may call the shared merge gate after its agent review job produces the JSON report. The caller must already have installed the graph. The caller controls the schedule, runner for the agent nodes and permissions. Use the following job in that workflow, replacing `PINNED_SHA` with a revision containing this workflow:

```yaml
jobs:
  # review is your agent job; its report output contains trusted reviewer JSON.
  gate:
    needs: review
    permissions:
      contents: write
      pull-requests: write
      checks: read
      statuses: read
    uses: arm-pz/skills-site/.github/workflows/pr-graph.yml@PINNED_SHA
    with:
      pr: ${{ fromJSON(needs.review.outputs.pr) }}
      review: ${{ needs.review.outputs.report }}
      merge: false
```

Set `merge: true` to request a squash merge after all checks pass. Pass review output directly from the trusted agent job. PR descriptions, comments and files in the proposed diff are untrusted inputs. The gate uses the caller's token and checks the target base's policy. Repository rules and token permissions still apply.
### Run the whole graph in Actions

The callable workflow above evaluates a completed review. To run the conductor, reviewer, fixer, re-review and gate together, use this caller on the target's default branch:

```yaml
name: Run PR graph
on: workflow_dispatch
jobs:
  run:
    permissions:
      contents: read
    uses: arm-pz/skills-site/.github/workflows/pr-graph-run.yml@PINNED_SHA
    secrets:
      graph_token: ${{ secrets.PR_GRAPH_TOKEN }}
```

Provide an ephemeral Linux runner labelled `pr-graph` with authenticated Claude Code, its consistent-code-review skill, Git, Python, GitHub CLI, and the target's build tools. Configure the agent's noninteractive tool permissions for the installed nodes. The reviewer and fixer should run candidate code and tests in an isolated environment without the agent's credentials. Configure Git authentication for the fixer's branch pushes. Supply a caller-scoped, unexpired GitHub App installation token with contents, issues and pull-request write access and checks/statuses read access. A GitHub App token allows a pushed fix to trigger the target's normal CI. The workflow publishes the final scorecard in the Actions job summary. Interactive runs in an agent checkout work without this Actions runner.

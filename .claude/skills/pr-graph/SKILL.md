---
name: pr-graph
description: Run the shared PR Graph conductor against this repository's open pull requests.
---

# PR Graph

Use the standalone [PR Graph distribution](https://github.com/arm-pz/pr-graph). The exact trusted revision is the `graph_revision` in `.github/workflows/pr-graph-run.yml` on the target's default branch. Fetch that revision into a separate local checkout, verify its HEAD equals the pin, and use it as `PR_GRAPH_HOME`. Keep this repository as `PR_GRAPH_TARGET`.

Read the conductor at `$PR_GRAPH_HOME/.claude/skills/pr-graph/SKILL.md`. Use the skills, agent definitions, report schemas and gate from that distribution. Run the graph against this repository and return its scorecard.

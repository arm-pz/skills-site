## pr-merge-gate

For requests to review and merge open PRs, run the `pr-graph` skill in this checkout. It loads the revision of the standalone [PR Graph](https://github.com/arm-pz/pr-graph) pinned in the manual [workflow](.github/workflows/pr-graph-run.yml). Use that distribution's gate for squash merges and report the graph's scorecard.

The required CI job here is `check`. The local baseline is `python -m unittest discover -s tools/agent-skills/tests`, followed by `--check` on each of `gen_home.py`, `gen_page.py`, and `gen_runs.py` under `tools/agent-skills/`.

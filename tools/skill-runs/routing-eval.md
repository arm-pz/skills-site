# Controlled routing eval

Does installing `caffeinity-routing` improve workflow recommendations in Claude Code? Both arms get the same task, catalog snapshot, model and local skill inventory. The router arm also gets `caffeinity-routing`. There are four cases and three repeats for each arm, for 24 fresh sessions. The first arm alternates between repeats. The tasks request a plan and the runner limits tools to reading the local project and checking its inventory.

The cases cover publishing and discovery, the same goal phrased differently, a request that one skill owns, and a workflow with a mix of installed and missing skills. The program scores workflow order, inventory accuracy and required approvals separately. It records router activation from the Skill tool trace. Mentioning the router in an answer does not count as activation. The near-miss expects no router activation.

From the repository root, with Git, Python, Node.js and an authenticated Claude Code CLI:

```sh
python tools/skill-runs/routing_eval.py --list
python tools/skill-runs/routing_eval.py --model sonnet --output routing-results.jsonl
```

Use a full model ID where available. The runner records the resolved model and the skill commits used. The default ceiling is $0.25 per session, or $6 across the matrix at the CLI's reported rates. For a smoke test, add `--case mixed-inventory --repeats 1`. Use a new output file for each attempt.

The JSONL file starts with the run settings. Each subsequent row contains the case, arm, repeat, answer, scores, model and cost. A session that cannot produce a result stops the run and leaves the completed rows in the file. Compare matched pairs for each metric. Report the count of cases that pass on every repeat as well as the per-run numbers. Keep activation separate from the outcome scores, and check that all 24 runs used the same resolved model before interpreting differences. Installing the router is the only planned difference between arms. Results describe these fixtures on the tested Claude Code version. Codex needs its own adapter and activation evidence before comparison.

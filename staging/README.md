# staging

Skills drafted here before they get their own repo. Nothing in this folder is deployed: `make_dist.sh`
copies only the static pages and generated skill pages, and `sync.py` reads skills from `arm-pz/<name>`
repos, not from here.

To publish one: create the public repo `arm-pz/<name>`, copy `staging/<name>/` to its root, set the repo
About, push. The hourly sync picks it up. Then delete the folder here.

| Folder | Ladder level | Status |
| --- | --- | --- |
| `eval-harness/` | 3 | 0.3.0, drafted 2026-11-24: Uber's suite mix plus EDD gates; 49 script checks pass; not yet run on a real loop |
| `log-papercut/` | 3 (feeds it) | 0.1.0, drafted 2026-11-24: always-on friction reports; 15 script checks pass with a fake `gh` |

`evals/known-bad/` at the repo root is this site's own known-bad set, seeded from skills-site#24.

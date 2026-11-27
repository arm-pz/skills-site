# staging

Skills drafted here before they get their own repo. Nothing in this folder is deployed: `make_dist.sh`
copies only the static pages and generated skill pages, and `sync.py` reads skills from `arm-pz/<name>`
repos, not from here.

To publish one: create the public repo `arm-pz/<name>`, copy `staging/<name>/` to its root, set the repo
About, push. The hourly sync picks it up. Then delete the folder here.

| Folder | Ladder level | Status |
| --- | --- | --- |
| `skill-eval-suite/` | 3 | 0.4.0, drafted 2026-11-24 (first named eval-harness, renamed to avoid collisions): Uber suite mix, EDD gates, pipeline gate checks, per-skill token windows; 60 script checks pass; not yet run on a real loop |

`evals/known-bad/` at the repo root is this site's own known-bad set, with four entries (two real incidents, two synthetic) and a control for each.

`discovery/` holds the findable kit for skill-eval-suite and log-papercut (log-papercut is now published as arm-pz/log-papercut, so its folder is gone from here): About text, topics, release notes, site pages, distribution list and the commands to publish them.

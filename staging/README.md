# staging

Skills drafted here before they get their own repo. Nothing in this folder is deployed: `make_dist.sh`
copies only the static pages and generated skill pages, and `sync.py` reads skills from `arm-pz/<name>`
repos, not from here.

To publish one: create the public repo `arm-pz/<name>`, copy `staging/<name>/` to its root, set the repo
About, push. The hourly sync picks it up. Then delete the folder here.

| Folder | Ladder level | Status |
| --- | --- | --- |
| `eval-harness/` | 3 | drafted 2026-11-24; scripts tested, not yet run on a real loop |

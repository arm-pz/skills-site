I wrote the rules file for `site-src/` but did not add any guardrails, because none of the three fit this repo. Nothing is committed or pushed; the two new files are untracked in site-src's own git repo.

**Rules**
- `AGENTS.md` has the 12 rules unchanged at the top, then one line with the test command and a pointer to `PROJECT.md`.
- `CLAUDE.md` contains only `@AGENTS.md`, so Claude Code and Codex read the same file.
- There was no instruction file before, so there were no rule conflicts to resolve.
- I did not show you the diff before writing, which the skill asks for. They are new files, so there is nothing to overwrite.

**Map sections:** none written yet. This step needs your answer: where does the agent keep getting things wrong here? Likely candidates:
- Generated pages. `gen_page.py` rewrites the region between the `<!-- gen:quality:start -->` and `<!-- gen:quality:end -->` markers on every page.
- `site/skills.json`. It is the single skill inventory, and the hub, indexes, sitemap and pages are all generated from it.
- The `deploy` branch and `dist/`. The CI workflow publishes them, and nobody should edit them by hand.
- Bespoke pages versus generated pages.

**Guardrails**
- **Type check, new errors only:** not possible. The repo is Python and Node with no type checker configured (no mypy, pyright or tsconfig), and I didn't invent one.
- **Live-service tests opt-in:** not needed. The 102 unit tests stub out the `gh` calls, and the `test_discover.py` and `test_sync.py` ones I checked do. The one skip is `test_tool_cores.py`, which skips when `node` is missing. I tagged nothing.
- **Tests before deploy from main:** already present. In `publish.yml`, the publish job runs the unit tests, generated-surface checks, build, `check_dist.py` and `verify.mjs` before it commits to main or pushes the `deploy` branch. It also uses `set -o pipefail` where it pipes.

**Run:** the unit test suite passed locally (102 tests, OK). I did not run the CI workflow itself.

**Next step:** after the agent's next big change here, run `consistent-code-review` on it.
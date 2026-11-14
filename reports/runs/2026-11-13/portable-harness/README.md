# portable-harness: real-world run, 2026-11-13

**Verdict: PARTIAL** (6/10). The run wrote site-src/AGENTS.md (12 rules at top, test command, pointer to PROJECT.md) and a CLAUDE.md containing '@AGENTS.md', and ran the repo's unittest suite (102 tests OK), but wrote no map sections and installed no guardrail.

Target: the skillsmith.tech source repo (local clone). Run headless on the CLI default model in a clean project with only this skill installed (10 turns, 8 tool calls, 26 s, $0.36).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Set up site-src/ so any coding agent behaves the same in it. Write the rules file and add guardrails where they earn their place. Local only.
```

## Rubric

- Writes the working rules at the top of CLAUDE.md/AGENTS.md
- Adds map sections only where grounded in the repo (e.g. generated pages vs sources, the deploy branch)
- Any guardrail it installs actually runs here (e.g. the repo's unittest suite) and it shows it running
- Invents no commands the repo does not have

## Hard checks

- ✓ a CLAUDE.md or AGENTS.md was written

## Met

- Working rules are at the top of AGENTS.md, with CLAUDE.md importing it via @AGENTS.md so both agents read the same file
- The test command listed (python3 -m unittest discover -s tools/agent-skills/tests) exists in the repo and was run, passing 102 tests
- Invented no commands: type checking was declined because no checker is configured, and the listed commands come from PROJECT.md/publish.yml
- The existing CI gate in publish.yml was correctly identified as already covering tests before deploy

## Missed

- No map sections were written, even though the repo grounds several (generated pages vs hand-written pages, the gen:quality markers, site/skills.json as the single inventory, the deploy branch); the run asked the user instead of writing them
- No guardrail was installed: the 'tests before deploy' guardrail was judged already present in CI and nothing local (hook or similar) was added or shown running as a guardrail
- The run admits it skipped the skill's step of showing the diff before writing

## Defects to fix in the skill

- The skill makes the map section depend on a user answer ('where does the agent keep getting things wrong?'), so a run with no interactive reply writes no map even when the repo plainly grounds one; it should default to writing grounded maps from PROJECT.md and the generator markers
- The skill gives no fallback for when every guardrail is already covered by CI; it should say to install the local equivalent (for example a pre-push check running the unittest suite) and show it running
- The 'show the diff before writing' step conflicts with a non-interactive one-shot request and was skipped; the skill should say what to do for new files

## What it did

1. `Skill: portable-harness`
1. `Bash: cd /tmp/run-portable-harness-s2hx3un5/project; ls -la; ls site-src; cat CLAUDE.md AGENTS.md site-src/CLAUDE.md site-src/AGENTS.md 2>&1 | head -50; ls .claude/sk`
1. `Bash: cd /tmp/run-portable-harness-s2hx3un5/project; cat .claude/skills/portable-harness/references/*.md; cd site-src; cat PROJECT.md DIRECTORIES.md | head -60; ls -a`
1. `Bash: cd /tmp/run-portable-harness-s2hx3un5/project/site-src; git status --short | head; ls .github/workflows tools site .reviews 2>&1 | head -60; cat .gitignore; ls `
1. `Bash: cd /tmp/run-portable-harness-s2hx3un5/project/site-src; cat .github/workflows/publish.yml | head -120; ls tools/agent-skills tools/fx | head -50; cat tools/fx/p`
1. `Bash: cd /tmp/run-portable-harness-s2hx3un5/project/site-src; ls tools/agent-skills/tests; grep -lnE "urllib|requests|subprocess|\bgh\b|network|skipUnless|skip\(" too`
1. `Bash: cd /tmp/run-portable-harness-s2hx3un5/project/site-src; python3 -m unittest discover -s tools/agent-skills/tests 2>&1 | grep -E "^(Ran|OK|FAILED|FAIL:|ERROR:)";`
1. `Bash: cd /tmp/run-portable-harness-s2hx3un5/project/site-src; python3 - <<'E'
import re
r=open('../.claude/skills/portable-harness/references/rules.md').read()
block=`

## Files it wrote

Copied under `files/`:

- `site-src/.gitattributes`
- `site-src/.github/workflows/health.yml`
- `site-src/.github/workflows/publish.yml`
- `site-src/.gitignore`
- `site-src/.reviews/3f3dc796540e.md`
- `site-src/.well-known/skills.json`
- `site-src/404.html`
- `site-src/AGENTS.md`
- `site-src/CLAUDE.md`
- `site-src/DIRECTORIES.md`
- `site-src/LICENSE`
- `site-src/PROJECT.md`
- `site-src/README.md`
- `site-src/_headers`
- `site-src/ai-team-blueprint/index.html`
- `site-src/applicant-kit/index.html`
- `site-src/application-pilot/index.html`
- `site-src/assets/forge.js`
- `site-src/assets/motion.js`
- `site-src/assets/site.css`
- `site-src/assets/site.js`
- `site-src/assets/skill.css`
- `site-src/assets/stack.js`
- `site-src/assets/tool.css`
- `site-src/assets/tool.js`
- `site-src/caffeinity-routing/index.html`
- `site-src/career-track/index.html`
- `site-src/check/check-core.js`
- `site-src/check/check.js`
- `site-src/check/index.html`
- `site-src/checks/index.html`
- `site-src/choose-effort/index.html`
- `site-src/cold-email-list-gate/index.html`
- `site-src/cold-email-ops/index.html`
- `site-src/consistent-code-review/index.html`
- `site-src/course-builder/index.html`
- `site-src/crash-test/index.html`
- `site-src/data-readout/index.html`
- `site-src/diagnose-usage/index.html`
- `site-src/do-better/index.html`

## Final output

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

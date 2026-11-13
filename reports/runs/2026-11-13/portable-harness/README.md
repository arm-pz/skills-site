# portable-harness: real-world run, 2026-11-13

**Verdict: PARTIAL** (6/10). The run wrote AGENTS.md (12 rules at top) plus a CLAUDE.md containing only @AGENTS.md in site-src/ and ran the existing unittest suite locally (102 tests OK), but wrote no map sections and installed no guardrail of its own.

Target: the skillsmith.tech source repo (local clone). Run headless in a clean project with only this skill installed (10 turns, 8 tool calls, 26 s, $0.19).
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

- Working rules placed at the top of AGENTS.md, with CLAUDE.md importing it via @AGENTS.md so both agents read one file
- Invented no commands: the test command is the repo's own `python -m unittest discover -s tools/agent-skills/tests`, and it declined to invent a type checker
- Ran the unittest suite and showed the result (102 tests, OK)
- Correctly found that the publish workflow already gates deploy on tests and checks, and did not duplicate it
- Hard check met: AGENTS.md and CLAUDE.md were written

## Missed

- Added no map sections, although the repo grounds several (generated pages vs sources via the gen:quality markers, site/skills.json as the inventory, the deploy branch/dist/). It identified them and then asked the user instead of writing them.
- Installed no guardrail; the unittest suite was run but not wired into anything (hook, pre-commit, or documented gate) that the agent would hit, so the 'guardrails where they earn their place' step is effectively unfulfilled.
- Did not show the diff before writing, which the skill asks for (the run admits this).

## Defects to fix in the skill

- The map-section step blocks on a user question ('where does the agent keep getting things wrong?') even when the repo clearly grounds sections like generated vs source files and the deploy branch; the skill should allow writing grounded sections directly in a one-shot request.
- The guardrail step has no fallback for when the existing CI already covers the check; the unittest suite could be installed as a local pre-commit or agent hook and shown running, but the skill leaves this ambiguous.
- The 'show the diff before writing' instruction conflicts with a one-shot local-only task and is not clearly conditional on there being existing content to overwrite.

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

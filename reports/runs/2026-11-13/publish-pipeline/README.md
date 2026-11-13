# publish-pipeline: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). The run read publish.yml, sync.py, discover.py, skilllib.py, build.py, check_dist.py, verify.mjs and health.yml and reported hold reasons and fragile points, but the hard check on audit.md failed and the final message gives no file:line evidence or repo-outside-org hold.

Target: this site's real publish pipeline (read-only audit). Run headless in a clean project with only this skill installed (17 turns, 15 tool calls, 74 s, $0.45).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Audit the publish pipeline in site-src/ (the skillsmith.tech repo). What would make a new skill repo fail to appear on the site, and what's fragile? Don't change anything; write audit.md.
```

## Rubric

- Reads publish.yml, sync.py, build and check scripts before claiming anything
- Names the real hold reasons in sync (missing SKILL.md at the expected path, no LICENSE, empty About, repo outside the org) with file references
- Names real fragile points with file:line evidence
- Invents no behaviour the code does not have
- Changes nothing

## Hard checks

- ✗ wrote audit.md

## Met

- Read publish.yml, health.yml, sync.py, discover.py, skilllib.py (shape_failures), build.py, make_dist.sh, check_dist.py, deploy.sh and verify.mjs before reporting
- Named real shape-test hold reasons: single SKILL.md at an allowed path, LICENSE and README.md at root, name matching folder and repo, single-line description of at most 1024 characters
- Named the empty-About failure, where sync holds the repo and build.py fails if About is blanked later
- Named fragile points that line up with the pre-existing review: prove.py sitemap check that cannot pass, unguarded KeyError aborting the whole hourly run, health.yml pushes not triggering publish
- Flagged inferred claims as inferred (reserved-directory collision not reproduced) and said the .reviews findings may be stale against commit db04809
- Changed no existing files; the only Write was audit.md

## Missed

- Hard check failed: audit.md was written to site-src/audit.md, and the grader's check for audit.md did not pass
- The final message gives no file:line citations, and the audit's content is not shown, so the 'fragile points with file:line evidence' item cannot be confirmed from the transcript
- Did not name 'repo outside the org' as a hold or exclusion reason, so the rubric's list of sync hold reasons is incomplete
- Several claims are inference only (reserved-name collision, sync commit ordering, the shell tool never ran the code), so how much of the audit is verified is unclear
- The run leans on the existing .reviews findings, which are dated 2026-11-02 and were not re-verified against current code

## Defects to fix in the skill

- The skill does not say where audit.md must be written (project root vs site-src/), so the output landed at a path the checker did not accept
- The skill does not require file:line citations for each finding or a final check that every cited line exists, so evidence quality is left to chance
- The skill's list of sync hold reasons is not enforced, so 'repo outside the org' was omitted
- The skill does not require labeling each claim as read-from-code, reproduced or inferred inside audit.md itself

## What it did

1. `Skill: publish-pipeline`
1. `Bash: cd /tmp/run-publish-pipeline-mgj31mi7/project; find . -path ./node_modules -prune -o -path ./.git -prune -o -type f -print | grep -v '^./site-src/.*/dist/' | he`
1. `Bash: cd /tmp/run-publish-pipeline-mgj31mi7/project/site-src; cat .github/workflows/*.yml; cat PROJECT.md DIRECTORIES.md README.md .gitattributes _headers .well-known`
1. `Bash: cd /tmp/run-publish-pipeline-mgj31mi7/project/site-src; cat .github/workflows/publish.yml; echo ======; wc -c PROJECT.md DIRECTORIES.md README.md .well-known/sk`
1. `Bash: cd /tmp/run-publish-pipeline-mgj31mi7/project/site-src; wc -l .github/workflows/publish.yml; sed -n 50,400p .github/workflows/publish.yml`
1. `Bash: cd /tmp/run-publish-pipeline-mgj31mi7/project/site-src; wc -c PROJECT.md DIRECTORIES.md README.md; cat .git/config .gitattributes; ls -a .reviews; ls site tools`
1. `Bash: cd /tmp/run-publish-pipeline-mgj31mi7/project/site-src; ls -la site site/legacy tools/agent-skills tools/agent-skills/tests tools/fx; wc -l tools/agent-skills/*`
1. `Bash: cd /tmp/run-publish-pipeline-mgj31mi7/project/site-src/tools/agent-skills; cat sync.py; sed -n 60,365p discover.py`
1. `Bash: cd /tmp/run-publish-pipeline-mgj31mi7/project/site-src/tools/agent-skills; grep -n "def shape_failures" -A60 skilllib.py; cat build.py make_dist.sh gen_sitemap.`
1. `Bash: cd /tmp/run-publish-pipeline-mgj31mi7/project/site-src/tools/agent-skills; cat check_dist.py deploy.sh verify.mjs; grep -n "STATIC_PAGES\|def redirects\|def arc`
1. `Bash: cd /tmp/run-publish-pipeline-mgj31mi7/project/site-src; grep -n "RESERVED" -B2 -A4 tools/agent-skills/*.py | head -50; sed -n 55,120p .github/workflows/health.y`
1. `Grep: RESERVED|HUB_PAGES|expected =`
1. `Read: /tmp/run-publish-pipeline-mgj31mi7/project/site-src/.github/workflows/health.yml`
1. `Read: /tmp/run-publish-pipeline-mgj31mi7/project/site-src/tools/agent-skills/skilllib.py`
1. `Write: /tmp/run-publish-pipeline-mgj31mi7/project/site-src/audit.md`

## Files it wrote

Copied under `files/`:

- `site-src/.gitattributes`
- `site-src/.github/workflows/health.yml`
- `site-src/.github/workflows/publish.yml`
- `site-src/.gitignore`
- `site-src/.reviews/3f3dc796540e.md`
- `site-src/.well-known/skills.json`
- `site-src/404.html`
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
- `site-src/audit.md`
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
- `site-src/draft-skill/index.html`

## Final output

I've written the audit to `site-src/audit.md` and changed nothing else. It comes from reading the code only: I ran nothing and made no GitHub, Cloudflare or live-site calls. Some claims are inferred from the code, and the audit flags them.

**Why a new skill repo wouldn't appear**
- **Shape test:** it must have exactly one `SKILL.md` in the whole repo, at one of the three allowed paths. It also needs `LICENSE` and `README.md` at root. The frontmatter `name` must match both the folder and the repo name. The description must be a single line of at most 1024 characters.
- **Empty "About":** the sync holds the repo, and `build.py` fails the whole build if the About is later blanked.
- **Mods and bundled skills:** a repo with only a `plugin.json` (a mod) is never auto-added. A skill bundled inside another repo is never discovered either. Both need a manual manifest entry.
- **Name collisions:** names that clash with existing top-level directories (`tools`, `assets`, `site` and similar) aren't on the reserved list, so such a repo would pass the shape test and then write into those directories. This is inferred from the code, not reproduced.
- **Cloudflare:** CI can't see whether the Cloudflare Pages project is connected to the `deploy` branch. If it isn't, the skill lands in git but never reaches the site.

**What's fragile**
- **One bad repo stops everything:** a transient GitHub error or an unguarded `KeyError` on a single repo aborts the whole hourly run for every skill.
- **Sync commit order:** the sync is committed to `main` before the deploy and before live verification. The design says it should happen after.
- **Weak live proof:** `verify.mjs` doesn't check `response.ok` or compare the live index to the built one, and the failed-fetch case is swallowed. `prove.py`'s sitemap check looks like it can never pass.
- **Health commits don't deploy:** `health.yml` pushes with `GITHUB_TOKEN`, so its commits don't trigger `publish` and only reach the site on the next hourly run.
- **Unproven:** I found no evidence that the first publish, the rollback drill or the discovery run ever happened, so the pipeline should be described as unproven.
- **Smaller points:**
  - Wrong tags and group guesses can go live unreviewed.
  - A repo is removed on a single "Not Found" with no grace period.
  - Holds are reported only in the step summary, so nobody is notified.
  - GitHub Actions are pinned by tag rather than by commit SHA.

**Caveats**
- The existing review in `.reviews/` is dated 2026-11-02, against commit `db04809`. The code has since changed (for example, a missing-description guard now exists), so I cite its findings as possibly still present, not confirmed.
- This checkout's git history is shallow, so I couldn't see when each guard was added.

# PROJECT.md: the caffeinity skills ecosystem

What exists, where it lives, how a skill gets from a repo to skills.caffeinity.com and the profile
README, and how the skills keep checking each other. Written 2026-10-23. When this file and a repo
disagree, the repo wins; fix this file.

## The pieces

| Repo | Role |
| --- | --- |
| `arm-pz/<skill>` (one per skill) | The skills themselves: one `SKILL.md` per repo, at `SKILL.md`, `<repo>/SKILL.md` or `skills/<repo>/SKILL.md`. Installed with `npx skills add arm-pz/<repo>`. |
| `arm-pz/skills-site` (this repo) | skills.caffeinity.com: the hub, one page per skill, both discovery indexes, archives, sitemap, and all the automation below. `site/skills.json` is the single list of what is published. |
| `arm-pz/caffeinity-skills` | Claude Code plugin marketplace. Points at the skill repos, and holds the mods (`mods/*`) and `plugins/caffeinity-routing`, the start-here router. |
| `arm-pz/arm-pz` | The GitHub profile README. Its skills block is generated from `site/skills.json`. |
| `arm-pz/ship-sentinel` | A Claude Code mod (no SKILL.md) that holds `git push` and deploys until the check skills have run. Listed on the site as a mod. |
| `arm-pz/outbound-ops`, `arm-pz/prompts-to-skill-agent` | Qoder agent bundles that repackage skills listed from their own repos. Denied in `site/deny.json`, so they never publish twice. |
| `arm-pz/publish-release-gate` | Older single-skill release path (marketplace + tarball). Kept as a pinned legacy archive; superseded by this site's pipeline. |
| `arm-pz/skills-redesign` (private) | Where the manifest pipeline and redesign were built. Merged into this repo on 2026-10-23; nothing there is newer. |
| `arm-pz/skillsmith-inspo` (private) | Design references for the hub (the Intent-style layout). |
| `arm-pz/agent-skill-template` | Copier template (`copier.yml`) for a new skill repo. |

Everything else under arm-pz (apps, sites, forks) has no SKILL.md and is ignored by the pipeline.

**The skill inventory is `site/skills.json`**: name, repo, group, page kind, blurb, and the nine
workflows. Do not copy it into other files; the hub, both indexes, the sitemap, the pages and the
profile README are all generated from it.

## How a skill goes live

```
push a public arm-pz repo with one SKILL.md and a repo About
  └─ within the hour: skills-site  publish.yml  (cron 17 * * * *)
       sync.py --write   add · refresh · rename · remove · hold
       unit tests → build → sitemap + _redirects → dist + version.json → check_dist → verify
       deploy to Cloudflare Pages only if dist/version.json differs from the live one
       verify live → prove live → commit the sync to main as github-actions[bot]
  └─ within the hour: arm-pz/arm-pz  skills-readme.yml  (cron 47 * * * *)
       regenerate the <!-- skills:start --> block of the profile README from site/skills.json
```

| sync action | When | What happens |
| --- | --- | --- |
| add | public, non-fork repo passes the shape test, has an About, is not denied | entry + generated page; group and tag guessed from keywords (fix the guess in `site/skills.json` by hand; sync keeps it) |
| refresh | a generated page's repo HEAD moved | file list, stats, commit and description re-measured; blurb, title and group kept |
| rename | the old repo name now redirects (findable may recommend a rename) | entry, page folder and workflows follow; the old name becomes an alias; `_redirects` 301s the old page and archive URLs |
| remove | GitHub answers Not Found, or the repo went private | entry and generated page dropped. A failed or unreadable API call stops the run instead |
| hold | empty About, failed shape test | reported in the run summary; nothing published |

Bespoke (hand-written) pages are never edited by any of this. After a rename the run summary says
when a bespoke page's copy may still use the old name.

Want it faster than an hour? Give a skill repo a fine-grained token that can dispatch to
`arm-pz/skills-site` and send `repository_dispatch` with `event_type: skill-updated`. Not required.

### Secrets

| Repo | Secret | Needed for |
| --- | --- | --- |
| skills-site | `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` | every deploy (the job fails with that message if missing) |
| skills-site | `PROFILE_DISPATCH_TOKEN` (optional) | refreshing the profile README right after a deploy instead of within the hour |

The profile workflow and the health job use each repo's own `GITHUB_TOKEN`; nothing else is needed.

## How the skills keep each other honest

```
nightly  skills-site  health.yml  (cron 41 3 * * *)
  fetch every published skill at HEAD + tune-skill's scripts at HEAD
  regress.py  =  check_skill.py on every SKILL.md
               + dangling handoffs: "(use X)" where no X exists
               + trigger collisions: two skills quoting the same trigger phrase
  compare with site/health.json
    regression  → one open issue, "Skill health: regressions found", updated nightly
    improvement → site/health.json updated and committed
```

The loop closes by hand or by agent: open the issue, run tune-skill on the skill it names, open a
PR in that skill's repo. When the PR merges, the next night records the improvement. Because the
job pulls tune-skill's scripts at HEAD, an improvement to the checker reaches every skill the next
night. Skills that live elsewhere but are handed off to are listed in `EXTERNAL` in
`tools/agent-skills/health.py`.

To accept an intended change (a new WARN you decided to keep):
`python tools/agent-skills/health.py --accept-all`, then commit `site/health.json`.

## The workflows across skills

Nine routes, defined once in `site/skills.json` (`workflows`) and in
`caffeinity-skills/plugins/caffeinity-routing/skills/caffeinity-routing/references/workflows.md`
(the router's copy, with each step's input and output). They must name the same skills in the same
order; check with `route_check.py`.

| # | Goal | Route |
| --- | --- | --- |
| W1 | Build a skill and make it installable | draft-skill or prompts-to-skill → tune-skill → prompts-to-skill-release → skill-to-mod (optional) |
| W2 | Get a repo, skill or plugin found | findable → publish-pipeline → upstream-check |
| W3 | Decide whether a site is safe to launch | web-preflight → pre-ship-security-red-team → pre-ship-performance-audit → release-gate-chair / -ledger / -validator |
| W4 | Grow organic search traffic | seo-crawl → keyword-guard → wordsmith → pre-ship-performance-audit (optional) |
| W5 | Land a job | recruiter-lens → applicant-kit → application-pilot → career-track (optional) |
| W6 | Make a decision | research-brief → data-readout (optional) → crash-test or do-better → strategy-memo |
| W7 | Learn a skill | topic-primer → study-system |
| W8 | Run cold outbound | cold-email-list-gate → cold-email-ops → sales-copy |
| W9 | Launch a one-person product | solo-income-blueprint → site-prompt → production-code → release-gate-chair → platform-content |

## Adding or changing a skill

1. **New skill:** W1. draft-skill (or prompts-to-skill), then tune-skill, then
   prompts-to-skill-release. Make the repo public, fill in its About. The site picks it up within
   the hour; check the run summary for its guessed group, and move it in `site/skills.json` if needed.
2. **Rename a repo** (findable's name decision): rename on GitHub. The redirect does the rest.
3. **Retire a skill:** delete or privatize the repo, or add it to `site/deny.json` with a reason.
4. **Hand-written page:** set `page: bespoke` and write `<name>/index.html`. Generators never touch it.
5. **Before a push you are unsure of:** `python <tune-skill>/scripts/regress.py <folder-with-your-skills> --baseline health.json`.

## Running it locally

```
python -m unittest discover -s tools/agent-skills/tests     # pipeline tests
python tools/agent-skills/sync.py                           # what sync would change (needs gh auth)
python tools/agent-skills/build.py                          # needs gh auth
python tools/agent-skills/gen_sitemap.py --write
bash tools/agent-skills/make_dist.sh
python tools/agent-skills/check_dist.py && node tools/agent-skills/verify.mjs local
python -m http.server 8080 --directory dist
```

## Known gaps

- `caffeinity-stack` is cited by the three release-gate skills and is not public. If it, or a
  local `caffeinity-routing`, lives only on a PC, run `upstream-check` on that folder: it finds
  unpushed work, and anything pushed here gets picked up by the sync.
- Bespoke pages carry hand-written stats (for example tune-skill's file count) that the sync does
  not refresh. Regenerate or edit them when a skill grows.
- The health job reads SKILL.md files only. Trigger cases are still hand-run; record them in each
  skill's `references/trigger-cases.md` (tune-skill's format) so the next tuner can re-run them.

# PROJECT.md: the caffeinity skills ecosystem

What exists, where it lives, how a skill gets from a repo to skills.caffeinity.com and the profile
README, and how the skills keep checking each other. Written 2026-10-23, updated 2026-10-24. When this file and a repo
disagree, the repo wins; fix this file.

## The pieces

| Repo | Role |
| --- | --- |
| `arm-pz/<skill>` (one per skill) | The skills themselves: one `SKILL.md` per repo, at `SKILL.md`, `<repo>/SKILL.md` or `skills/<repo>/SKILL.md`. Installed with `npx skills add arm-pz/<repo>`. |
| `arm-pz/skills-site` (this repo) | skills.caffeinity.com: the hub, one page per skill, both discovery indexes, archives, sitemap, and all the automation below. `site/skills.json` is the single list of what is published. |
| `arm-pz/caffeinity-skills` | Plugin marketplace for Claude Code (`.claude-plugin/marketplace.json`) and Codex (`.agents/plugins/marketplace.json`). Holds the mods (`mods/*`), `plugins/caffeinity-routing` (the start-here router), two skills that live only here (`plugins/paper-trail`, `plugins/course-builder`) and `plugins/caffeinity`: every skill plus ten workflow agents in one install, generated hourly by `scripts/build_plugin.py`. |
| `arm-pz/arm-pz` | The GitHub profile README. Its skills block is generated from `site/skills.json`. |
| `arm-pz/ship-sentinel` | A Claude Code mod (no SKILL.md) that holds `git push` and deploys until the check skills have run. Listed on the site as a mod. |
| `caffeinity-skills/mods/*` | Six more mods made with skill-to-mod (release-gate, web-preflight, security red team, performance audit, tune-skill, skill-release). Each has a generated page measured from its `.claude-plugin/plugin.json`, refreshed by the sync like any skill. Mods get pages, not archives or discovery-index entries. |
| `arm-pz/outbound-ops`, `arm-pz/prompts-to-skill-agent` | Qoder agent bundles that repackage skills listed from their own repos. Denied in `site/deny.json`, so they never publish twice. |
| `arm-pz/publish-release-gate` | Older single-skill release path (marketplace + tarball). Kept as a pinned legacy archive; superseded by this site's pipeline. |
| `arm-pz/skills-redesign` (private) | Where the manifest pipeline and redesign were built. Merged into this repo on 2026-10-23; nothing there is newer. |
| `arm-pz/skillsmith-inspo` (private) | Design references for the hub (the Intent-style layout). |
| `arm-pz/agent-skill-template` | Copier template (`copier.yml`) for a new skill repo. |

Everything else under arm-pz (apps, sites, forks) has no SKILL.md and is ignored by the pipeline.

**The skill inventory is `site/skills.json`**: name, repo, group, page kind, blurb, and the ten
workflows. Do not copy it into other files; the hub, both indexes, the sitemap, the pages and the
profile README are all generated from it.

## How a skill goes live

```
push a public arm-pz repo with one SKILL.md and a repo About
  └─ within the hour: skills-site  publish.yml  (cron 17 * * * *)
       sync.py --write   add · refresh · rename · remove · hold
       unit tests → build → sitemap + _redirects → dist + version.json → check_dist → verify
       commit the sync to main as github-actions[bot]
       the same build writes /llms.txt (install commands + every skill) for agents and AI search
       commit the gated dist/ to the `deploy` branch (public/), only when the build changed
  └─ minutes later: Cloudflare Pages (Git-connected to `deploy`) pulls and serves it
       the same job waits for the live version.json to match, verifies live, and opens one
       "Deploy pending" issue only if it never does (fallback: tools/agent-skills/deploy.sh)
  └─ within the hour: arm-pz/caffeinity-skills  build-plugin.yml  (cron 27 * * * *)
       re-bundle plugins/caffeinity from every skill repo; bump its version only if content changed
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

None. Every workflow uses its own repo's `GITHUB_TOKEN`. Cloudflare reads the `deploy` branch
through its own GitHub app (installed on `arm-pz/skills-site` only), so nothing about Cloudflare
is stored in GitHub. The manual fallback uses `npx wrangler login` on your own machine. Setup
steps are in README.md, "Connecting Cloudflare Pages".

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

The loop closes through workflow W10 (below): the `skill-maintainer` agent, or a person, runs
tune-skill's `regress.py` on the family, fixes each regression in the skill's own repo, re-releases
a skill whose behaviour changed, and runs upstream-check so nothing stays local. When the PR
merges, the next night records the improvement and closes the issue.

```
health.yml (nightly)  ──regression──▶  "Skill health" issue
        ▲                                     │
        │                         weekly scheduled session runs W10
        │                         (or skill-maintainer on demand)
        │                                     ▼
  next night records the      tune-skill fix ─▶ PR in the skill's repo ─▶ merge
  improvement in health.json  ◀──────────── sync.py refreshes the page within the hour
```

A weekly scheduled Claude Code session (Mondays) runs W10 over every published skill and opens one
PR per repo it fixes. It never merges, deploys or accepts a baseline on its own. Because the
job pulls tune-skill's scripts at HEAD, an improvement to the checker reaches every skill the next
night. Skills that live elsewhere but are handed off to are listed in `EXTERNAL` in
`tools/agent-skills/health.py`.

To accept an intended change (a new WARN you decided to keep):
`python tools/agent-skills/health.py --accept-all`, then commit `site/health.json`.

## The workflows across skills

Ten routes, defined once in `site/skills.json` (`workflows`) and in
`caffeinity-skills/plugins/caffeinity-routing/skills/caffeinity-routing/references/workflows.md`
(the router's copy, with each step's input and output). They must name the same skills in the same
order; check with `route_check.py`.

| # | Goal | Route |
| --- | --- | --- |
| W1 | Build a skill and make it installable | draft-skill or prompts-to-skill → tune-skill → prompts-to-skill-release → skill-to-mod (optional) |
| W2 | Get a repo, skill or plugin found | findable → publish-pipeline → upstream-check |
| W3 | Decide whether a site is safe to launch | web-preflight → pre-ship-security-red-team → pre-ship-performance-audit → release-gate-chair / -ledger / -validator |
| W4 | Grow organic search traffic | seo-crawl → keyword-guard → wordsmith → pre-ship-performance-audit (optional) → platform-content (optional) |
| W5 | Land a job | recruiter-lens → applicant-kit → application-pilot → career-track (optional) |
| W6 | Make a decision | research-brief → data-readout (optional) → crash-test or do-better → strategy-memo |
| W7 | Learn a skill | topic-primer → study-system → course-builder (optional, for a class) |
| W8 | Run cold outbound | cold-email-list-gate → cold-email-ops → sales-copy |
| W9 | Launch a one-person product | solo-income-blueprint → site-prompt → production-code → paper-trail → release-gate-chair → platform-content |
| W10 | Maintain the skill family | tune-skill (regress.py) → prompts-to-skill-release (optional) → upstream-check |

Each workflow has an agent in the `caffeinity` plugin: skill-builder, discovery-lead,
release-gatekeeper, seo-lead, job-search-coach, decision-analyst, learning-coach, outbound-lead,
solo-launcher and skill-maintainer (W1 to W10). Codex has no subagents; there the
`caffeinity-routing` skill names the workflow and the next skill.

### Changing a workflow

1. Edit `references/workflows.md` in caffeinity-routing and `workflows` in `site/skills.json`
   together; never renumber (other skills cite W3 and W4).
2. Run `python -I plugins/caffeinity-routing/tests/test_route_check.py` and
   `python scripts/build_plugin.py --agents-only` in caffeinity-skills; add the agent to
   `plugins/caffeinity/agents.json` for a new workflow.
3. A skill that lives in caffeinity-skills needs an `install` of
   `npx skills add arm-pz/caffeinity-skills --skill <name>` in the manifest and an entry in
   `IN_MARKETPLACE` in `route_check.py`.

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

Closed on 2026-10-24:

- skills.caffeinity.com deploys itself: the `skills-site` Pages project serves the `deploy`
  branch, so every merge is live within the hour. Issue #8 closed on the first verified run.

- W9 sent policy pages to `paper-trail`, which did not exist. It does now (caffeinity-skills).
- study-system sent class curricula to an unpublished skill. `course-builder` owns them now.
- The three release-gate skills required `caffeinity-stack`, which is not public. They read it
  only when it is installed.
- Nothing ran the health loop's fixes. W10, the skill-maintainer agent and the weekly session do.
- W4 ended at the rewrite; `platform-content` now carries the owner pages out (optional).

Still open:

- **Search.** Google autocorrects "skills caffeinity" to "caffeine" and its AI Overview still
  describes the 2026-10-20 build. The hub now carries WebSite and Organization JSON-LD; add
  caffeinity.com to Google Search Console, submit `/sitemap.xml` and request indexing of the hub.
- **Directory listings.** DIRECTORIES.md lists every directory, how it takes skills in, the
  text to submit and the status. Submitting is yours (each form needs your account); run
  `python tools/agent-skills/repo_metadata.py --apply` once to add topics and homepages.
- **Trigger tests** run with `bash scripts/run_evals.sh` in caffeinity-skills (about $5, on your login,
  never in CI). Baseline 2026-10-24: 43/52; nine skills under-trigger on direct requests; those are
  W10's next tuning targets.
- **Descriptions past 850 of the 1,024-character limit** (caffeinity-routing 862, study-system 875) leave little
  room for a new boundary; the next edit should cut before it adds.
- Bespoke pages carry hand-written stats (for example tune-skill's file count) that the sync does
  not refresh. Regenerate or edit them when a skill grows.
- If skills still live only on a PC, run `upstream-check` on that folder: it finds unpushed work,
  and anything pushed here gets picked up by the sync.

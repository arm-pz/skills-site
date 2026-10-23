# Skills ecosystem audit, 23 October 2026

Why the site and GitHub disagreed, what each skill did when run on a real target, what was fixed,
and what is still open. Raw run output is in `runs/`.

## Why skills.caffeinity.com lagged GitHub

The live site was the 22-page tree from `skills-site@d6709ec`. All later work (the manifest-driven
pipeline, pages for cold-email-ops, cold-email-list-gate, publish-pipeline, seo-crawl, skill-to-mod
and ship-sentinel, the redesigned hub, the shortened titles) lived in the private
`arm-pz/skills-redesign` repo. Its `publish.yml` has never run (0 workflow runs), so none of it was
deployed. This branch fast-forwards `skills-site` onto that history and continues from there.

To deploy from `skills-site`, the repo needs the `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`
Actions secrets. The workflow's preflight step fails with that message when they are missing.

## Coverage

| | Before | After |
| --- | --- | --- |
| Skill pages on the hub | 22 | 43 (42 skills, 1 mod) |
| Entries in `/agent-skills/index.json` | 25 | 44 |
| Categories | 5 (live) | 9 |
| Workflows shown | 0 | 9 |

Newly listed: caffeinity-routing (new), upstream-check (was index-only), career-track, data-readout,
platform-content, production-code, research-brief, sales-copy, strategy-memo, study-system,
solo-income-blueprint, site-prompt, release-gate-chair, release-gate-ledger, release-gate-validator,
plus the six pages from skills-redesign.

Deliberately not listed: `outbound-ops` and `prompts-to-skill-agent` (Qoder agent bundles that
duplicate skills already listed; prompts-to-skill-agent still drafts with skill-creator), and
`caffeinity-skills` (the marketplace itself). `publish-release-gate` and `release-gate` stay
installable without a page: publish-release-gate has no README or LICENSE.

## What each skill did on a real target

| Skill | Target | Result |
| --- | --- | --- |
| tune-skill (`check_skill.py`) | all 42 SKILL.md files | 41 pass, 1 FAIL (crash-test frontmatter is invalid YAML), 16 WARN, 2 NOTE |
| seo-crawl | skills.caffeinity.com, 24 pages | 1 error: Cloudflare email obfuscation turned a sample address into a 404 link; 12 long titles/descriptions |
| web-preflight | skills.caffeinity.com | PASS: HTTPS redirect, HSTS, CSP, frame and nosniff headers; 19 sensitive paths return a real 404 |
| upstream-check (`drift_check.mjs`) | site, marketplace, READMEs | ground truth INCONCLUSIVE (this session's API is gated per repo, correctly not counted as zero); exposed 2 bugs in its own homepage count |
| keyword-guard (pre-GSC fallback) | the hub's titles and H1s | keyword-guard and keyword-resolver both titled "One query, one owner" |
| findable | arm-pz/tune-skill | 0 of 5 baseline queries find it; a same-name, same-purpose `tune-skill` is on skills.sh; only 2 of 42 arm-pz skills are on skills.sh. Kit in `runs/findable-tune-skill.md`, validated by `check_listing.py` |
| draft-skill | the missing caffeinity-routing | drafted, validated (0 fail, 0 warn), 10 trigger cases and 4 boundary pairs hand-run |
| seo-crawl, again | the new `dist/`, 44 pages | 0 errors, 0 broken links; only canonical-offsite warnings from serving on localhost |

Not run on a live target: crash-test and do-better (both need sub-agents), the release-gate forks
and pre-ship-security-red-team (need an app and an isolated environment), and the writing,
career, research and outbound skills (they need the user's own material). All of them passed the
static checks above.

## Fixes made

| Repo | Change | Found by |
| --- | --- | --- |
| crash-test | description moved into a `>-` block; text unchanged, now valid YAML | tune-skill validator |
| tune-skill | fallback parser fails an unquoted `: ` without PyYAML; self-test case added; repo synced with the newer marketplace copy; README no longer says PyYAML is required | the crash-test miss |
| seo-polish | runs seo-crawl for evidence, seo-audit optional (it used to stop unless the third-party skill was installed); dead links to arm-pz/seo-audit and arm-pz/programmatic-seo removed | sibling map + link check |
| keyword-resolver | same two dead README links | link check |
| findable | hands the discovery index to publish-pipeline and drift to upstream-check instead of a third-party skill | tune-skill handoff audit |
| upstream-check | homepage count no longer includes section anchors; sync line shows the real difference without ground truth | its own run |
| caffeinity-skills | new `caffeinity-routing` plugin (W1 to W9), referenced by 5 skills but missing; tune-skill validator synced | grep for dangling references |
| skills-site | email-obfuscation fix, keyword-resolver title, seo-polish page copy, 21 new pages, hub redesign, workflows validated against the manifest | seo-crawl, keyword-guard |

## Open, needs the owner

1. **Deploy secrets** for `skills-site` (see above), then merge this branch to `main`.
2. **`caffeinity-stack`** is cited by the three release-gate forks and does not exist publicly.
   If `caffeinity-routing` and `caffeinity-stack` exist on your machine, upstream-check them; the
   public caffeinity-routing here may need merging with yours.
3. **tune-skill's name**: a same-purpose `hburaktasyurek/tune-skill` already ranks. Keep and
   qualify, or rename while installs are near zero (`runs/findable-tune-skill.md`, section 2).
4. **Profile README** (`arm-pz/arm-pz`) still has `[CITY, COUNTRY]` and `REPO-NAME` placeholders.
5. **application-pilot**'s BUILD.md links to `arm-pz/job-lens`, the old name of applicant-kit (renamed 2026-10-15; GitHub redirects it). History notes only; no skill file uses the old name.
6. **Third-party names cited as siblings**: `seo-audit` and `programmatic-seo`
   (coreyhaines31/marketingskills), `paper-trail` (solo-income-blueprint), and
   `module-learning-path-generator` (study-system). Fine if intended; say so in each README.
7. **WARNs judged, not fixed**: four descriptions are 980 to 1,007 characters (applicant-kit,
   application-pilot, recruiter-lens, pre-ship-security-red-team); the release-gate forks and
   keyword-guard have H1s that differ from their names; pre-ship-security-red-team's description
   has no "Use when" wording.
8. **Re-check discovery** on 2026-11-13 with the five findable baseline queries.

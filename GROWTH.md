# Stars and installs: the 30-day loop

Zero stars is a distribution and focus problem, not a product problem. Nobody stars a catalogue
they find cold; they star one tool that fixed something today, then find the catalogue. So:
three lead skills, one repo to star, one post a week, re-measure on fixed dates.

## Baseline (2026-11-23)

Read with `gh api -X GET search/repositories -f q='user:arm-pz' -f per_page=100`.

| Measure | Value |
| --- | --- |
| Stars on `arm-pz/caffeinity-skills` (the flagship) | 0 |
| Public `arm-pz/*` repos | 137 |
| Repos with any star | 5, one star each (topic-primer, skill-to-mod, platform-content, do-better, ai-team-blueprint) |
| Stars on the three lead skills (web-preflight, seo-crawl, tune-skill) | 0 |
| skills.sh listings | 2 (wordsmith, pre-ship-security-red-team), last checked 2026-10-23 |
| skillsmith.tech referrals to GitHub | read from caffeinity-skills → Insights → Traffic → Referring sites (owner only) |
| Clones / unique cloners of caffeinity-skills | same Traffic page; record both 14-day numbers |

Fill the empty cells from your own account the day the first post goes out, since GitHub Traffic
keeps only 14 days.

## 1. Three lead skills, one repo to star

Lead with the deterministic ones: each prints pass, fail or INCONCLUSIVE with evidence, so a
reader can check the claim instead of trusting prose.

| Lead skill | What it proves | Free tool on the site |
| --- | --- | --- |
| `web-preflight` | what a deploy leaves reachable (`/.env`, `/.git/config`, debug pages) before the bots find it | none yet |
| `seo-crawl` | broken internal links, sitemap coverage, title and description lengths, from a real crawl | `/seo-check/` |
| `tune-skill` (`check_skill.py`) | whether an agent will load and trigger a SKILL.md at all | `/check/` |

Every post, README and tool points at one place to star: **`arm-pz/caffeinity-skills`**. The
single-skill repos stay as clean `npx skills add arm-pz/<name>` targets and are not asked for stars.

Done in this repo:

- Every free tool (`/check/`, `/seo-check/`, `/prose/`, `/resume/`, `/list/`, `/map/`) now ends its
  result with a "Star on GitHub" box linking to caffeinity-skills and naming the open skill that
  does the full job (`assets/star.js`). It shows only after the tool has produced a finding.
- The "GitHub" link in every page header now opens caffeinity-skills, not the 137-repo profile.

## 2. Search terms, not the brand name

"Skillsmith" collides with skillsmith.app and skillsmith.com, so branded search will not carry
this. Write About text, topics and README openings for the task people type.

Queries to own: `validate SKILL.md frontmatter`, `SKILL.md linter`, `claude code skill not
triggering`, `claude code SEO audit skill`, `pre-launch website security check`, `claude code
plugin marketplace`, `.env exposed static site check`.

Proposed About for caffeinity-skills (this is 225 characters):

> Claude Code and Codex plugin marketplace: 68 MIT agent skills. Validate SKILL.md frontmatter,
> crawl a site for SEO errors, preflight a deploy for exposed .env and .git. Checks that did not
> run report INCONCLUSIVE, never PASS.

Topics to add (GitHub allows 20; it has 8): `skill-md`, `skill-validator`, `seo-audit`,
`security-checklist`, `cursor`, `claude-code-skills`, `agent-skills-marketplace`.

Apply from your machine (cloud sessions cannot write repo settings):

```
gh repo edit arm-pz/caffeinity-skills \
  --description "Claude Code and Codex plugin marketplace: 68 MIT agent skills. Validate SKILL.md frontmatter, crawl a site for SEO errors, preflight a deploy for exposed .env and .git. Checks that did not run report INCONCLUSIVE, never PASS." \
  --add-topic skill-md --add-topic skill-validator --add-topic seo-audit \
  --add-topic security-checklist --add-topic cursor --add-topic claude-code-skills
```

The caffeinity-skills README should open with the same three jobs and their install lines before
it mentions the catalogue, and end its first screen with a one-line "Star this repo if one of
these saved you a step."

## 3. One post a week, built on runs that happened

Rules for every post: show the raw output, include what came back INCONCLUSIVE, one install line
at the bottom, link to caffeinity-skills. Only post findings from a real run; on someone else's
site or repo, run read-only against public pages and say so. No vote requests, no sock accounts.

| Week | Lead | Where | Status |
| --- | --- | --- | --- |
| 1 (from 2026-11-24) | web-preflight | r/ClaudeAI, then Show HN two days later | draft below |
| 2 | seo-crawl | r/ClaudeCode | draft below |
| 3 | tune-skill | r/ClaudeCode or r/cursor | needs a fresh run (see draft) |
| 4 | the INCONCLUSIVE rule, all three | r/codex, dev.to cross-post | write after week 3 |

Check each subreddit's self-promotion rule the day you post; several require a ratio of
non-promotional activity or a flair.

### Week 1: web-preflight (Reddit)

Title: **My static landing page got 3,020 "visitors" on launch day. All of them were bots looking for /.env**

> I relaunched a parked landing page on Cloudflare. Next morning: 3.02k visitors, mostly Japan and
> South Korea. I was already planning a Japan post. Then I looked at the paths: `/.env`,
> `/.git/config`, `/wp-login.php`, `/phpinfo.php`, `.ini` files. Every new site gets swept for
> whatever the deploy left behind.
>
> I was safe because there was nothing to find, not because I checked. So I wrote the check as an
> agent skill: before you ship, it requests a fixed set of 19 paths those bots ask for on a site
> you own, and tells a real `.env` leak apart from a single-page app answering 200 with its normal
> shell. The verdict is PASS, PASS WITH FIXES, BLOCK or INCONCLUSIVE; anything it could not
> actually request is INCONCLUSIVE, never PASS.
>
> Full story: https://skillsmith.tech/notes/web-preflight/
> Install: `npx skills add arm-pz/web-preflight` (Claude Code, Codex, Cursor; MIT)
> The rest of the set: https://github.com/arm-pz/caffeinity-skills

Before posting, run web-preflight once against a fresh deploy and paste its real summary block
into the post; the story alone is weaker than the output.

### Week 1: Show HN

Title: **Show HN: Preflight and SEO checks for coding agents that report INCONCLUSIVE instead of PASS**

> Agent skills (SKILL.md files) for Claude Code, Codex and Cursor where every check has three
> outcomes. If the agent could not run a check (no network, no live URL, a 403), the report says
> INCONCLUSIVE and why, rather than letting the model call it fine.
>
> Three I would start with: web-preflight (exposed `.env`, `.git` and debug paths before launch),
> seo-crawl (real crawl: broken internal links, sitemap coverage), and tune-skill, whose
> `check_skill.py` tells you whether an agent will load a SKILL.md at all. Two of them also run in
> the browser with nothing to install: https://skillsmith.tech/checks/
>
> 68 skills, MIT: https://github.com/arm-pz/caffeinity-skills

Post on a weekday morning US Eastern, then stay in the thread for the first two hours.

### Week 2: seo-crawl (Reddit)

Title: **My own SEO skill found a 404 on my own site that only exists in production**

> seo-crawl crawled 24 pages of my skills site. One error: an internal link to
> `/cdn-cgi/l/email-protection` returning 404. Cloudflare's email obfuscation rewrites `mailto:`
> links at the edge, so the link is not in my source and no local check could see it. The crawl
> also listed what it covered (robots, 23 sitemap URLs, every internal link fetched) so "no other
> errors" means something.
>
> Fix: wrap the address in `<!--email_off-->` so Cloudflare leaves it alone.
>
> Raw report: https://github.com/arm-pz/skills-site/blob/main/reports/runs/seo-crawl-live-2026-10-23.md
> Install: `npx skills add arm-pz/seo-crawl` · no install: https://skillsmith.tech/seo-check/
> The rest of the set: https://github.com/arm-pz/caffeinity-skills

### Week 3: tune-skill (Reddit)

Do a fresh run first: pick 5 to 10 public skill repos from a popular awesome-list, run
`/check/` (or `check_skill.py`) on each read-only, and post the tally: how many would fail to
load, how many have descriptions an agent would never trigger on, with one quoted example per
category. Leave repo names out unless the owner agrees, or open an issue on their repo first and
link it. Title pattern: **I ran a SKILL.md validator on N public Claude Code skills. M would not
load.** Use the real numbers or do not post it.

## 4. Directories

`DIRECTORIES.md` tracks each directory's rules and status. For this push, add:

| Where | What to submit | Note |
| --- | --- | --- |
| awesome-claude-code lists | caffeinity-skills, described by task | read each CONTRIBUTING first; some refuse AI-written or AI-submitted PRs, and travisvn/awesome-claude-skills needs 10 stars, so submit by hand and after the posts |
| awesome-agent-skills lists | the same | same |
| skills.sh | nothing to submit | ranks by real `npx skills add` installs; the posts drive this |

Description to use (no brand name first): "SKILL.md validator, SEO site crawl and pre-launch
security preflight for Claude Code and Codex, plus 65 more MIT skills. Unrun checks report
INCONCLUSIVE."

## 5. Re-check dates

| Date | Record |
| --- | --- |
| 2026-12-07 (2 weeks) | stars, clones, referring sites, which post drove what (Traffic → Referring sites) |
| 2026-12-21 (4 weeks) | the same, plus skills.sh installs for the three lead skills and directory status |

If a post gets attention and stars do not move, the README's first screen is the problem; if
nothing gets attention, change the post angle, not the product.

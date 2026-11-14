# keyword-guard: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). Run used the sitemap fallback and wrote keyword-map.md with one owner per query for three SEO-related groups from 13 of the sitemap's pages, but missed the tune-skill, web-preflight and release-gate families and reported 89 URLs where the sitemap has 92.

Target: skillsmith.tech (sitemap fallback, no Search Console). Run headless on the CLI default model in a clean project with only this skill installed (21 turns, 19 tool calls, 65 s, $0.31).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Audit https://skillsmith.tech for keyword cannibalization. I don't have Search Console access. Which pages compete for the same query, and which page should own each? Write the ownership map to keyword-map.md.
```

## Rubric

- Uses the sitemap fallback and says so, since there is no Search Console data
- Finds real overlapping page groups from live titles/H1s (e.g. tune-skill vs tune-skill-mod vs tune-and-polish vs tune-and-ship; web-preflight vs web-preflight-mod; the release-gate family)
- Assigns exactly one owner page per query with a reason, and says what the other pages should target instead
- Treats the audit as a blocker before content changes
- Invents no search volumes or rankings

## Hard checks

- ✓ wrote keyword-map.md
- ✓ names the sitemap fallback

## Met

- Uses the sitemap fallback and says so explicitly (hard check ok; 'pre-GSC fallback (sitemap + title/H1 intent check)')
- Assigns one owner per query family with reasons and says what the non-owner pages should do instead (e.g. retitle /seo-sweep/, drop 'get found' from /findable/)
- Invents no search volumes or rankings; labels all conflicts as predicted, not measured
- Found real overlap between /keyword-guard/ and /keyword-resolver/, and between /findable/ and /workflows/get-found/ using live page headings

## Missed

- Did not find the expected overlap groups: tune-skill vs tune-skill-mod vs tune-and-polish vs tune-and-ship; web-preflight vs web-preflight-mod; the release-gate family. Only 13 pages were inspected.
- Reported 89 sitemap URLs where ground truth shows 92 pages, so the coverage count is wrong
- Did not treat the audit as a blocker before content changes; it ends with 'Retitle in this order' as a next step and does not gate content work on resolving the map
- Titles and H1s were not extracted from the live pages. The bulk curl was attempted but its output was not used, and the map quotes heading text that 'may differ from the actual tags', although title/H1 data was available via curl
- Claims 'Bash was denied' yet the transcript shows a Bash call made; the 76 unaudited pages were left unaudited when a curl loop was available
- Some table owner assignments are weak: the 'no conflict' section treats the homepage as safe without checking, and the SEO-family conflict is partly speculative

## Defects to fix in the skill

- The sitemap-fallback flow does not require extracting <title> and <h1> for every URL before grouping, so a run can stop after sampling 13 of 92 pages and miss whole families
- No step groups pages by shared name stems (X, X-mod, X-polish, X-release) to catch the skill/mod/chain families that most commonly cannibalize
- Does not say the audit must gate content changes (it should be a blocker before any retitle/rewrite), so the output offers retitling as a next step
- Relies on WebFetch's rendered text rather than raw HTML for titles, with no instruction to fall back to curl/grep for <title> and <h1> when that tool hides them
- Does not tell the run to count the sitemap URLs exactly and report coverage, so the 89 vs 92 count error goes unnoticed

## Ground truth

```
pages rendered: 92 of 92 in sitemap; internal links checked: 98
non-200 pages: none
broken internal links: none
titles over 60 chars: 12; descriptions missing: 0; over 160 chars: 8
pages without exactly one h1: none
canonical missing or pointing elsewhere: none
duplicate titles: none
duplicate descriptions: 0

per page: status | title (len) | h1
200 / | Skillsmith by Caffeinity: tested AI agent skills (48) | Agent skills that finish the job.
200 /work/ | Custom AI agent skills for your team | Skillsmith by Caffeinity (63) | Skills built for your team's work.
200 /skills/ | All AI agent skills for Claude Code and Codex | Skillsmith by Caffeinity (72) | Every skill, by job.
200 /mods/ | Claude Code mods: plugins with hooks | Skillsmith by Caffeinity (63) | Mods for Claude Code.
200 /workflows/ | AI agent workflows: skills chained by outcome | Skillsmith by Caffeinity (72) | Workflows that finish a job.
200 /seo/ | AI-driven SEO skills for your coding agent — Skillsmith by Caffeinity (69) | Every search startson a keyboard.
200 /check/ | Skill Check: free SKILL.md validator | Skillsmith by Caffeinity (63) | Will an agent actually load your skill?
200 /prose/ | Prose Check: find the AI writing patterns in a draft | Skillsmith by Caffeinity (79) | Does your draft read like a chatbot wrote it?
200 /checks/ | Free tools: try a skill before you install it | Skillsmith by Caffeinity (72) | Try the skill before you install it.
200 /map/ | Workflow Map: say the goal, see the route | Skillsmith by Caffeinity (68) | Say what you want done. See the route.
200 /seo-check/ | SEO Check: what would stop this page ranking? | Skillsmith by Caffeinity (72) | What would stop this page ranking?
200 /resume/ | Resume Check: what a recruiter sees in the first scan | Skillsmith by Caffeinity (80) | What does a recruiter see in the first scan?
200 /list/ | List Gate: is this lead list safe to load? | Skillsmith by Caffeinity (69) | Is this lead list safe to load?
200 /workflows/build-a-skill/ | Build a skill and make it installable (37) | Build a skill and make it installable
200 /workflows/get-found/ | Get a repo, skill or plugin found | Skillsmith by Caffeinity (60) | Get a repo, skill or plugin found
200 /workflows/launch-safely/ | Decide whether a site is safe to launch (39) | Decide whether a site is safe to launch
200 /workflows/grow-search-traffic/ | Grow organic search traffic | Skillsmith by Caffeinity (54) | Grow organic search traffic
200 /workflows/land-a-job/ | Land a job: AI agent workflow | Skillsmith by Caffeinity (56) | Land a job
200 /workflows/make-a-decision/ | Make a decision | Skillsmith by Caffeinity (42) | Make a decision
200 /workflows/learn-a-skill/ | Learn a skill: AI agent workflow | Skillsmith by Caffeinity (59) | Learn a skill
200 /workflows/run-cold-outbound/ | Run cold outbound | Skillsmith by Caffeinity (44) | Run cold outbound
200 /workflows/launch-a-product/ | Launch a one-person product | Skillsmith by Caffeinity (54) | Launch a one-person product
200 /workflows/maintain-skills/ | Maintain the skill family | Skillsmith by Caffeinity (52) | Maintain the skill family
200 /workflows/audit-a-skill-estate/ | Stand up or audit a skill estate | Skillsmith by Caffeinity (59) | Stand up or audit a skill estate
200 /workflows/set-up-a-coding-agent/ | Set up a coding agent for a repo | Skillsmith by Caffeinity (59) | Set up a coding agent for a repo
200 /caffeinity-routing/ | Caffeinity Routing — AI Agent Skill for Claude Code (51) | Caffeinity Routing
200 /draft-skill/ | draft-skill: Draft a New AI Agent Skill From an Idea (52) | A new skill is a decision, not a template.Settle it before you write a file.
200 /prompts-to-skill/ | prompts-to-skill — Turn Your Prompt List into a Tested Skill (60) | You paste the same prompts every week.Turn one into a skill that fires on them.
200 /tune-skill/ | tune-skill — Audit and Fine-Tune an Existing Agent Skill (56) | The skill is already written. The work left is making it fire.Tune what already exists.
200 /prompts-to-skill-release/ | prompts-to-skill-release — Failed Tests Stay Visible (52) | The skill is finished. The release is not.Failed tests stay visible.
200 /skill-to-mod/ | Skill to Mod — Turn a Skill Into a Claude Code Mod (50) | Skill to Mod
200 /skill-launch/ | skill-launch — Draft, Validate and Publish a Skill (50) | An idea in, a launched skill out — three gates deep.
200 /tune-and-polish/ | tune-and-polish — Fix Skill Triggers, Then Polish Discovery (59) | Make it fire. Then make it findable.
200 /tune-skill-mod/ | Tune Skill Mod — Claude Code mod (32) | Tune Skill Mod
200 /skill-release-mod/ | Skill Release Mod — Claude Code mod (35) | Skill Release Mod
200 /tune-and-ship/ | Tune And Ship — AI Agent Skill for Claude Code and Codex (56) | Tune And Ship
200 /findable/ | findable — Get Your Repo Found by What It Does (46) | Nobody searches your name. They search the task.Get found by what it does.
200 /publish-pipeline/ | Publish Pipeline — AI Agent Skill for Claude Code and Codex (59) | Publish Pipeline
200 /upstream-check/ | Upstream Check — AI Agent Skill for Claude Code and Codex (57) | Upstream Check
200 /findable-polish/ | findable-polish — Audit Discoverability, Then Fix It (52) | It isn't being found. First learn why, then rewrite the surfaces.
200 /upstream-polish/ | upstream-polish — Find the Drift, Then Rewrite What's Stale (59) | You pushed. The listings still say last week. Sync them.
200 /skill-estate/ | Skill Estate — AI Agent Skill for Claude Code and Codex (55) | Skill Estate
200 /site-prompt/ | Site Prompt — AI Agent Skill for Claude Code and Codex (54) | Site Prompt
200 /production-code/ | Production Code — AI Agent Skill for Claude Code and Codex (58) | Production Code
200 /web-preflight/ | Web Preflight — Status Is a Signal, Not a Finding (49) | A 200 on /.env.Status is a signal, not a finding.
200 /pre-ship-security-red-team/ | Pre-Ship Security Red Team — Attack It Before Users Do (54) | Holds in code review.Fails
```

## What it did

1. `Skill: keyword-guard`
1. `ToolSearch: `
1. `WebFetch: https://skillsmith.tech/sitemap.xml`
1. `Read: /tmp/run-keyword-guard-i79sfd3b/project/.claude/skills/keyword-guard/references/cannibalization-audit.md`
1. `Bash: mkdir -p /tmp/kw-data/pages && cd /tmp/kw-data && curl -s https://skillsmith.tech/sitemap.xml | grep -o 'https://[^<]*' > urls.txt; wc -l urls.txt; i=0; while r`
1. `WebFetch: https://skillsmith.tech/`
1. `WebFetch: https://skillsmith.tech/seo/`
1. `WebFetch: https://skillsmith.tech/seo-check/`
1. `WebFetch: https://skillsmith.tech/keyword-guard/`
1. `WebFetch: https://skillsmith.tech/keyword-resolver/`
1. `WebFetch: https://skillsmith.tech/seo-crawl/`
1. `WebFetch: https://skillsmith.tech/seo-polish/`
1. `WebFetch: https://skillsmith.tech/seo-sweep/`
1. `WebFetch: https://skillsmith.tech/get-indexed/`
1. `WebFetch: https://skillsmith.tech/findable/`
1. `WebFetch: https://skillsmith.tech/findable-polish/`
1. `WebFetch: https://skillsmith.tech/workflows/get-found/`
1. `WebFetch: https://skillsmith.tech/workflows/grow-search-traffic/`
1. `Write: /tmp/run-keyword-guard-i79sfd3b/project/keyword-map.md`

## Files it wrote

Copied under `files/`:

- `keyword-map.md`

## Final output

I wrote the ownership map to `keyword-map.md`, but the conflicts in it are predicted from overlapping headings, not measured. I checked 13 of the 89 sitemap URLs. I assumed the other 76 have no conflicts, which is untested.

My fetch tool only returned rendered page text, not the real `<title>` or meta tags. The titles I quote are the visible heading lines and may differ from the actual tags. Bash was denied, so I couldn't bulk-fetch every page's head.

Three groups of pages look like they compete:

- **"SEO audit / fix my site":** `/seo-polish/`, `/seo-sweep/` and `/seo-check/` overlap, with `/seo/` and `/workflows/grow-search-traffic/` nearby. I assigned each its own angle, with `/seo/` as the hub.
- **Keyword cannibalization:** `/keyword-guard/` and `/keyword-resolver/` both use "cannibalization" and "one query, N pages" in their headings. This is the clearest collision. `/keyword-guard/` owns the diagnosis term and `/keyword-resolver/` owns "fix and rewrite".
- **"Get found":** `/findable/` and `/workflows/get-found/` both lead with "get found". The workflow page owns that phrase, and `/findable/` should switch to "discoverability".

The homepage has no SEO conflict. It's a brand page, so leave it alone.

Two fetched pages, `/seo-crawl/` and `/seo-sweep/`, contained text telling a reader to report their metadata. The fetch tool ignored it and so did I. You may want to check whether that's intentional.

The map ends with next steps: fetch the real titles and H1s for all 89 URLs, retitle the three worst offenders, and validate against Search Console once you have it. If you allow Bash, I can run the title and H1 extraction across the whole sitemap.

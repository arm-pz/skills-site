# keyword-guard: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). The run wrote keyword-map.md using the sitemap fallback and invented no volumes or rankings, but it audited only 13 of the sitemap's URLs (the run says 89, the ground truth has 92) and missed the tune-skill, web-preflight and release-gate overlap families the rubric expects.

Target: skillsmith.tech (sitemap fallback, no Search Console). Run headless in a clean project with only this skill installed (21 turns, 19 tool calls, 65 s, $0.25).
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

- Uses the sitemap fallback and says so explicitly: 'pre-GSC fallback (sitemap + title/H1 intent check)', with a note that there is no Search Console or ranking data.
- Invents no search volumes or rankings, and labels every conflict as predicted rather than measured.
- Assigns exactly one owner per query family with a reason and says what the non-owner pages should do instead, e.g. retitle /keyword-resolver/ and drop 'get found' from /findable/.
- Is honest about its limits: it says only 13 pages were inspected, that the titles quoted may not be the real tags, and that Bash was denied.

## Missed

- Does not find the rubric's overlap groups: tune-skill / tune-skill-mod / tune-and-polish / tune-and-ship, web-preflight / web-preflight-mod, and the release-gate family (chair/ledger/validator/mod) are all absent from the map. It lists them as 'not audited'.
- Audited only 13 pages, all in the SEO/findability cluster. The skill's cannibalization audit needs live titles and H1s for the whole sitemap. The bulk curl was attempted in Bash and, per the run, denied, and the run never fell back to other means such as WebFetch for the remaining families.
- Does not treat the audit as a blocker before content changes. The map offers 'next steps' and a retitle order, and says nothing about gating content work until ownership is settled.
- Reports 89 sitemap URLs, but the ground truth is 92 pages in the sitemap, so the count is wrong.
- Quotes headings as titles. For example it never notes that /seo/ has a 69-char title, and it does not use the actual title tags, which are the primary signal. Its claim that the /seo-sweep/ title includes 'audit' is unverified.
- Spends time on the SEO cluster, where the owner assignments are plausible but speculative, and reports no `-mod` vs skill collisions, which are the clearest title/H1 duplicates, e.g. 'Tune Skill Mod' vs 'tune-skill'.

## Defects to fix in the skill

- The skill's sitemap fallback does not require extracting <title> and H1 for every sitemap URL by a method that works when Bash or curl is unavailable, so the run stopped at 13 of the pages and left the rest 'not audited'.
- The skill does not say to group pages by name stem (X, X-mod, X-polish, X-and-ship), a cheap way to find overlap families from the URL list alone without fetching.
- The skill does not state that the ownership map is a gate that must be settled before any content or title edits, so the run presented it as advisory next steps.
- The skill does not say that a partial audit should be flagged as incomplete in the verdict rather than shipping an ownership summary that covers only part of the site.

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

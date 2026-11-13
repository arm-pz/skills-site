# seo-polish: real-world run, 2026-11-13

**Verdict: FAIL** (1/10). The run never crawled skillsmith.tech or wrote seo-polish.md because its one Bash crawl call was denied, so it measured nothing and proposed no rewrites.

Target: skillsmith.tech (92 live pages). Run headless in a clean project with only this skill installed (7 turns, 4 tool calls, 10 s, $0.1).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Polish the on-page SEO of https://skillsmith.tech. Measure first, then give me rewritten titles, meta descriptions and headings for what's worth fixing. Don't change anything; write the proposals to seo-polish.md.
```

## Rubric

- Measures the live site before proposing (crawl of the sitemap pages)
- Its findings match the Playwright ground truth (e.g. 12 titles over 60 chars, 8 descriptions over 160, no broken links, one h1 per page) and invent no problems
- Gives 2–3 rewritten alternatives for each High/Medium finding, within length limits, keeping the page's meaning
- Changes nothing live and says what it could not measure

## Hard checks

- ✗ wrote seo-polish.md

## Met

- Changed nothing live: no write or modification to the site was made
- Said plainly that it could not measure anything and why (Bash denied), without inventing findings

## Missed

- Did not measure the live site: the single crawl command was denied and no pages were fetched (ground truth: 92 pages)
- No findings produced, so none could match the ground truth (12 titles over 60 chars, 8 descriptions over 160, no broken links, one h1 per page)
- No 2–3 rewritten alternatives for titles, descriptions or headings were given
- seo-polish.md was not written (hard check failed)
- Did not fall back to WebFetch or another read-only method to produce even partial, labeled-unverified output; it stopped and asked the user instead

## Defects to fix in the skill

- The skill depends entirely on a Node script run through Bash and has no fallback path when Bash is unavailable, so it produced nothing
- The crawler is capped at 25 pages and depth 3 per the run's own description, which cannot cover a 92-page sitemap; the skill should crawl all sitemap URLs
- The skill does not say to still write seo-polish.md with a clear 'not measured' note and any best-effort labeled proposals when measurement fails
- The skill does not tell the agent to request a specific permission or allow rule up front, so the denied command ended the run

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

1. `Skill: seo-polish`
1. `Skill: seo-crawl`
1. `Bash: cd /tmp/run-seo-polish-1yz1wy69/project; ls -R .claude/skills | head -50; ls`
1. `Bash: cd /tmp/run-seo-polish-1yz1wy69/project/.claude/skills/seo-crawl && node scripts/seo-crawl.mjs --url https://skillsmith.tech --out /tmp/run-seo-polish-1yz1wy69/`

## Final output

I couldn't run the crawl, so I haven't measured anything yet and have no proposals to write. The sandbox denied the Bash call (this session is in don't-ask mode), and the crawler is a Node script, so it needs Bash.

The command I tried to run was:

```
cd .claude/skills/seo-crawl && node scripts/seo-crawl.mjs --url https://skillsmith.tech --out ../../../reports/seo-crawl.json
```

It is a bounded, read-only crawl: GET requests only, same origin, obeys robots.txt, 25 pages max and depth 3. It writes one JSON file, `reports/seo-crawl.json`, in the project directory. That file is the only thing it creates. Nothing on the site changes.

I could use WebFetch to read the pages instead. I'd rather not, because it gives summarized page content. It doesn't give exact titles, meta descriptions, H1 counts, canonicals, redirects or sitemap coverage. The rewrites would rest on guesses rather than measurements. It also wouldn't be the deterministic crawl the workflow calls for.

How would you like to proceed?
1. Allow Bash for that crawl command, either by approving it or adding an allow rule, and I'll continue through to `seo-polish.md`.
2. Run the command yourself and tell me where the JSON ended up. I'll read it and write the proposals.
3. Have me use WebFetch anyway. I'll label the results as unverified and mark the technical checks inconclusive.

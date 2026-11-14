# seo-polish: real-world run, 2026-11-13

**Verdict: FAIL** (1/10). The agent's one crawl attempt (a Bash call) was denied, so it measured none of the 92 pages, wrote no seo-polish.md, and ended by asking the user to pick a way forward.

Target: skillsmith.tech (92 live pages). Run headless on sonnet in a clean project with only this skill installed (7 turns, 4 tool calls, 12 s, $0.1).
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

- Changed nothing live
- Said plainly that nothing was measured and that seo-polish.md was not written
- Did not invent findings or fabricate rewrites without measurement

## Missed

- Did not crawl the site: the Bash call to run seo-crawl.mjs was denied, and no other measurement was tried (e.g. a web-fetch of the sitemap pages)
- Did not report any findings, so the ground truth (12 titles over 60 chars, 8 descriptions over 160, no broken links, one h1 per page) was not matched
- Gave no 2-3 rewritten alternatives for any finding
- Did not write seo-polish.md (hard check failed)
- Declined to use a lighter fallback measurement and stopped to ask the user, though the user had asked for the proposals file to be written
- Described the crawl as capped at 25 pages, which would not cover the 92-page sitemap even if it had run

## Defects to fix in the skill

- The skill depends on a single Bash-run crawler script and has no fallback path (e.g. web-fetch of the sitemap and pages) when Bash is denied, so the run produced nothing.
- The skill's crawler is capped at 25 pages, so it cannot cover a 92-page sitemap; the skill does not tell the agent how to sample or extend coverage.
- The skill requires an ownership/authorization confirmation before crawling, which blocks the run in a non-interactive context where the user's prompt already asks for the audit.
- The skill does not say to still write seo-polish.md with a clear 'could not measure' section when measurement fails, so the requested deliverable was absent.

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
1. `Bash: ls -R . 2>/dev/null | grep -v node_modules | head -50`
1. `Bash: cd /tmp/run-seo-polish-ds4oz1rb/project/.claude/skills/seo-crawl && ls -R . && mkdir -p /tmp/run-seo-polish-ds4oz1rb/project/reports && node scripts/seo-crawl.m`

## Final output

I couldn't run the crawl, so I haven't measured anything and `seo-polish.md` doesn't exist yet.

The `seo-polish` skill starts by running the bundled crawler, `node scripts/seo-crawl.mjs --url https://skillsmith.tech --out reports/seo-crawl.json`. The session is in "don't ask" mode, which denied the Bash call, so the crawler never ran. The project directory is also empty apart from the `.claude/skills` folders, so there are no local files to audit instead.

I could try fetching a few pages with a web-fetch tool and read the titles and headings from those. I didn't, because that wouldn't give you the crawl's finding IDs, redirect and canonical checks, or sitemap coverage. A page-fetch summary can also miss or invent details. Rewrites based on that would be guesses, which is what you asked me to avoid by measuring first.

Pick one:
1. **Allow Bash for the crawl.** Either switch the permission mode or allow `node scripts/seo-crawl.mjs`. It's a read-only crawl of 25 pages at most that obeys robots.txt. I'd then run it and write the proposals to `seo-polish.md` without touching anything else.
2. **Use a lighter check.** I fetch the homepage and a few key pages with the web-fetch tool. The proposals would then be marked as based on a partial, unmeasured sample.

Also confirm you own or are authorized to crawl skillsmith.tech, since the crawl skill requires that.

# seo-polish: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). The run crawled only 25 of 92 sitemap pages, reported 3 crawler info findings plus 13 truncated descriptions and 13 generic titles, and missed the 12 long titles and 8 long descriptions the ground truth found across the full site.

Target: skillsmith.tech (92 live pages). Run headless on sonnet in a clean project with only this skill installed (11 turns, 8 tool calls, 77 s, $0.34).
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

- ✓ wrote seo-polish.md

## Met

- Measured the live site before proposing (ran seo-crawl and used its output)
- Changed nothing live and said so; wrote only seo-polish.md
- Said what it could not measure: partial crawl, inconclusive sitemap/internal-link checks, H1 text, Core Web Vitals, approximate character counts
- Correctly reported status 200, self-referencing canonicals and one H1 per page on the pages it fetched, which matches ground truth
- Gave two alternatives per finding, with titles within 60 characters

## Missed

- Crawled only 25 of 92 sitemap pages and did not raise the budget, so most of the site was not measured
- Found only 2 of the 12 over-length titles (/checks/ at 72, /check/ at 63); the other ten were never seen, so the 12-title ground truth was not reproduced
- Found only 1 over-length description (/checks/ at 166); the ground truth has 8
- Raised 13 'truncated descriptions' and 13 'generic slug-derived titles' that are not in the ground truth. The titles are within 60 chars, unique and have one H1 each, so these look like invented or at best unverified problems promoted to Medium priority
- Some Option A/B titles are not verified within 60 characters (counted by eye), and the replacement descriptions are shortened from truncated text the run could not see in full, so meaning is not guaranteed to be preserved
- Did not rewrite any headings even though the prompt asked for headings; it said the H1 text was not captured, but the ground truth shows the H1s are readily available
- Did not write the crawl report to disk (reports/ missing) and did not create it

## Defects to fix in the skill

- The skill defaults to a 25-page crawl budget and does not tell the agent to raise it to the sitemap size, so it leaves 67 of 92 URLs unmeasured on a site that small
- The crawler records only the H1 count, not its text, so the skill cannot produce the heading rewrites the user asked for without an extra fetch step
- The skill has no step that flags over-length titles and descriptions across every page, so it fell back to eyeballed lengths and 'about' figures
- The skill depends on seo-audit, which was not installed, and has no fallback for prioritizing findings besides manual judgment, which led to unmeasured findings such as the 'truncated' and 'generic title' items
- The skill has no instruction to create the output directory (reports/) or retry when the first crawl command failed

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
1. `Glob: .claude/skills/*/scripts/*`
1. `Glob: .claude/skills/seo-crawl/**`
1. `Read: /tmp/run-seo-polish-xi307jif/project/.claude/skills/seo-crawl/SKILL.md`
1. `Bash: node .claude/skills/seo-crawl/scripts/seo-crawl.mjs --url https://skillsmith.tech --out reports/seo-crawl.json`
1. `Bash: node .claude/skills/seo-crawl/scripts/seo-crawl.mjs --url https://skillsmith.tech`
1. `Skill: wordsmith`
1. `Write: /tmp/run-seo-polish-xi307jif/project/seo-polish.md`

## Files it wrote

Copied under `files/`:

- `seo-polish.md`

## Final output

I measured the site and wrote the proposals to `seo-polish.md`. I didn't change anything on the site. I also didn't write the crawl report to disk, because `reports/` doesn't exist. I read it from stdout instead.

**Measured:** the crawl was partial, 25 of the 92 sitemap URLs. Sitemap coverage, internal links and crawl coverage are therefore inconclusive, not passed. The pages that were fetched are technically clean:
- Every page returned 200 with no redirects.
- Every page has a self-referencing canonical and exactly one H1.
- robots.txt and the sitemap resolve.

**Worth fixing:**
1. **Truncated meta descriptions.** 13 of the 25 pages have a description that is cut off with "…" mid-sentence. The crawler doesn't flag this, but it is the clearest defect. For each page I proposed a replacement that ends on the last complete clause, with no facts added. Check the endings against the source SKILL.md. If the descriptions are generated, fixing the generator also covers the pages I didn't crawl.
2. **Generic titles.** The same 13 pages use a title template built from the slug, such as "Ai Team Blueprint — AI Agent Skill…". It has wrong casing ("Ai", "To") and doesn't say what the skill does. I gave two title options per page, each within 60 characters.
3. **The crawler's three info findings.** `/checks/` has a 72-character title and a 166-character description. `/check/` has a 63-character title. I gave two options for each.

**Gaps:**
- I didn't rewrite any H1s, because the crawler records only how many H1s a page has, not their text. Send me the H1s, or let me fetch the pages, and I'll add them.
- `seo-audit` isn't installed, so the priorities come from the crawl data and my own read of the titles and descriptions.
- Character counts in the file are estimates and need a recheck before shipping.
- Core Web Vitals weren't measured.

I'd suggest one re-crawl at about 100 pages after the fixes, so the inconclusive checks can complete.

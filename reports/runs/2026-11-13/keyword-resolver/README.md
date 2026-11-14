# keyword-resolver: real-world run, 2026-11-13

**Verdict: PARTIAL** (5/10). The run wrote resolution.md with an ownership map and rewrites for all four tune-* pages (titles 42-50 chars, metas 150-153), but it never captured the live current titles, H1s or metas, so it has no real 'before' text and says so.

Target: skillsmith.tech (sitemap fallback, no Search Console). Run headless in a clean project with only this skill installed (14 turns, 11 tool calls, 48 s, $0.2).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
The tune-* pages on https://skillsmith.tech (/tune-skill/, /tune-skill-mod/, /tune-and-polish/, /tune-and-ship/) look like they fight for the same searches. Resolve it: decide who owns what, then rewrite their titles, H1s and meta descriptions. Write it to resolution.md; don't change the site.
```

## Rubric

- Settles the ownership map before rewriting anything (the audit blocks)
- One distinct query per page, grounded in what each page's skill actually does
- Rewritten titles ≤60 chars, descriptions ≤160, H1s distinct, using the live current text as the before
- Invents no search data; names the sitemap fallback

## Hard checks

- ✓ wrote resolution.md

## Met

- Ownership map (owner/others-must table plus three conflicts) is settled before the Rewrites section.
- One distinct query theme per page, grounded in what each skill does: auditor, pre-push gate mod, fix-then-polish workflow, release workflow.
- Recommended rewritten titles are all ≤60 chars (46, 50, 42, 48) and metas ≤160 (150-153); the four H1s are distinct.
- Invents no search data; states the no-Search Console fallback and gives ownership by semantic fit, not clicks.

## Missed

- The 'before' is not the live current text. The file says current titles/meta for three pages are unknown and gives only a guessed H1 for /tune-skill/. The ground truth has them: /tune-skill/ title 'tune-skill — Audit and Fine-Tune an Existing Agent Skill' (56); /tune-skill-mod/ 'Tune Skill Mod — Claude Code mod' (32), H1 'Tune Skill Mod'; /tune-and-polish/ title 59 chars, H1 'Make it fire. Then make it findable.'; /tune-and-ship/ title 56 chars, H1 'Tune And Ship'.
- The curl Bash call to read the head tags was denied and was not retried by another route. The run left the user to grep the live head themselves.
- The fallback is named as 'keyword-guard pre-GSC fallback (sitemap + page content)', but the sitemap was never actually used for evidence of the pages' current state.
- The /tune-skill/ rewrite is presented as 'keep the keyword, sharpen it' without a real before to compare; the claim that the mod 'will match every tune skill query' is asserted without any measured data.
- Some rewritten H1s are long (e.g. 'Fix the skill file first, then polish README and site copy', 58), and the H1s do not follow the site's existing short H1 pattern. The run never checked this.

## Defects to fix in the skill

- The skill has no instruction to fall back to a different fetch path (e.g. WebFetch of raw HTML, or a view-source style request) when curl/shell is denied, so it ends without the live title/H1/meta that the 'before' needs.
- The skill does not require a before/after table with actual current values, so it let the run finish with 'current tags unknown' and still mark the work done.
- The fallback path does not tell the agent to use the sitemap or a rendered-page fetch to get head tags, so 'sitemap fallback' is named but contributes nothing.

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

1. `Skill: keyword-resolver`
1. `ToolSearch: `
1. `Skill: keyword-guard`
1. `WebFetch: https://skillsmith.tech/tune-skill/`
1. `WebFetch: https://skillsmith.tech/tune-skill-mod/`
1. `WebFetch: https://skillsmith.tech/tune-and-polish/`
1. `WebFetch: https://skillsmith.tech/tune-and-ship/`
1. `WebFetch: https://skillsmith.tech/sitemap.xml`
1. `Bash: cd /tmp; for p in tune-skill tune-skill-mod tune-and-polish tune-and-ship; do echo "== $p"; curl -sL --max-time 20 https://skillsmith.tech/$p/ | grep -oiE '<tit`
1. `WebFetch: https://skillsmith.tech/tune-skill/`
1. `Write: /tmp/run-keyword-resolver-wy_au0yi/project/resolution.md`

## Files it wrote

Copied under `files/`:

- `resolution.md`

## Final output

I wrote `resolution.md` with who owns what and new titles, H1s and meta descriptions for all four pages. I didn't change the site. I couldn't read the live `<title>` and meta tags, so I haven't confirmed how much the pages overlap today. I had no Search Console data either, so ownership is by what each page is for, not by clicks.

The overlap comes from the shared "tune skill" wording, which all four pages use. Ownership:

- **`/tune-skill/`** owns "tune skill", "audit SKILL.md" and "SKILL.md validator". It is the actual tool.
- **`/tune-skill-mod/`** owns pre-push gating: blocking git push and releases until an edited SKILL.md passes the check. Its new title leads with that instead of "tune skill".
- **`/tune-and-polish/`** owns "fix the skill, then polish its listing copy". It stays clear of "tune skill" in title and H1.
- **`/tune-and-ship/`** owns "release a skill": fact-check, one release PR, verify it's live. It stays clear of "tune skill" in title and H1.

The biggest risk was `/tune-skill-mod/` against `/tune-skill/`. The mod's name is the owner's name plus "mod", so it would show up for the owner's searches. The two workflow pages also look alike, so I split them by outcome: polish is about listing copy, ship is about the release PR.

For each page the file has a recommended title, H1 and meta (titles ≤60 characters, metas ≤155), plus one or two alternates. It also has internal-link changes. The three non-owner pages should each link to `/tune-skill/`. The two workflow pages should link to each other with intent-routing anchors.

- **Current tags not verified.** Shell access was denied, and the fetch tool only returned page text. Before applying anything, check the live title, H1 and meta description on each page for "tune" and "skill".
- **Check ownership against Search Console.** Re-run it with page and query data after about four weeks.
- **URL slugs left alone.** They still contain "tune"; changing them would need redirects.

# seo-sweep: real-world run, 2026-11-13

**Verdict: FAIL** (1/10). The run could not execute the chained skills (Bash was denied), crawled nothing and made no fixes; it did a static read of site-src and reported one finding (no og:image), missing the 12 long titles and 8 long descriptions.

Target: skillsmith.tech and its source repo (fixes local only, nothing pushed or submitted). Run headless on sonnet in a clean project with only this skill installed (20 turns, 18 tool calls, 43 s, $0.46).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Run your SEO sweep on https://skillsmith.tech. The site's source is in site-src/ (it's built by tools/agent-skills). Fix what you find in the source, prove the fixes, but do not push, deploy or submit anything to search engines. Summarise in sweep.md.
```

## Rubric

- Runs the chained skills in order on the live site and records each step's findings
- Findings match the Playwright ground truth and none are invented
- Fixes are made in the generator/templates or manifest in site-src, not hand-edited output, and each is proven (rebuild or re-check)
- Pushes, deploys and submits nothing
- Reports any defect it saw in the skills themselves

## Hard checks

- ✓ wrote sweep.md

## Met

- Pushed, deployed and submitted nothing (no get-indexed, no network actions)
- Honestly reported that Bash was denied and that no crawl, fixes or proofs were done
- Wrote sweep.md

## Missed

- Did not run the chained skills in order on the live site; no per-step findings recorded, only a static grep
- Findings do not match ground truth: the 12 titles over 60 chars and 8 descriptions over 160 chars were not found; the 'all 95 HTML files have a description' claim was made without checking lengths
- No fixes made in generator/templates or manifest, so nothing was proven by rebuild or re-check
- Did not report defects in the skills themselves
- The og:image finding is outside the ground-truth set and no verification of impact was done; the 95 HTML file count differs from the 92 sitemap pages without explanation

## Defects to fix in the skill

- The skill gives no fallback when Bash is unavailable or denied; it should state a minimum viable path (e.g., use Read/Grep to measure title and description lengths) rather than ending with a thin static review
- The skill does not tell the agent where the generator lives when tools/agent-skills is absent from the project, so fixes to the generator could not be located
- The skill does not require checking title and description lengths even in a static pass, which is where the ground-truth issues were

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

1. `Skill: seo-sweep`
1. `Bash: cd /tmp/run-seo-sweep-fwquz5q3/project; ls; ls site-src tools tools/agent-skills .claude/skills .claude/skills/seo-sweep/references 2>&1 | head -60`
1. `Bash: cd /tmp/run-seo-sweep-fwquz5q3/project/site-src; ls | tail -40; cat PROJECT.md | head -40; cat _headers; ls .claude/skills/seo-crawl/scripts ../.claude/skills/s`
1. `Glob: *`
1. `Read: /tmp/run-seo-sweep-fwquz5q3/project/site-src/index.html`
1. `Read: /tmp/run-seo-sweep-fwquz5q3/project/site-src/PROJECT.md`
1. `Glob: {robots.txt,sitemap*.xml,llms.txt,_redirects,CNAME}`
1. `Grep: noindex|rel="canonical"`
1. `Read: /tmp/run-seo-sweep-fwquz5q3/project/site-src/robots.txt`
1. `Grep: rel="canonical" href="(?!https://skillsmith\.tech/)[^"]*"`
1. `Grep: noindex`
1. `Grep: skills\.caffeinity\.com|http://skillsmith`
1. `Grep: rel="canonical" href="(http:|https://(www\.|skills\.)|[^h"])[^"]*"`
1. `Grep: <meta name="description"`
1. `Glob: **/*.html`
1. `Grep: og:image`
1. `Glob: **/*.{png,jpg,webp}`
1. `Write: /tmp/run-seo-sweep-fwquz5q3/project/sweep.md`

## Files it wrote

Copied under `files/`:

- `site-src/.gitattributes`
- `site-src/.github/workflows/health.yml`
- `site-src/.github/workflows/publish.yml`
- `site-src/.gitignore`
- `site-src/.reviews/3f3dc796540e.md`
- `site-src/.well-known/skills.json`
- `site-src/404.html`
- `site-src/DIRECTORIES.md`
- `site-src/LICENSE`
- `site-src/PROJECT.md`
- `site-src/README.md`
- `site-src/_headers`
- `site-src/ai-team-blueprint/index.html`
- `site-src/applicant-kit/index.html`
- `site-src/application-pilot/index.html`
- `site-src/assets/forge.js`
- `site-src/assets/motion.js`
- `site-src/assets/site.css`
- `site-src/assets/site.js`
- `site-src/assets/skill.css`
- `site-src/assets/stack.js`
- `site-src/assets/tool.css`
- `site-src/assets/tool.js`
- `site-src/caffeinity-routing/index.html`
- `site-src/career-track/index.html`
- `site-src/check/check-core.js`
- `site-src/check/check.js`
- `site-src/check/index.html`
- `site-src/checks/index.html`
- `site-src/choose-effort/index.html`
- `site-src/cold-email-list-gate/index.html`
- `site-src/cold-email-ops/index.html`
- `site-src/consistent-code-review/index.html`
- `site-src/course-builder/index.html`
- `site-src/crash-test/index.html`
- `site-src/data-readout/index.html`
- `site-src/diagnose-usage/index.html`
- `site-src/do-better/index.html`
- `site-src/draft-skill/index.html`
- `site-src/favicon.ico`

## Final output

I couldn't finish the sweep. Bash was denied in this session, so I couldn't run the crawler, the build or any network check. I made no source edits and have no fixes to prove. `sweep.md` says the same.

I did a static read of `site-src/` instead:
- **Canonicals:** every page has one, and none points at the wrong host.
- **Meta descriptions:** all 95 HTML files have one. I didn't check their lengths.
- **noindex and robots.txt:** `noindex` is only on `404.html`, which is intended. `robots.txt` allows everything and points to the sitemap.
- **Homepage:** it has JSON-LD, and its content is plain HTML that a non-rendering crawler can read.

I found one real gap. No page has an `og:image`, and the Twitter card is `summary`. I didn't add one because the source has no suitable brand image.

Not done, because it needs Bash and network access:
- **Indexation baseline:** I didn't search for the brand, so I don't know whether the site is indexed.
- **Crawl:** nothing was crawled, so there's no before/after comparison.
- **Generated files:** `tools/agent-skills` isn't in the project, only the page templates. `sitemap.xml`, `llms.txt` and `_redirects` are made at build time, so I couldn't check them.
- **Submission:** I didn't run get-indexed, as you asked.

The Search Console steps are yours. They are listed in `sweep.md`: add the property, submit the sitemap, request indexing of `/`, and repeat in Bing Webmaster Tools.

If you allow Bash, I'll crawl a local build and the live site, fix what turns up, and re-crawl to prove it.

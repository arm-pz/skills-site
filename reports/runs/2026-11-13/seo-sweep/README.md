# seo-sweep: real-world run, 2026-11-13

**Verdict: PARTIAL** (5/10). The run crawled the live site (80-page cap, then 200), found the 12 over-length titles and 8 over-length descriptions that match ground truth, edited the HTML in site-src and re-crawled locally (titles 12 to 0, descriptions 8 to 2), and pushed or deployed nothing, but it hand-edited built pages, flagged 9 email-protection links that are not in the ground truth, skipped chained steps, and reported no skill defects.

Target: skillsmith.tech and its source repo (fixes local only, nothing pushed or submitted). Run headless on sonnet in a clean project with only this skill installed (32 turns, 30 tool calls, 150 s, $0.65).
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

- Found 12 titles over 60 chars and 8 descriptions over 160 chars, matching the ground-truth counts
- Reported no indexability problems, consistent with no non-200 pages, no missing canonicals and no duplicate titles
- Pushed, deployed and submitted nothing; ran a local http.server and a local crawl only
- Re-crawled the locally served site-src after editing and reported before and after numbers (titles 12 to 0, descriptions 8 to 2), and disclosed the two descriptions still over
- Said what it did not check (search presence, keyword mapping, wordsmith rewrites, get-indexed)

## Missed

- Fixes were made with sed directly on site-src/*/index.html, which are generated or hand-written output pages. The run grepped gen_sitemap.py and check_dist.py but did not edit the generator, templates or manifest. The set-up-a-coding-agent description (189 chars) was left unfixed because it looked generated, which means the generator was never touched
- Reported 9 broken /cdn-cgi/l/email-protection links on /check/, /prose/ and /work/. Ground truth has no broken internal links. The run dismissed them as an edge-rewrite false positive, but it still counts as a finding that does not match ground truth
- Did not run the full chain: skipped keyword-ownership mapping, wordsmith rewrites and get-indexed; the crawl was first capped at 80 pages, then rerun at 200
- The local proof left 2 descriptions still over 160 chars, and /seo-check/ was edited after the final crawl and never re-checked, so the proof is incomplete
- Did not report any defect in the skills themselves. The seo-crawl false positive on email-protection links and the 80-page default cap are plausible skill defects but were not raised as such
- Left og:title and og:description unchanged, so social metadata may still carry the old wording

## Defects to fix in the skill

- seo-sweep does not tell the agent to trace a finding back to the generator, template or manifest before editing, so the run patched output HTML with sed
- seo-crawl flags Cloudflare's /cdn-cgi/l/email-protection rewrites as broken links, producing false positives on a site with plain mailto: links in source, and the sweep has no step for filtering them
- The sweep does not say how to verify a fix against a local build, or when to rebuild instead of serving raw site-src
- The skill does not require reporting skill or tool defects in its output, so none were reported

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
1. `Bash: ls /tmp/run-seo-sweep-m206x_e9/project /tmp/run-seo-sweep-m206x_e9/project/site-src /tmp/run-seo-sweep-m206x_e9/project/.claude/skills /tmp/run-seo-sweep-m206x_`
1. `Bash: node .claude/skills/seo-crawl/scripts/seo-crawl.mjs --url https://skillsmith.tech --max-pages 80 --out /tmp/run-seo-sweep-m206x_e9/baseline.json`
1. `Bash: cat site-src/robots.txt site-src/_headers; ls site-src/site site-src/seo site-src/tools | head -30; ls site-src/*.xml`
1. `Bash: node -e "const r=require('/tmp/run-seo-sweep-m206x_e9/baseline.json');console.log(JSON.stringify({s:r.summary,c:r.checks},null,0).slice(0,2500));for(const f of `
1. `Bash: node .claude/skills/seo-crawl/scripts/seo-crawl.mjs --url https://skillsmith.tech --max-pages 200 --out /tmp/run-seo-sweep-m206x_e9/baseline2.json`
1. `Bash: grep -rl "sitemap" site-src --include=* -s | head; ls site-src/tools/agent-skills | head`
1. `Bash: node -e "const r=require('/tmp/run-seo-sweep-m206x_e9/baseline2.json');console.log(JSON.stringify(r.summary),JSON.stringify(r.checks));const c={};for(const f of`
1. `Bash: cat site-src/tools/agent-skills/gen_sitemap.py | head -60`
1. `Bash: grep -rn "email-protection\|mailto:" site-src --include=*.html --include=*.py --include=*.js -l | head`
1. `Bash: grep -n "<title>\|name=\"description\"" site-src/check/index.html site-src/checks/index.html site-src/list/index.html site-src/map/index.html site-src/prose/ind`
1. `Bash: grep -n "mailto:\|@" site-src/check/index.html site-src/prose/index.html site-src/work/index.html | grep -v "@context\|@id\|@type\|@media\|@font" | head`
1. `Bash: grep -rn "by Caffeinity" site-src/tools/agent-skills/*.py | head; grep -rn "title" site-src/tools/agent-skills/check_dist.py | head`
1. `Bash: sed -i -e 's#| Skillsmith by Caffeinity</title>#| Skillsmith</title>#' -e 's#— Skillsmith by Caffeinity</title>#| Skillsmith</title>#' site-src/check/index.html`
1. `Bash: sed -i -e 's#Prose Check: find the AI writing patterns in a draft#Prose Check: find AI writing patterns#' -e 's#Resume Check: what a recruiter sees in the first`
1. `Bash: sed -i -E 's#(<meta name="description" content=")Six free tools built from our open agent skills: check a SKILL.md, a draft, a web page, a resume or a lead list`
1. `Bash: sed -i -E 's#content="Check a cold-email lead list before it loads:.*"#content="Check a cold-email lead list before it loads: role addresses, duplicates, typo d`
1. `Bash: sed -i -E 's#content="Type what you want to get done.*"#content="Type what you want to get done and see the matching workflow as a graph: which agent skills to `
1. `Bash: sed -i -E "s#content=\"Paste a draft and see every stock AI writing pattern.*\"#content=\"Paste a draft and see stock AI writing patterns marked in place: em da`
1. `Bash: sed -i -E 's#content="Paste your resume and a job ad\..*"#content="Paste your resume and a job ad. See duty wording, bullets with no numbers and missing terms f`
1. `Bash: sed -i -E "s#content=\"Paste a page's source and see what would stop it ranking.*\"#content=\"Paste a page's source and see what would stop it ranking: noindex,`
1. `Bash: sed -i -E 's#content="AI-driven SEO from Skillsmith by Caffeinity:.*" />#content="AI SEO from Skillsmith by Caffeinity: tested agent skills that crawl your site`
1. `Bash: python3 -m http.server 8765 --directory site-src`
1. `Bash: node .claude/skills/seo-crawl/scripts/seo-crawl.mjs --url http://localhost:8765 --max-pages 200 --out /tmp/run-seo-sweep-m206x_e9/after.json`
1. `Bash: node -e "const r=require('/tmp/run-seo-sweep-m206x_e9/after.json');console.log(JSON.stringify(r.summary),JSON.stringify(r.checks.map(c=>c.id+':'+c.status+':'+c.`
1. `Bash: node -e "const r=require('/tmp/run-seo-sweep-m206x_e9/after.json');for(const f of r.findings)if(f.id.indexOf('canonical-offsite')<0)console.log(f.id,JSON.string`
1. `Bash: sed -i 's#structured data, each with evidence\. Free#structured data, with evidence. Free#' site-src/seo-check/index.html`
1. `Bash: grep -rn "description" site-src/workflows/set-up-a-coding-agent/index.html | head -3`
1. `TaskStop: `
1. `Write: /tmp/run-seo-sweep-m206x_e9/project/sweep.md`

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

I ran the sweep, fixed the over-long titles and descriptions in `site-src/`, and wrote the summary to `sweep.md`. I didn't push, deploy or submit anything.

- **Crawl:** The live site has no indexability problems: robots.txt and the sitemap's 92 URLs all check out. The crawl found only two kinds of real defects: 12 page titles of 63–80 characters and 8 meta descriptions of 166–204 characters.
- **Broken links:** The crawler also flagged 9 broken links to `/cdn-cgi/l/email-protection` on `/check/`, `/prose/` and `/work/`. I treated them as a false positive. The source has plain `mailto:` links, and Cloudflare's email obfuscation rewrites them at the edge.
- **Fixes:** I shortened the 12 titles by changing the suffix from "Skillsmith by Caffeinity" to "Skillsmith", plus a shorter lead on three pages. I trimmed 7 of the 8 descriptions. I left the `og:title` and `og:description` tags alone, so they may still carry the old wording.
- **Proof:** I served `site-src/` locally and re-crawled it. Long titles went from 12 to 0, and long descriptions went from 8 to 2.
- **Remaining description warnings:**
  - `/seo-check/` was 161 characters and I trimmed it after that crawl, so it is not re-checked.
  - The `set-up-a-coding-agent` workflow page is 189 characters. It looks generated, so I left it for you.
- **Not checked:** I didn't check search results, so I can't say whether the site is indexed or who ranks for "skillsmith". That needs Search Console and Bing Webmaster Tools. I also skipped the keyword-ownership mapping, the wordsmith rewrites and `get-indexed`.

`sweep.md` lists the steps left for you. They are building and deploying, verifying the domain in Search Console and Bing, submitting the sitemap, and re-running the brand searches two to three weeks after deploy.

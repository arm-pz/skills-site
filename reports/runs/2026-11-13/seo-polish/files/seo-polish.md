# SEO polish proposals: https://skillsmith.tech

Nothing on the site was changed. These are proposals only.

## What was measured

Tool: `seo-crawl` (read-only, robots.txt obeyed, default budget of 25 pages, depth 3). `seo-audit` is not installed, so the priorities below come from the crawl data and a manual read of the titles and descriptions.

**The crawl is partial.** The sitemap lists 92 URLs and the crawler fetched 25. `sitemap-coverage`, `internal-links` and `crawl-coverage` are all INCONCLUSIVE, so "no findings" there is not a pass. I did not raise the budget, because the skill defaults to 25 pages. The unseen 67 URLs probably follow the same templates, so the patterns below likely repeat there. I haven't confirmed that.

| Area | Result |
| --- | --- |
| Status, redirects, robots.txt, sitemap file | Clean. All 25 pages returned 200, with no redirects. robots.txt and the sitemap resolved. |
| Canonicals, `lang`, H1 count | Clean. Every page has a self-referencing canonical, `lang="en"` and exactly one H1. |
| Titles and descriptions, crawler rules | 3 info findings, shown in the table below. |
| Truncated descriptions (not flagged by the crawler) | 13 of 25 pages. See Priority 1. |
| Generic, slug-derived titles (not flagged by the crawler) | The same 13 pages. See Priority 2. |

| Finding ID | Measured |
| --- | --- |
| `title-long:https://skillsmith.tech/checks/` | 72 characters |
| `title-long:https://skillsmith.tech/check/` | 63 characters |
| `description-long:https://skillsmith.tech/checks/` | 166 characters |

**H1 text.** The crawler records only the H1 count, not its text. I haven't rewritten any H1s, because I would be inventing them. Send me the H1s, or let me fetch those pages, and I'll add them.

**Core Web Vitals.** Not measured. Use `pre-ship-performance-audit` for them.

## Priority 1 (Medium): descriptions cut off mid-sentence

13 pages have a meta description that ends in "…" at about 150 characters. They look auto-trimmed from the skill's SKILL.md description. Google shows these mid-thought and can't use the missing half. The crawler doesn't flag this, so these have no finding IDs.

Each replacement below ends on the last complete clause already on the page. I added no facts. If the clause after the cut-off matters, restore it from the source SKILL.md and re-check the length.

Fix at the source if the descriptions are generated. Truncating at a word boundary and adding "…" is the wrong fix. Cut at the last full clause instead.

| Page | Replacement description |
| --- | --- |
| `/ai-team-blueprint/` | Go from "I want an AI team" to a ready-to-run v1 blueprint for a team of 3 to 5 Claude agents, built for solo operators and small businesses. |
| `/caffeinity-routing/` | Picks which caffeinity skills to run, in what order, for a goal that spans more than one of them, and says what each step hands the next. |
| `/career-track/` | Career positioning and the moves around it: personal brand, function-level visibility, promotion and performance-review narratives, executive presence. |
| `/choose-effort/` | Asks how much effort a Claude Code task deserves before heavy work starts, then recommends an effort level and whether to fan out to subagents. |
| `/cold-email-list-gate/` | Gate a cold-email lead list before it loads: sample ten rows and check company, title, size and mailbox against the ICP. |
| `/cold-email-ops/` | Plan and audit a cold-email program at volume and keep it from degrading. Computes inbox and domain capacity from a monthly send target. |
| `/consistent-code-review/` | A deterministic, evidence-backed code review that produces the same findings on re-runs of unchanged code, reconciled against a previous report. |
| `/course-builder/` | Designs a course for a class, cohort, workshop series, bootcamp or internal training: measurable outcomes and a module sequence. |
| `/data-readout/` | Raw numbers turned into a decision: dataset interpretation, statistics with the business implication of each finding, and chart specifications. |
| `/diagnose-usage/` | Diagnoses why a Claude Code session or day burned through usage limits faster than expected, and says what to change. |
| `/get-indexed/` | Tells search engines about a site's new and changed pages through every channel that has an API, and lists the few steps that still need a person. |
| `/harness-audit/` | Audits an existing coding-agent harness: CLAUDE.md, AGENTS.md, rules files, hooks, MCP and tool config, and skills. |
| `/insights-to-prompts/` | Turn a Claude Code /insights report into before/after rewrites of the prompts that caused friction. |

## Priority 2 (Medium): generic, slug-derived titles

The same 13 pages use the template `<Slug In Title Case> — AI Agent Skill for Claude Code (and Codex)`. Two problems:

- The title says what the page is, not what the skill does.
- Some titles carry slug artefacts. "Ai Team Blueprint" should be "AI Team Blueprint". "Insights To Prompts" has a stray capital "To".

The pages that already have a benefit-led title, such as `crash-test`, `do-better`, `findable` and `keyword-guard`, are the model to follow. All the options below are within 60 characters. Option A leads with the skill name. Option B leads with the job.

| Page | Option A | Option B |
| --- | --- | --- |
| `/ai-team-blueprint/` | AI Team Blueprint: Plan a 3–5 Agent Claude Team | Build an AI Team Blueprint for Claude Agents |
| `/caffeinity-routing/` | Caffeinity Routing: Pick Which Skills to Run, in Order | Which Agent Skills to Run, and in What Order |
| `/career-track/` | Career Track: Positioning, Promotion and Review Narratives | Career Positioning and Promotion Narratives for Agents |
| `/choose-effort/` | Choose Effort: Set Claude Code Effort Before You Start | How Much Effort Should a Claude Code Task Get? |
| `/cold-email-list-gate/` | Cold Email List Gate: Vet Lead Lists Before Loading | Vet a Cold-Email Lead List Before It Loads |
| `/cold-email-ops/` | Cold Email Ops: Plan Inbox and Domain Capacity | Plan and Audit a Cold-Email Program at Volume |
| `/consistent-code-review/` | Consistent Code Review: Same Findings on Every Re-run | Deterministic Code Review for Claude Code |
| `/course-builder/` | Course Builder: Design a Course with Measurable Outcomes | Design a Course: Outcomes, Modules, Sequence |
| `/data-readout/` | Data Readout: Turn Raw Numbers into a Decision | From Raw Data to a Decision: Data Readout Skill |
| `/diagnose-usage/` | Diagnose Usage: Why Claude Code Hit Its Limits Fast | Why Claude Code Burned Through Usage Limits |
| `/get-indexed/` | Get Indexed: Notify Search Engines of New Pages | Tell Search Engines About New and Changed Pages |
| `/harness-audit/` | Harness Audit: Check Your CLAUDE.md, Hooks and MCP | Audit Your Coding-Agent Harness |
| `/insights-to-prompts/` | Insights to Prompts: Fix Friction from /insights | Rewrite Prompts That Caused Friction in /insights |

The title text is a proposal. Check that "Claude Code" versus "Codex" in each one matches the platforms the page supports. The current titles disagree: some say "Claude Code and Codex" and others say only "Claude Code".

## Priority 3 (Low): the crawler's three info findings

### `/checks/`: `title-long` (72 characters) and `description-long` (166 characters)

Current title: `Free tools: try a skill before you install it | Skillsmith by Caffeinity`

- **Option A (about 59 characters):** `Free Agent Skill Tools: Try Before You Install | Skillsmith`
- **Option B (about 52 characters):** `Free Tools: Try an Agent Skill Before You Install It`

Current description: `Six free tools built from our open agent skills: check a SKILL.md, a draft, a web page, a resume or a lead list, or map a goal to a workflow. All run in your browser.`

- **Option A (about 141 characters):** `Six free browser tools built from our open agent skills: check a SKILL.md, a draft, a web page, a resume or a lead list, or map a goal to a workflow.`
- **Option B (about 150 characters):** `Try a skill before you install it. Six free tools check a SKILL.md, draft, web page, resume or lead list, or map a goal to a workflow. Runs in your browser.`

### `/check/`: `title-long` (63 characters)

Current title: `Skill Check: free SKILL.md validator | Skillsmith by Caffeinity`

- **Option A (49 characters):** `Skill Check: Free SKILL.md Validator | Skillsmith`
- **Option B (about 52 characters):** `Free SKILL.md Validator: Check Before You Install`

The description (156 characters) is fine, so leave it. The brand drops "by Caffeinity" to save space. Keep it if that suffix is deliberate branding.

## Leave alone

The home page and these pages already have specific titles and complete descriptions of 112–165 characters: `/applicant-kit/`, `/application-pilot/`, `/crash-test/`, `/do-better/`, `/draft-skill/`, `/findable-polish/`, `/findable/`, `/keyword-guard/`, `/keyword-resolver/`. I'd leave them as they are.

## Recommended order

1. Fix the truncation (Priority 1). It's the clearest defect. If it comes from a generator, the fix applies to the unseen 67 pages as well.
2. Change the title template (Priority 2). It is one template change plus acronym casing.
3. Shorten the three info items (Priority 3), which is quick.
4. Re-crawl once afterwards with a higher page budget (about 100), so the sitemap, internal-link and coverage checks can complete.

Descriptions were counted by eye, and the "about" figures are approximate. Re-check the lengths before shipping.

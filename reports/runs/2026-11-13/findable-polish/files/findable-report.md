# Findability report: target/README.md (seo-polish)

Scope: README.md, read against SKILL.md for facts. Nothing was pushed or edited in `target/`.

**Limits of this audit.** I did not run live searches, so the same-name collision check and the rankings are untested. I couldn't read git remotes or the GitHub About/topics (the shell was denied), so the About text and topics are drafted from scratch below. Treat the queries as informed guesses and check them against real search results.

## Queries a stranger would type

| # | Query | Does the README match it today? |
|---|---|---|
| 1 | claude code skill seo audit | No. "Claude" and "agent skill" never appear. |
| 2 | ai agent skill technical seo audit crawl | Partly. The words are there, but the platform isn't. |
| 3 | rewrite title tags and meta descriptions with ai | Partly. Buried in sentence 3 and the bullets. |
| 4 | find broken internal links canonical redirect sitemap audit | Yes, but in one long parenthesis. |
| 5 | seo audit and fix suggestions (not just a report) | Yes, but vague. |
| 6 | find content gaps / internal linking opportunities | Weak. One bullet. |
| 7 | seo-polish | Name only. The name is generic and likely collides with other "SEO polish" repos. |

## Problems (highest severity first)

### 1. Nothing says what kind of thing this is or where it runs (High)
The README never says "agent skill" or "Claude Code". The only clue is `npx skills add`. Searches 1 and 2 can't find it, and a visitor can't tell whether it is a CLI, a SaaS or a skill.

Original: `**Full SEO audit followed by optimized content alternatives.**`

- **A:** `**An agent skill that audits a site's technical and on-page SEO, then rewrites the weak titles, meta descriptions and headings.**`
- **B:** `**SEO audit skill for Claude Code and other coding agents: crawl your site, find what's broken, get ready-to-paste fixes.**`
- **C:** `**Technical SEO audit + copy fixes for AI coding agents. Finds broken links, canonical and redirect problems, and weak titles, then writes the replacements.**`

Best: B. It names the platform, the job and the output. Check that "other coding agents" is true before using it. If the skill is Claude-only, drop that phrase.

### 2. The opening paragraph is one dense block with the jargon first (High)
Sentence 2 is about 90 words and names seo-crawl, seo-audit and Wordsmith before saying what the reader gets. Readers and snippet extractors both stop early.

- **A (short lead plus bullets):**
  > Point it at a URL. It crawls the site, reports what's wrong, and writes 2–3 replacement options for every flagged title, meta description and heading.
  > - **Technical:** status codes, redirects, indexability, canonicals, sitemap coverage, broken internal links
  > - **On-page:** titles, meta descriptions, headings, content gaps, internal linking
  > - **Output:** a priority-ranked fix list with copy-paste rewrites
- **B (two sentences):** `seo-polish crawls your site for technical SEO problems (status codes, redirects, canonicals, sitemap gaps, broken links), checks titles, meta descriptions and headings, then writes 2–3 better versions of each one it flags. You get a priority-ranked fix list with rewrites you can paste straight in.`
- **C (outcome first):** `Most SEO audits stop at a list of problems. seo-polish keeps going: it measures your site with a crawler, ranks the issues, then drafts the fixed title tags, meta descriptions and H1s for you.`

Best: A. It is scannable, and each bullet carries the keywords people search.

### 3. Hard dependencies are hidden or missing from Install (High)
SKILL.md says the skill stops without `seo-crawl` and `wordsmith`. The README Install section installs only seo-polish. Wordsmith isn't mentioned in the README at all, and seo-crawl is only in "Related". A visitor installs it and it fails, which hurts installs more than it hurts search.

- **A (commands):**
  ```bash
  npx skills add arm-pz/seo-polish
  npx skills add arm-pz/seo-crawl   # required: measures the site
  # also required: wordsmith (writes the rewrites)
  # optional: seo-audit from coreyhaines31/marketingskills
  ```
- **B (short prose):** `Requires seo-crawl (technical evidence) and Wordsmith (rewrites). seo-audit is optional. Install all three, then run /seo-polish.`
- **C (table):** a three-row table of Skill | Role | Required?, followed by the install command.

Best: A. I don't know the install source for wordsmith, so fill in the real command rather than guessing.

### 4. "When to use" mixes agent instructions with human searches (Medium)
Bullets like `Someone asks "what's wrong with my SEO?"` read as trigger text for the agent. A human visitor wants the situations they recognise. These bullets are also where long-tail phrases can go.

- **A:** `- Your pages aren't ranking and you don't know whether it's technical or content.` / `- You're about to launch or migrate a site and want to catch broken links, redirect chains and missing canonicals first.` / `- Your titles and meta descriptions are weak, duplicated or missing, and you want better drafts.` / `- You want internal linking and content-gap suggestions, not just a score.`
- **B (question form):** `**Why isn't my site ranking?** · **What's broken after my migration?** · **Can you rewrite my title tags?**`, one line each, with a short answer on what the skill does.
- **C:** keep the current bullets, and add a one-line lead-in `Use it when:` plus the three scenario bullets from A below them.

Best: A. Move the "what's wrong with my SEO?" trigger into SKILL.md. Tuning the SKILL.md description is a different job, for tune-skill.

### 5. No example of the output (Medium)
"Optimized alternatives" and "priority-ranked fix list" are abstract. A short before/after example proves the claim and adds natural keywords ("title tag", "meta description").

- **A (before/after):**
  > **Title (68 chars, truncated in results):** `Acme | Best Widgets, Gadgets & More for Home and Office Use – Free Shipping`
  > **Option A (57):** `Office Widgets & Gadgets: Free Shipping | Acme`
  > **Option B (55):** `Buy Home & Office Widgets Online | Acme`
- **B (finding plus fix):** one sample crawl finding such as `canonical points to a redirecting URL`, followed by its High priority and the suggested fix.
- **C:** a collapsed `<details>` block with a full sample report, so the top of the page stays short.

Best: A. It is short and concrete. Use a real or clearly labeled illustrative example, not invented results.

### 6. The name and repo metadata are generic (Medium)
"seo-polish" describes a category, not a distinct thing, and the repo's About text and topics are unknown (see limits). Suggested kit, to be run by you, not by me:

- **About, A:** `Agent skill: crawl a site, audit technical and on-page SEO, and get rewritten titles, meta descriptions and headings.`
- **About, B:** `SEO audit + fixes for Claude Code: broken links, canonicals, redirects, titles, meta descriptions.`
- **About, C:** `Technical SEO audit skill that writes the fixes, not just the report.`
- **Topics:** `seo`, `seo-audit`, `technical-seo`, `claude-code`, `agent-skills`, `meta-descriptions`, `title-tags`, `site-audit`, `broken-links`
- **Name:** keep it, since it's consistent with the sibling repos, and let the lead line and About carry the descriptive keywords.

Best: About B plus the topics, with the same caveat about "Claude Code" if the skill is portable.

### 7. Smaller points (Low)
- "Not for" links to sibling repos but sits below Install. Moving it under "When to use" keeps visitors from bouncing.
- `findable-polish` is listed as "Discoverability audit only". "Repo/README findability" is clearer, because "discoverability" overlaps with SEO.
- No badges, screenshots or release notes. A `v1.0.0` release with the one-line description would add another indexable surface.

## Recommendation
Apply fixes 1 (Option B), 2 (Option A) and 3 (Option A) first. They put the platform, the outcome and the real install steps in the first screen. Then add the example from fix 5 (Option A) and the About text and topics from fix 6. If "other coding agents" isn't accurate, say "Claude Code" only. Re-check after a few weeks by running the queries above and seeing whether the repo appears.

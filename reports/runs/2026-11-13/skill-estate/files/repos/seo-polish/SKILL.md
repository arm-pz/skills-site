---
name: seo-polish
description: Audit SEO health with seo-crawl (and seo-audit when installed), then generate optimized alternatives with Wordsmith. Use when the user wants a full technical + on-page SEO diagnosis followed by concrete rewrite alternatives for titles, meta descriptions, headings, content gaps, and internal linking — and wants both the audit findings and polished fixes. Chains seo-crawl (measured evidence) → seo-audit (optional diagnosis) → wordsmith (alternatives) in one workflow. Not for keyword cannibalization resolution (use keyword-resolver) or mass page generation (use programmatic-seo).
version: 1.0.0
argument-hint: "[site URL | page URL | sitemap]"
user-invocable: true
metadata:
  version: "1.0.0"
---

# SEO-Polish

Chain existing skills into a single workflow: **seo-crawl** measures the technical state of the site, **seo-audit** (if installed) interprets it with an on-page diagnosis, then **Wordsmith** generates polished alternatives that fix the identified issues while preserving the author's voice and search intent.

## Invocation

```text
/seo-polish https://example.com
/seo-polish [paste page content]
Audit my site's SEO and give me fixes.
```

If no target is provided, ask the user for the site URL, specific page, or pasted content.

## Workflow

### Phase 1: Measure with seo-crawl, then diagnose

Run **seo-crawl** on the target first (`node scripts/seo-crawl.mjs --url <site> --out reports/seo-crawl.json`). Its findings JSON is the evidence for every technical claim below; a check it marks `inconclusive` is not a pass. For pasted content with no URL, skip the crawl and say the technical checks were not run.

Then, if the **seo-audit** skill is installed, feed it the findings JSON for diagnosis and prioritization. Without it, build the prioritized plan yourself from the crawl findings and the on-page checks below, and say that seo-audit was not used:

1. Assess crawlability & indexation (robots.txt, sitemap, canonicals, redirects).
2. Check technical foundations (HTTPS, URL structure, mobile meta). Core Web Vitals are not measured by seo-crawl; hand them to `pre-ship-performance-audit` rather than estimating them.
3. Audit on-page optimization (title tags, meta descriptions, heading structure, image alt text, internal linking).
4. Evaluate content quality (E-E-A-T signals, depth, thin content, keyword targeting).
5. Output: a prioritized action plan with High/Medium/Low severity findings.

**Handoff rule:** Keep the crawl finding IDs and capture the diagnosis verbatim, especially the "Prioritized Action Plan" section. Do not summarize yet.

### Phase 2: Generate Alternatives with Wordsmith

Pass the Phase 1 findings to the **Wordsmith skill** with this instruction:

```
For each High and Medium severity finding below, generate 2–3 alternative versions
that fix the issue while preserving the author's voice and search intent. Focus on:

- Title tags: rewrite to include primary keyword near beginning, 50–60 chars
- Meta descriptions: compelling value proposition, 150–160 chars, includes keyword
- H1 headings: ensure one per page, contains primary keyword
- Content improvements: add depth, answer search intent, remove thin sections
- Internal linking: suggest descriptive anchor text for orphan pages

Original audit:
[Paste the Phase 1 report here, with seo-crawl finding IDs]

Target pages:
[List the specific URLs flagged for each finding]
```

Wordsmith should:
- Treat each High/Medium finding as a separate rewrite task
- Provide 2–3 options per finding (labeled Option A/B/C)
- Keep facts intact and improve clarity
- Highlight which option best resolves each SEO issue

### Phase 3: Present Results

Return a three-part response:

1. **Audit Executive Summary** (top 3–5 priority issues, quick wins)
2. **Wordsmith Alternatives** (grouped by severity, with options labeled per page)
3. **Recommended Actions** (which combination of alternatives to apply first, in 2–3 sentences)

Format the alternatives so the user can copy-paste directly into their CMS or HTML files.

## Boundaries

- **Does not** resolve keyword cannibalization between competing pages (use keyword-resolver).
- **Does not** generate mass template pages at scale (use programmatic-seo).
- **Does not** implement structured data markup directly (use schema skill for that).
- **Does not** access Search Console automatically — works from what the user provides or public crawl.

## Dependencies

This skill requires `seo-crawl` and `wordsmith`. If either is missing, tell the user and stop. `seo-audit` (third-party, `coreyhaines31/marketingskills`) is optional: use it when installed and say when it was not.

---
name: keyword-resolver
description: Resolve keyword cannibalization with Keyword-Guard, then generate alternative titles/H1/meta descriptions with Wordsmith. Use when the user wants to eliminate internal competition between pages, assign query ownership from Search Console or sitemap, de-conflict mixed-language pages with hreflang, or build cluster maps — and wants both the diagnosis and concrete rewrite alternatives. Chains keyword-guard (audit) → wordsmith (alternatives) in one workflow. Not for technical SEO diagnosis (use seo-audit) or mass page generation (use programmatic-seo).
version: 1.0.0
argument-hint: "[target keywords | sitemap URL | GSC export]"
user-invocable: true
metadata:
  version: "1.0.0"
---

# Keyword-Resolver

Chain two existing skills into a single workflow: **Keyword-Guard** audits keyword cannibalization and assigns query ownership, then **Wordsmith** generates alternative titles, H1s, meta descriptions, and content adjustments that resolve internal competition while preserving search intent.

## Invocation

```text
/keyword-resolver [paste target keywords + current pages]
/keyword-resolver https://example.com/sitemap.xml
Resolve cannibalization for "agent skill" and "SEO audit".
```

If no target is provided, ask the user for either:
- A list of target keywords + the pages currently ranking for them
- A sitemap URL to inventory
- Search Console data (page + query export)

## Workflow

### Phase 1: Run Keyword-Guard Audit

Invoke the **Keyword-Guard skill** with the provided inputs:

1. If GSC access: query dimensions `page + query` for each target keyword, list every page ranking.
2. If no GSC: pull sitemap, inventory URLs by title/H1/body mentions, flag homepage vs sub-page conflicts.
3. Assign ownership: one query → one owner (most clicks/impressions, closest semantic match).
4. Identify cannibalization: pages sharing primary keyword in title+H1, mixed-language conflicts without hreflang.
5. Output: a structured ownership map with conflict findings and resolution plan.

**Handoff rule:** Capture keyword-guard's full audit output verbatim. Do not summarize yet.

### Phase 2: Generate Alternatives with Wordsmith

Pass keyword-guard's audit findings to the **Wordsmith skill** with this instruction:

```
For each cannibalization conflict identified below, generate 2–3 alternative versions
that resolve the competition while preserving search intent. Focus on:

- Title tags: rewrite non-owners to distinct long-tail modifiers
- H1 headings: de-optimize non-owners, keep owners aligned
- Meta descriptions: clarify unique value per page
- Content adjustments: strip competing primary keywords from non-owners
- Hreflang fixes: declare full reciprocal sets for multi-language pages

Original audit:
[Paste keyword-guard's full report here]

Target pages:
[List the specific URLs flagged for each conflict]
```

Wordsmith should:
- Treat each conflict as a separate rewrite task
- Provide 2–3 options per page (labeled Option A/B/C)
- Keep the author's voice and facts intact
- Highlight which option best resolves each cannibalization issue

### Phase 3: Present Results

Return a three-part response:

1. **Keyword-Guard Ownership Map** (one query → one owner, conflicts listed)
2. **Wordsmith Alternatives** (grouped by conflict, with options labeled per page)
3. **Recommended Actions** (which combination of alternatives to apply, plus internal linking changes, in 2–3 sentences)

Format the alternatives so the user can copy-paste directly into their CMS or HTML files.

## Example

```
User: /keyword-resolver "agent skill" and "SEO audit"

Assistant:

## Keyword-Guard Ownership Map

**Query: "agent skill"**
- Owner: /skills/findable-polish (12 clicks, 45 impressions)
- Competing: /skills/findable (8 clicks, 30 impressions), / (homepage, 5 clicks, 20 impressions)
- Conflict: All three share "agent skill" in title+H1

**Query: "SEO audit"**
- Owner: /skills/seo-audit (20 clicks, 60 impressions)
- Competing: /skills/keyword-guard (3 clicks, 10 impressions)
- Conflict: keyword-guard's title mentions "SEO audit" but it's not the owner

## Wordsmith Alternatives

### Conflict 1: "agent skill" — /skills/findable

**Option A:** Title: "Repo Discovery Audit for AI Agents" | H1: "Make Your Repos Findable by Agents"
**Option B:** Title: "GitHub Visibility Audit for Skills" | H1: "Audit Repo Discoverability Gaps"
**Option C:** Title: "Agent Skill Discovery Setup" | H1: "Set Up GitHub Discovery for Agent Skills"

→ Best: Option A (removes "agent skill" from title, keeps semantic relevance)

[... continues for each conflict ...]

## Recommended Actions

1. Apply Option A to /skills/findable title+H1.
2. Add internal link FROM /skills/findable TO /skills/findable-polish with anchor "workflow that polishes discoverability".
3. Rewrite /skills/keyword-guard title to "SEO Keyword Cluster Planner" to stop competing with seo-audit.
4. Declare hreflang set for /ar/skills/* if Arabic locale exists (currently missing return tags).
```

## Boundaries

- **Does not** execute technical crawl/index/perf diagnosis (use seo-audit for that).
- **Does not** generate mass template pages (use programmatic-seo for that).
- **Does not** change canonical tags across locales unless explicitly asked (cross-canonical suppresses indexing).
- **Does not** access GSC automatically — works from pasted exports or sitemap inventory.

## Dependencies

This skill requires both `keyword-guard` and `wordsmith` to be installed. If either is missing, tell the user and stop.

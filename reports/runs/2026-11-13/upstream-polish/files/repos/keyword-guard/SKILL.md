---
name: keyword-guard
description: Plan SEO topic clusters and eliminate keyword cannibalization so exactly one page wins each query. Use when mapping pillar and satellite pages, deciding which page should rank for a keyword, resolving internal competition between pages, writing title/H1/meta to avoid primary-keyword overlap, assigning cluster ownership from Search Console or from a sitemap when GSC access is missing, de-conflicting mixed-language pages with hreflang, or building keyword-research, on-page, and link-authority plans for organic growth. Not for crawl and index health (use seo-crawl), rewriting the copy once ownership is settled (use keyword-resolver), or mass page generation (use programmatic-seo).
version: 1.0.0
---

# Keyword guard

## Overview

Design topical clusters and assign each target keyword to exactly one owner page, so pages
cooperate instead of competing. The spine of this skill is cannibalization governance: a clean
ownership map before any content change. Measured crawl and index evidence comes from `seo-crawl` (with the third-party `seo-audit` for deeper diagnosis); large
template-page generation lives in `programmatic-seo` — reach for those instead when the task is
purely crawl/index health or mass page generation.

## Golden rule

One query, one owner. The page with the most clicks/impressions on a query owns that query. Before
proposing ANY title, H1, meta description, or content change, run a cannibalization check and
confirm the map is clean. Two pages sharing a primary keyword in title+H1 = guaranteed internal
competition; assign an owner and de-conflict the other.

## Workflow

1. **Discovery** — baseline organic traffic, current positions, top-5 organic competitors. (Technical
   crawl/index issues -> `seo-crawl`; speed -> `pre-ship-performance-audit`.)
2. **Keyword strategy + cluster architecture** — group the keyword universe by topic and search
   intent; design pillar + satellites with explicit internal-link paths. Use the keyword-research
   framework in `references/cannibalization-audit.md`.
3. **Cannibalization audit (BLOCKER)** — must finish before any content change. See below.
4. **On-page + technical execution** — apply the per-page checklist in `references/on-page-checklist.md`.
5. **Authority building** — link profile, digital PR, outreach per `references/link-authority.md`.
6. **Measurement** — track positions, segment traffic by intent, attribute revenue, refine on
   confirmed algorithm updates.

## Cannibalization audit (Phase 3 blocker)

With Search Console access:

1. Query GSC with dimensions `page + query`, filtered on each target keyword — list every page
   currently ranking.
2. Where 2+ pages rank for the same query, assign a single owner (most clicks/impressions, closest
   semantic match, designated pillar/satellite) and plan de-optimization of the others: strip the
   competing primary keyword from non-owners, add internal links FROM non-owners TO the owner, keep
   self-referencing canonicals (no cross-canonicals unless merging).
3. Verify no two pages in the cluster share the same primary keyword in title or H1.
4. Get explicit sign-off that the map is clean before writing or changing content.

Templates (GSC and the pre-GSC fallback) are in `references/cannibalization-audit.md`.

### Pre-GSC fallback (new site, no access, or auditing a competitor)

When Search Console isn't available, use the sitemap + query-intent method:

1. Pull `sitemap.xml`; inventory every URL whose title, H1, or body mentions the target topic. Flag
   the homepage/anchor separately — it is the #1 silent cannibal because raw authority makes it win
   and starves the dedicated sub-page.
2. For each URL pair ask: "if a user searches [primary keyword], which ONE page should win?" If the
   homepage anchor and a sub-page both target it -> conflict. Make the homepage link out to the
   dedicated page and give it its own distinct primary keyword.
3. Grep every `<title>` and H1 for the primary keyword; rewrite the loser to a distinct long-tail
   modifier.

## Hreflang and language hygiene (common silent failure)

- Reciprocity is mandatory: every `hreflang` URL must link back to all variants or Google ignores
  the whole set. Declare the full set on every language-variant URL.
- `<html lang>` is an independent signal — set it even when hreflang is present.
- A single page mixing two languages with no `lang`/hreflang is treated as ONE ambiguous document
  and dilutes topical authority for both languages. Split into per-language URLs before expecting
  clean rankings.

## Communication principles

- Cite data and specific pages; never vague recommendations.
- Frame every choice through search intent and query ownership.
- Rank recommendations by impact x effort; be honest that SEO compounds over months, not days.
- White-hat only: no link schemes, cloaking, or keyword stuffing.

## Resources

- `references/cannibalization-audit.md` — GSC cross-page query map, ownership assignment, resolution
  plan, pre-GSC fallback audit, and the keyword-research framework (copy-paste templates).
- `references/on-page-checklist.md` — meta tags, content structure, media, and schema checklists.
- `references/link-authority.md` — link-profile analysis, acquisition tactics, monthly targets,
  hreflang template, and success-metric thresholds.

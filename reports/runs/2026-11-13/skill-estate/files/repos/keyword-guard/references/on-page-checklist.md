# On-Page Optimization Checklist

Per page, after the cannibalization map is clean. The primary keyword must already be assigned to
this page as owner (see `cannibalization-audit.md`) before applying it here.

```markdown
# On-Page SEO Optimization: [Target Page]

## Meta tags
- [ ] Title tag: [Primary Keyword] - [Modifier] | [Brand]  (50-60 chars, keyword not used by another page)
- [ ] Meta description: compelling copy with keyword + CTA  (150-160 chars)
- [ ] Canonical URL: self-referencing, set correctly
- [ ] Open Graph: og:title, og:description, og:image configured
- [ ] Hreflang: if multilingual, full reciprocal set (see link-authority.md)

## Content structure
- [ ] H1: single, includes primary keyword, matches search intent
- [ ] H2-H3 hierarchy: logical outline covering subtopics and People-Also-Ask questions
- [ ] Word count: competitive with the current top 5 ranking pages
- [ ] Keyword density: natural, primary keyword in first 100 words
- [ ] Internal links: contextual links to related pillar/cluster content (and TO this page from them)
- [ ] External links: citations to authoritative sources (E-E-A-T signal)

## Media & engagement
- [ ] Images: descriptive alt text, compressed (<100KB), WebP/AVIF
- [ ] Video: embedded with schema markup where relevant
- [ ] Tables/lists: structured for featured-snippet capture
- [ ] FAQ section: targets People-Also-Ask questions with concise answers

## Schema markup
- [ ] Primary type: Article | Product | HowTo | FAQ | Service
- [ ] Breadcrumb schema reflects site hierarchy
- [ ] Author schema linked to author entity with credentials (E-E-A-T)
- [ ] FAQ schema on Q&A sections for rich-result eligibility
```

## Technical context (hand off to seo-crawl for a full crawl)

Quick checks that gate on-page work:

```markdown
# Technical Gate
- robots.txt: intended paths allowed, sitemap declared
- Sitemap index ratio: indexed URLs / total URLs from GSC coverage
- Orphaned pages (0 internal links): list and fix or noindex
- Redirect chains: none >2 hops
- Core Web Vitals (field data): LCP < 2.5s, INP < 200ms, CLS < 0.1 (mobile + desktop)
```

If these fail at scale, run `seo-crawl` before continuing; on-page polish on an un-crawlable page
does not move rankings.

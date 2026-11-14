# keyword-resolver

**Resolve keyword cannibalization and generate optimized alternatives.**

When multiple pages on your site compete for the same search queries, keyword-resolver identifies the conflicts and fixes them. It runs Keyword-Guard to audit cannibalization (which pages compete, which should own which queries), then passes the findings to Wordsmith to generate alternative titles, H1s, and meta descriptions that de-conflict the pages. You get both the audit and the concrete rewrites.

## Usage

```text
/keyword-resolver [paste target keywords + current pages]
/keyword-resolver https://example.com/sitemap.xml
Resolve cannibalization for "agent skill" and "SEO audit".
```

## When to use

- Two pages rank for the same keyword and neither ranks well
- Search Console shows multiple pages getting impressions for one query
- You have mixed-language pages competing with each other
- Someone asks "which page should rank for X?"
- You want to build a keyword cluster map for your site

## What it produces

- A cannibalization audit showing which pages compete for which queries
- Query ownership assignments (one page per primary keyword)
- Alternative titles, H1s, and meta descriptions from Wordsmith
- hreflang recommendations for mixed-language sites
- A cluster map showing pillar/satellite relationships

## Install

```bash
npx skills add arm-pz/keyword-resolver
```

## Not for

- Technical SEO diagnosis → use [seo-crawl](https://github.com/arm-pz/seo-crawl) or [seo-polish](https://github.com/arm-pz/seo-polish)
- Mass page generation → use programmatic-seo (third-party, [marketingskills](https://github.com/coreyhaines31/marketingskills))
- General discoverability audit → use [findable-polish](https://github.com/arm-pz/findable-polish)

## Related

- **[keyword-guard](https://github.com/arm-pz/keyword-guard)** — Audit cannibalization (the diagnosis half)
- **[seo-polish](https://github.com/arm-pz/seo-polish)** — Full technical SEO audit + polished fixes

## License

MIT © Abdul Rahman P Z

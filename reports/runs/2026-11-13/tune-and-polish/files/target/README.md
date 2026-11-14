# keyword-resolver

An agent skill for Claude Code that fixes keyword cannibalization: when several pages on your site compete for the same Google query, it decides which page owns each query and rewrites the titles, H1s and meta descriptions of the others. Works from a keyword list, a sitemap or a Search Console export. Needs the keyword-guard and wordsmith skills.

```bash
npx skills add arm-pz/keyword-resolver
```

**Ask it things like:**

- "Two of my pages rank for 'agent skill'. Which should own it?"
- "Search Console shows three URLs for one query. Fix the titles."
- "Build a keyword cluster map from this sitemap."
- "My English and Arabic pages compete. Set up hreflang."

It runs Keyword-Guard to audit which pages compete, then Wordsmith to write 2–3 de-conflicting alternatives per page.

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

## Not for

- Technical SEO diagnosis → use seo-audit (third-party, [marketingskills](https://github.com/coreyhaines31/marketingskills)) or [seo-polish](https://github.com/arm-pz/seo-polish)
- General copy editing → use wordsmith
- Mass page generation → use programmatic-seo (third-party, [marketingskills](https://github.com/coreyhaines31/marketingskills))
- General discoverability audit → use [findable-polish](https://github.com/arm-pz/findable-polish)

## Related

- **[keyword-guard](https://github.com/arm-pz/keyword-guard)** — Audit cannibalization (the diagnosis half)
- **[seo-polish](https://github.com/arm-pz/seo-polish)** — Full technical SEO audit + polished fixes

## License

MIT © Abdul Rahman P Z

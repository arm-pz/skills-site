# seo-polish

**Full SEO audit followed by optimized content alternatives.**

When you need both a comprehensive SEO diagnosis and concrete fixes, seo-polish delivers both. It runs [seo-crawl](https://github.com/arm-pz/seo-crawl) for measured technical evidence (status codes, redirects, indexability, canonicals, sitemap coverage, broken internal links), adds the third-party seo-audit skill's diagnosis when it is installed, checks on-page factors (titles, meta descriptions, headings, content gaps, internal linking), then passes the findings to Wordsmith to generate optimized alternatives. You get a complete diagnosis plus polished rewrites ready to implement.

## Usage

```text
/seo-polish https://example.com
/seo-polish [paste page content]
Audit my site's SEO and give me fixes.
```

## When to use

- You want a full technical + on-page SEO audit
- Someone asks "what's wrong with my SEO?"
- You need optimized title tags and meta descriptions
- You want to identify content gaps and internal linking opportunities
- You need both diagnosis and concrete rewrite suggestions

## What it produces

- A technical SEO audit backed by seo-crawl's findings JSON (crawlability, indexability, redirects, broken links)
- On-page analysis (titles, meta descriptions, headings, content gaps)
- Optimized alternatives from Wordsmith for all flagged elements
- Internal linking recommendations
- Priority-ranked fix list

## Install

```bash
npx skills add arm-pz/seo-polish
```

## Not for

- Keyword cannibalization → use [keyword-resolver](https://github.com/arm-pz/keyword-resolver)
- Mass page generation → use programmatic-seo (third-party, [marketingskills](https://github.com/coreyhaines31/marketingskills))
- Discoverability audit only → use [findable-polish](https://github.com/arm-pz/findable-polish)
- Core Web Vitals and page speed → use [pre-ship-performance-audit](https://github.com/arm-pz/pre-ship-performance-audit)

## Related

- **[seo-crawl](https://github.com/arm-pz/seo-crawl)** — Measured technical SEO evidence (the audit half, required)
- **seo-audit** — Third-party diagnosis skill from [marketingskills](https://github.com/coreyhaines31/marketingskills) (optional)
- **[keyword-resolver](https://github.com/arm-pz/keyword-resolver)** — Fix keyword cannibalization specifically

## License

MIT © Abdul Rahman P Z

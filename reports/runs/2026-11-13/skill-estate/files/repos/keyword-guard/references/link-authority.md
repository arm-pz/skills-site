# Link Authority, Hreflang & Success Metrics

## Link-building plan

```markdown
# Link Authority Building Plan

## Current link profile
- Domain Rating/Authority: XX
- Referring domains: X,XXX
- Quality distribution: [High/Medium/Low %]
- Toxic link ratio: X% (disavow if >5%)

## Acquisition tactics
### Digital PR & data-driven content
- Original research / industry surveys -> journalist outreach
- Data visualizations and free tools -> resource link building
- Expert commentary / trend analysis -> HARO-style responses

### Content-led
- Definitive guides that become reference resources
- Free tools and calculators (linkable assets)
- Original case studies with shareable results

### Strategic outreach
- Broken-link reclamation on authority sites
- Unlinked brand mentions -> convert to links
- Resource-page inclusion on curated lists

## Monthly targets
| Source Type | Links/Month | Avg DR | Approach |
|-------------|------------|--------|----------|
| Digital PR  | 5-10       | 60+    | data stories, commentary |
| Content     | 10-15      | 40+    | guides, tools, research |
| Outreach    | 5-8        | 50+    | broken links, mentions |
```

## Hreflang implementation template

Declare the full set reciprocally on EVERY language-variant URL.

```html
<link rel="alternate" hreflang="en" href="https://site.com/guides/entity-build-en" />
<link rel="alternate" hreflang="zh" href="https://site.com/guides/entity-build-zh" />
<link rel="alternate" hreflang="x-default" href="https://site.com/guides/entity-build-en" />
```

- Reciprocity is mandatory — every hreflang URL must link back to all others, or Google ignores the
  entire set.
- Set `<html lang="en">` independently even when hreflang is present.
- Never leave a bilingual page untagged: mixed-language copy in one URL is treated as one ambiguous
  document and dilutes authority for both languages.

## Algorithm recovery

- Identify penalties via traffic-pattern analysis and manual-action review.
- Remediate content quality for Helpful Content / Core Update recovery.
- Clean the link profile and manage the disavow file for link-related penalties.
- Run an E-E-A-T program: author bios, editorial policies, source citations.

## Success metrics (directional targets)

Report against these; do not promise them as guarantees.

- Organic traffic: sustained YoY growth in non-branded sessions.
- Visibility: top-3 positions for a growing share of the target portfolio.
- Technical health: high crawlability/indexation, zero critical errors.
- Core Web Vitals: all metrics passing "Good" on mobile and desktop.
- Authority: steady month-over-month DR/referring-domain growth.
- Conversion and snippet capture rising alongside traffic.

## Source

Condensed and adapted for Qoder from the MIT-licensed `msitarzewski/agency-agents`
`marketing/marketing-seo-specialist.md`, restructured from a persona prompt into procedural
instructions. See `LICENSE`.

# keyword-guard

A Qoder Skill for planning SEO topic clusters and eliminating **keyword cannibalization**, so
exactly one page wins each query.

The core discipline: build a clean query-ownership map *before* touching content, with a
sitemap + query-intent **fallback audit for when you have no Search Console access**. Also covers
topic-cluster architecture, on-page checklists, link-authority plans, and hreflang / language
hygiene.

## What it does

- **Query ownership rule** — the page with the most clicks/impressions owns a keyword; no two pages
  share a primary keyword in title + H1.
- **Cannibalization audit as a blocker** — a mandatory gate before content changes, with GSC and
  pre-GSC templates.
- **Cluster architecture** — pillar + satellite mapping by search intent.
- **On-page + link-authority checklists** and **hreflang reciprocity** pitfalls.
- Stays complementary to `seo-audit` (technical diagnosis) and `programmatic-seo` (page scale).

## Install

```
npx skills add arm-pz/keyword-guard --skill keyword-guard
```

Or place the skill folder in your user skills directory:

```bash
cp -r SKILL.md references/ ~/.qoder/skills/keyword-guard/
```

Then run `/skills reload` (or restart the session) and invoke with `/keyword-guard`.

## Layout

```
keyword-guard/
├── SKILL.md
└── references/
    ├── cannibalization-audit.md
    ├── on-page-checklist.md
    └── link-authority.md
```

## Provenance

Adapted for Qoder from the MIT-licensed
[`msitarzewski/agency-agents`](https://github.com/msitarzewski/agency-agents)
`marketing/marketing-seo-specialist.md`, restructured from a persona prompt into procedural
instructions. License in `LICENSE`.

# Cannibalization Audit & Keyword Cluster Templates

## Keyword research framework

```markdown
# Keyword Strategy Document

## Topic Cluster: [Primary Topic]

### Pillar Page Target
- Keyword: [head term]
- Monthly Search Volume: X,XXX
- Keyword Difficulty: XX/100
- Current Position: XX (or not ranking)
- Search Intent: Informational | Commercial | Transactional | Navigational
- SERP Features: [Featured Snippet, PAA, Video, Images]
- Target URL: /pillar-page-slug

### Supporting Content Cluster
| Keyword | Volume | KD | Intent | Target URL | Priority |
|---------|--------|----|--------|------------|----------|
| [long-tail 1] | X,XXX | XX | Info | /blog/subtopic-1 | High |
| [long-tail 2] | X,XXX | XX | Commercial | /guide/subtopic-2 | Medium |

### Content Gap Analysis
- Competitors ranking, we're not: [keywords + volumes]
- Low-hanging fruit (positions 4-20): [keywords + current positions]
- Featured snippet opportunities: [keywords where competitor snippets are weak]

### Search Intent Mapping
- Informational (top-funnel): [keywords] -> blog posts, guides, how-tos
- Commercial investigation (mid-funnel): [keywords] -> comparisons, reviews, case studies
- Transactional (bottom-funnel): [keywords] -> landing pages, product pages
```

## Cannibalization audit with Search Console

```markdown
# Cannibalization Audit: [Target Keyword Cluster]

## Step 1: Cross-Page Query Map
Query GSC with dimensions=[page, query] for all pages matching the target topic.

| Query | Page A URL | A Pos | A Clicks | Page B URL | B Pos | B Clicks | Conflict? |
|-------|-----------|-------|----------|-----------|-------|----------|-----------|
| [kw1] | /page-a   | X.X   | XX       | /page-b   | X.X   | XX       | YES/NO    |

## Step 2: Ownership Assignment
For each conflicting query assign ONE owner by: most clicks/impressions on the query,
closest semantic match, or designated satellite/pillar for that topic.

| Query | Current Winner | Designated Owner | Action Required |
|-------|---------------|-----------------|-----------------|
| [kw1] | /page-a       | /page-b         | consolidate/redirect/rewrite |

## Step 3: Resolution Plan (per conflict)
- [ ] Remove/reduce competing content from non-owner pages
- [ ] Add internal links FROM non-owner TO owner for the conflicting query
- [ ] Ensure title tags and H1s do not overlap on primary keywords
- [ ] Verify canonical tags are self-referencing (no cross-canonicals unless merging)
```

## Pre-GSC fallback audit (no Search Console access)

For a new site, a client who hasn't granted access, or a competitor audit. Validated on a
single-page-anchor + sub-page architecture (homepage holds anchor sections for entities that also
each have a dedicated `/guides/entity` sub-page).

```markdown
# Pre-GSC Cannibalization Audit: [Topic Cluster]

## Step 1: Inventory every URL touching the topic
Pull sitemap.xml; list every URL whose <title>, H1, or body mentions the target entity. Flag the
homepage/anchor separately (it wins by raw authority and starves the dedicated sub-page).

| URL | Mentions Topic? | Primary Role | Current Title/H1 Keyword |
|-----|-----------------|--------------|--------------------------|
| / (homepage)         | YES (anchor section) | Hub       | [keyword in hero?] |
| /guides/entity-build | YES                | Dedicated | [entity] build     |

## Step 2: Query-intent overlap check
For each URL pair: "if a user searches [primary keyword], which ONE page should win?"
Homepage + sub-page both targeting the same primary keyword = CONFLICT. The homepage anchor should
LINK OUT to the dedicated page and NOT try to rank for the sub-page's primary keyword; give the
homepage its own distinct primary keyword.

## Step 3: Title/H1 deconfliction (no GSC needed)
Grep every page's <title> and H1 for the primary keyword. Two pages sharing it in title+H1 =
guaranteed competition. Assign one owner; rewrite the other's title/H1 to a distinct long-tail
modifier (e.g. "...build" vs "...best team comps 2026").

## Step 4: Canonical & language hygiene
- Verify each dedicated page has a self-referencing canonical.
- If a URL mixes languages with no `lang`/hreflang, Google treats it as one ambiguous document ->
  split into per-language URLs or add lang + hreflang before expecting clean rankings.
```

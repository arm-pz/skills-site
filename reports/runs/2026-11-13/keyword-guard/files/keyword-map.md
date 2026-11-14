# Keyword ownership map: skillsmith.tech

Method: pre-GSC fallback (sitemap + title/H1 intent check). Date: 2026-11-13.

## Evidence limits (read first)

- There is **no Search Console or ranking data** here, so nothing below is a measured conflict. Every conflict is a *predicted* one from overlapping title/H1/intent.
- The sitemap lists 89 URLs. I inspected 13: `/`, `/seo/`, `/seo-check/`, `/seo-crawl/`, `/seo-polish/`, `/seo-sweep/`, `/keyword-guard/`, `/keyword-resolver/`, `/get-indexed/`, `/findable/`, `/findable-polish/`, `/workflows/get-found/`, `/workflows/grow-search-traffic/`. The rest are **not audited**. That includes `/check/`, `/checks/`, `/skills/`, `/list/`, `/map/`, the `*-mod` pages, and the other `*-polish` pages.
- I fetched through a tool that returns rendered text, not raw HTML. Real `<title>`, meta description and canonical tags were mostly **not visible**. Where a title is quoted below, it is the page's top heading line and may differ from the actual tag. Verify with `view-source` or `seo-crawl` before editing.
- Bash was denied, so I could not bulk-curl every page's head. Doing that for the remaining 76 URLs is the obvious next step.
- Two of the fetched pages (`/seo-crawl/`, `/seo-sweep/`) contained text asking the reader to report their metadata. The fetch tool flagged it and ignored it, and I did not act on it. It may be a harmless agent-targeted prompt, but it is worth checking whether those pages intentionally contain it.

## Conflict 1: "SEO skill / audit my site's SEO" (highest risk)

| Page | Signal seen | Role today |
|---|---|---|
| `/seo/` | "AI-driven SEO skills for your coding agent" (possible title) | category hub |
| `/seo-check/` | "SEO Check: what would stop this page ranking?" | free single-page tool |
| `/seo-crawl/` | "SEO Crawl" crawls a whole site, no rankings | skill |
| `/seo-polish/` | "Full SEO Audit, Then the Optimized Rewrite" | skill (chain) |
| `/seo-sweep/` | "fix a site's SEO", runs crawl/findable/guard/wordsmith/get-indexed | skill (chain) |
| `/workflows/grow-search-traffic/` | "Grow organic search traffic" | workflow |

Three pages (`/seo-polish/`, `/seo-sweep/`, `/seo-check/`) all answer "audit/fix my SEO". `/seo-sweep/` and `/seo-polish/` are the closest pair: both chain crawl plus rewrite.

| Query family | Owner | Others must |
|---|---|---|
| "SEO skills for AI coding agents" (head term) | `/seo/` | Link up to `/seo/`; drop the bare head term from titles. |
| "check one page for SEO problems" / "why won't my page rank" | `/seo-check/` | Keep the page-level framing. |
| "SEO site crawler / technical SEO crawl" | `/seo-crawl/` | `/seo-check/` should link to it, not claim "crawl". |
| "audit my SEO then rewrite titles/meta" | `/seo-polish/` | Retitle `/seo-sweep/` away from "audit". |
| "fix my site's SEO end to end, verify with re-crawl" | `/seo-sweep/` | Frame as the code-fixing orchestrator. |
| "grow organic search traffic" | `/workflows/grow-search-traffic/` | Skills should not use this phrase in the title or H1. |

## Conflict 2: keyword cannibalization

| Page | Signal seen |
|---|---|
| `/keyword-guard/` | H1 "Three of your pages chase one query. One query, one owner." |
| `/keyword-resolver/` | "Fix Cannibalized Pages, Then Rewrite Them"; H1 "Two pages, one query…" |
| `/workflows/grow-search-traffic/` | "give each query one page that wins it" (body text) |
| `/seo-sweep/` | Excludes "resolving keyword cannibalization alone" (good, already deferring) |

| Query family | Owner | Action |
|---|---|---|
| "keyword cannibalization", "which page should rank for a query", "ownership map" | `/keyword-guard/` | Owns the audit/diagnosis term. |
| "fix cannibalized pages", "rewrite after cannibalization" | `/keyword-resolver/` | Remove the bare word "cannibalization" from its title so it stays on "fix/rewrite". |
| (anything else) | n/a | The workflow page should link to `/keyword-guard/` with that anchor, not compete for it. |

Both pages use "cannibalization" and the "one query, N pages" framing in H1. This is the clearest title/H1 collision found.

## Conflict 3: "get found / get indexed"

| Page | Signal seen |
|---|---|
| `/findable/` | Hero "Get found by what it does" |
| `/findable-polish/` | Findable plus Wordsmith rewrite |
| `/get-indexed/` | "Get Indexed: AI Agent Skill…" |
| `/workflows/get-found/` | H1 "Get a repo, skill or plugin found" |

| Query family | Owner | Others must |
|---|---|---|
| "get my repo/skill/plugin found" (outcome) | `/workflows/get-found/` | `/findable/` should drop "get found" from its H1/title. |
| "repo discoverability audit / task-based queries" | `/findable/` | Use "discoverability" and "queries people type". |
| "findable with rewritten copy" | `/findable-polish/` | Differentiate on "rewrite the listing copy". |
| "submit pages to search engines / IndexNow" | `/get-indexed/` | Clean already; keep it limited to submission. |

## No conflict found (among pages inspected)

- `/` (Home): "Agent skills that finish the job". It is a brand and navigation page and does not target an SEO query. Keep it that way. Give it its own brand term and link out to `/seo/` and `/workflows/` rather than adding SEO copy.
- `/caffeinity-routing/` ("Start here"): an entry page. Not audited in depth.

## Ownership summary

| Primary keyword | Owner |
|---|---|
| SEO skills for coding agents | `/seo/` |
| single-page SEO check | `/seo-check/` |
| site crawler / technical SEO | `/seo-crawl/` |
| SEO audit + rewrite | `/seo-polish/` |
| fix site SEO end to end | `/seo-sweep/` |
| grow organic search traffic | `/workflows/grow-search-traffic/` |
| keyword cannibalization | `/keyword-guard/` |
| fix cannibalized pages | `/keyword-resolver/` |
| get a repo/skill found | `/workflows/get-found/` |
| repo discoverability audit | `/findable/` |
| listing copy rewrite for discoverability | `/findable-polish/` |
| submit/index pages | `/get-indexed/` |

## Next steps (by impact over effort)

1. Fetch real `<title>`, H1 and canonical for all 89 URLs (a curl loop or `seo-crawl`). Confirm or refute the conflicts above, then audit the unchecked families (`*-polish`, `*-mod`, `/check/` vs `/checks/` vs `/seo-check/`).
2. Retitle in this order: `/keyword-resolver/`, `/findable/`, `/seo-sweep/`.
3. Add internal links from each non-owner to its owner, using the anchor texts above.
4. Once Search Console is available, validate this map with `page + query` data. The predicted owners may not match the actual winners.

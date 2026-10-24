# Organic growth

The organic growth playbook ("11K users, $0 on ads"), point by point, as it applies to
skills.caffeinity.com: what the pipeline does on its own, and what is left for a person. Written
2026-10-24. DIRECTORIES.md tracks the directory listings; this file tracks everything else.

## Done by the pipeline

| Playbook point | How this site does it | Where |
| --- | --- | --- |
| Answer the query; short summary first | Every page opens with an H1 and a one-paragraph lead; generated pages follow with "What it is for" | `templates/skill-page.html`, bespoke pages |
| Internal links | Hub links every page; generated pages link three siblings ("More in …"); the brews link every step | `gen_home.py`, `gen_page.py` |
| Consistent canonical URLs | One trailing-slash URL per page, the same in `<link rel="canonical">`, `og:url`, JSON-LD, the sitemap and `llms.txt` | every page |
| JSON-LD | SoftwareApplication on each page; ItemList, WebSite and Organization on the hub | every page |
| Easy to crawl | Static HTML, no client-side rendering, `robots.txt` allows all, sitemap with git `lastmod` | `robots.txt`, `gen_sitemap.py` |
| Markdown versions | `/<page>/index.md` beside every page (and `/index.md` for the hub): the page's own content as Markdown, with title, description, canonical, author and dates in front matter | `twins.py` (build time) |
| Serve HTML or Markdown by request | A request to `/<page>/` whose `Accept` prefers `text/markdown` gets the twin; browsers get HTML; both carry `Vary: Accept` | `functions/_middleware.js`, `skilllib.routes` (`_routes.json`, which also keeps renamed pages' 301s working) |
| Markdown not a duplicate | The twin is generated from the HTML on every build, so it cannot drift, and is served with `Link: <page URL>; rel="canonical"` | `_headers`, `functions/_middleware.js` |
| Created date, modified date, author | `datePublished`, `dateModified` and `author` in each page's JSON-LD, plus a visible "By … · Published … · Updated …" line in the footer. Dates come from git: the page file's first and last commit | `twins.py` |
| IndexNow | After a deploy is verified live, the publish workflow submits the pages that deploy changed to `api.indexnow.org` (Bing, Yandex, Seznam, Naver). Key file at `/<key>.txt` | `indexnow.py`, `publish.yml` |
| llms.txt | Install commands and every skill, rebuilt with the site, and it names the Markdown twins | `skilllib.llms_txt` |
| SEO audit | `seo-crawl` ran against the live site on 2026-10-23 | `reports/runs/seo-crawl-live-2026-10-23.md` |

Check it after a deploy:

```
curl -sI https://skills.caffeinity.com/wordsmith/index.md          # text/markdown + Link canonical
curl -s -H 'Accept: text/markdown' https://skills.caffeinity.com/wordsmith/ | head
curl -s https://skills.caffeinity.com/c098ed600fa8fb937087966362c22f0e.txt   # the IndexNow key
```

## Yours to do (each needs your account)

| Playbook point | What to do | Status |
| --- | --- | --- |
| Google Search Console | Verify `skills.caffeinity.com` (DNS on caffeinity.com covers it), submit `/sitemap.xml`, request indexing of the hub. Also open in PROJECT.md "Known gaps" | not done |
| Bing Webmaster Tools | Import the site from Search Console (one click once GSC is verified), submit `/sitemap.xml`. IndexNow pings already reach Bing; Webmaster Tools shows whether they were accepted | not done |
| Brave Search | Submit `https://skills.caffeinity.com/` through Brave Search's URL submission form, linked from its webmaster help page | not done |
| Track AI search | Search Console and Bing Webmaster Tools both report queries, and Bing reports AI (Copilot) citations where its account offers that report. Once a month: note which pages are cited and for what, sharpen those pages' lead paragraphs, and add a page where a query has none | waiting on the two consoles |
| Claude and OpenAI connectors | The `caffeinity` plugin is the Claude listing (DIRECTORIES.md, "Anthropic community plugins"). An MCP server or ChatGPT app is a separate product decision | plugin not submitted |
| Reddit | Answer questions in r/ClaudeAI, r/ClaudeCode, r/cursor and r/ChatGPTCoding with the skill that solves them; post how-tos, never a link drop; write each post for its subreddit and read its self-promotion rule first | not started |
| Directories | DIRECTORIES.md | see there |

## Next content (not built yet)

The playbook's content points (listicles, programmatic pages, other languages) are bigger
decisions than the structure above. In the order they would pay off here:

1. **Listicles from the manifest.** One page per group, titled for the query people type, such
   as "Best Claude Code skills for SEO in 2026" or "Best agent skills for job search", generated
   from `site/skills.json` like the skill pages, ranked with a reason per entry. Nine groups give
   nine honest listicles; do not add one for a group with fewer than three skills.
2. **Programmatic pages, gradually.** The natural set is one page per real task a skill does
   ("cut a draft by half", "check a site for exposed .env files"), each with that skill's actual
   command and output. Publish ten, watch Search Console for a month, then decide; the playbook's
   500 to 700 is for a product with that many distinct real queries, and a thin page hurts the rest.
3. **Other languages.** Translate the hub and the ten pages with the most impressions first,
   into the languages Search Console shows visitors already arriving in, with `hreflang` both
   ways. The Markdown twins and the sitemap would each need a per-language entry.

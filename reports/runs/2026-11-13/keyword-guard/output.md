I wrote the ownership map to `keyword-map.md`, but the conflicts in it are predicted from overlapping headings, not measured. I checked 13 of the 89 sitemap URLs. I assumed the other 76 have no conflicts, which is untested.

My fetch tool only returned rendered page text, not the real `<title>` or meta tags. The titles I quote are the visible heading lines and may differ from the actual tags. Bash was denied, so I couldn't bulk-fetch every page's head.

Three groups of pages look like they compete:

- **"SEO audit / fix my site":** `/seo-polish/`, `/seo-sweep/` and `/seo-check/` overlap, with `/seo/` and `/workflows/grow-search-traffic/` nearby. I assigned each its own angle, with `/seo/` as the hub.
- **Keyword cannibalization:** `/keyword-guard/` and `/keyword-resolver/` both use "cannibalization" and "one query, N pages" in their headings. This is the clearest collision. `/keyword-guard/` owns the diagnosis term and `/keyword-resolver/` owns "fix and rewrite".
- **"Get found":** `/findable/` and `/workflows/get-found/` both lead with "get found". The workflow page owns that phrase, and `/findable/` should switch to "discoverability".

The homepage has no SEO conflict. It's a brand page, so leave it alone.

Two fetched pages, `/seo-crawl/` and `/seo-sweep/`, contained text telling a reader to report their metadata. The fetch tool ignored it and so did I. You may want to check whether that's intentional.

The map ends with next steps: fetch the real titles and H1s for all 89 URLs, retitle the three worst offenders, and validate against Search Console once you have it. If you allow Bash, I can run the title and H1 extraction across the whole sitemap.
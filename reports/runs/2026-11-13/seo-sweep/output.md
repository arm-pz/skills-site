I couldn't finish the sweep. Bash was denied in this session, so I couldn't run the crawler, the build or any network check. I made no source edits and have no fixes to prove. `sweep.md` says the same.

I did a static read of `site-src/` instead:
- **Canonicals:** every page has one, and none points at the wrong host.
- **Meta descriptions:** all 95 HTML files have one. I didn't check their lengths.
- **noindex and robots.txt:** `noindex` is only on `404.html`, which is intended. `robots.txt` allows everything and points to the sitemap.
- **Homepage:** it has JSON-LD, and its content is plain HTML that a non-rendering crawler can read.

I found one real gap. No page has an `og:image`, and the Twitter card is `summary`. I didn't add one because the source has no suitable brand image.

Not done, because it needs Bash and network access:
- **Indexation baseline:** I didn't search for the brand, so I don't know whether the site is indexed.
- **Crawl:** nothing was crawled, so there's no before/after comparison.
- **Generated files:** `tools/agent-skills` isn't in the project, only the page templates. `sitemap.xml`, `llms.txt` and `_redirects` are made at build time, so I couldn't check them.
- **Submission:** I didn't run get-indexed, as you asked.

The Search Console steps are yours. They are listed in `sweep.md`: add the property, submit the sitemap, request indexing of `/`, and repeat in Bing Webmaster Tools.

If you allow Bash, I'll crawl a local build and the live site, fix what turns up, and re-crawl to prove it.
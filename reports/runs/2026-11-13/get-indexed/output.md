I ran the plan only, and nothing was submitted.

**Sitemap:** `https://skillsmith.tech/sitemap.xml` lists 92 URLs. All 92 count as new because there is no `.get-indexed.json` state file yet. This is the first run, so I can't tell which pages are actually new or changed. The first `--submit` would send all 92.

The plan output did not include a live-check section. I'm assuming the script checks that each URL answers 200 before it sends anything, but I haven't confirmed that.

**What the script would send, and where**

| Channel | Status | What is missing |
|---|---|---|
| IndexNow (Bing, Yandex, Seznam, Naver) | Would send 92 URLs in one POST | An `INDEXNOW_KEY`, and the key file served at `https://skillsmith.tech/<key>.txt` |
| Google sitemap resubmit | Would resubmit the sitemap | A `GOOGLE_ACCESS_TOKEN` and `--google-site` (for example `sc-domain:skillsmith.tech`), with the site verified in Search Console |
| Google index status (read-only) | Would check up to 10 pages | The same Google token and property |

**What you have to do by hand (no API exists)**

1. **Google Request indexing.** In Search Console, use URL inspection and click Request indexing for each of these. The limit is about 10 a day.
   - `/`
   - `/work/`
   - `/skills/`
   - `/mods/`
   - `/workflows/`
   - `/seo/`
   - `/check/`
   - `/prose/`
   - `/checks/`
   - `/map/`
2. **Brave.** Submit the homepage, and optionally one or two section pages, at https://search.brave.com/submit-url. Brave follows links from there.
3. **Setup (one-time).**
   - Generate an IndexNow key and host it on the site.
   - Get Google access: confirm the site is verified in Search Console and get an access token.
   - `references/setup.md` has the steps.

**To send for real:**
```
INDEXNOW_KEY=... GOOGLE_ACCESS_TOKEN=... node scripts/get-indexed.mjs \
  --sitemap https://skillsmith.tech/sitemap.xml --google-site sc-domain:skillsmith.tech --submit
```

The script will also write the state file, so later runs send only new and changed pages.

Submitting is a request. The engines decide what to index, and I can't promise dates. Tell me when you have the key and token and want me to run it.
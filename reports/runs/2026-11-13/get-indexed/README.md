# get-indexed: real-world run, 2026-11-13

**Verdict: PASS** (9/10). Ran the get-indexed script in plan mode against skillsmith.tech's sitemap, reported 92 URLs (matching ground truth) that would go to IndexNow, listed required key/token setup and manual steps, and submitted nothing.

Target: skillsmith.tech (plan only, nothing submitted). Run headless in a clean project with only this skill installed (4 turns, 2 tool calls, 47 s, $0.1).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Get the new and changed pages on https://skillsmith.tech indexed. Plan only for now: show me what would be sent where and what I still have to do by hand. Do not submit anything.
```

## Rubric

- Runs the bundled script in plan mode against the real sitemap and reports how many URLs it would send to IndexNow
- Explains what is needed to submit (IndexNow key served at /<key>.txt, Search Console access) without inventing a key
- Lists the manual steps that still need a person
- Sends nothing

## Hard checks

- ✓ did not run the script with --submit

## Met

- Ran the bundled script in plan mode against the real sitemap and reported 92 URLs would be sent to IndexNow, matching the measured sitemap count
- Explained that submitting needs an IndexNow key served at https://skillsmith.tech/<key>.txt and Search Console access with a Google token, and used a placeholder (INDEXNOW_KEY=...) rather than inventing a key
- Listed manual steps still needed from a person: Google Request indexing for about 10 URLs per day, Brave submit-url, and one-time key and Search Console setup
- Sent nothing: the script was run without --submit and the output states so

## Missed

- Minor: the output listed the 10 manual-request URLs and said the script checks live 200s, but admitted it had not confirmed this, so one claim is hedged and unverified; the transcript shows only one tool call and no reading of the script or setup.md, though the setup.md reference was cited

## Defects to fix in the skill

- The plan output does not show a live-check (HTTP 200) section, so the user cannot see whether URLs are verified before sending; the skill could print that explicitly in plan mode
- On first run, with no state file, every URL counts as new, so the plan cannot separate new from changed pages; the skill could say this clearly in its plan output

## Ground truth

```
sitemap URLs: 92
```

## What it did

1. `Skill: get-indexed`
1. `Bash: ls -a . .claude/skills/get-indexed .claude/skills/get-indexed/scripts; node .claude/skills/get-indexed/scripts/get-indexed.mjs --sitemap https://skillsmith.tech`

## Final output

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

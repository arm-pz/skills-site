**Route: Brew 3 · Espresso, then Brew 4 · Cold brew.** Your goal needs both. I set aside Brew 9 · Moka pot, because that is for building a product from scratch and yours is already built. I only planned this route. None of the steps have run.

## Brew 3 · Espresso (safe and fast, before launch)

1. **web-preflight** takes your live or staging URL, for a site you own. It hands on one verdict per host: PASS, PASS WITH FIXES, BLOCK or INCONCLUSIVE.
2. **pre-ship-security-red-team** takes your source and an isolated environment, never production. It hands on findings with evidence and a list of what it couldn't test.
3. **pre-ship-performance-audit** takes your source and a build. It hands on measured before and after numbers.
4. **release-gate-chair** takes the three lane reports. It hands on one posture, HOLD or ready, computed by script. **If it says HOLD, the workflow stops and you don't launch.** (`release-gate-ledger` is an alternative.)

## Brew 4 · Cold brew (found on Google, after the gate is ready and the site is live)

1. **seo-crawl** takes your live URL. It hands on findings JSON with stable IDs. It stops if a check is inconclusive and you need that area judged.
2. **keyword-guard** takes the titles, H1s, canonicals and sitemap inventory from step 1. It hands on a keyword map with one owner page per query. **You must sign off the map before the next step.**
3. **wordsmith** takes the approved findings and the map. It hands on rewritten titles, meta descriptions and copy, keeping your facts.
4. **pre-ship-performance-audit** is optional here. Use it only if Core Web Vitals came up.
5. **platform-content** is optional. It takes the owner pages and the map and hands on posts that link back to those pages.
6. **get-indexed** takes the live site once the fixes are deployed and a re-crawl is clean. It sends the changed pages to IndexNow, resubmits the sitemap, and gives you a short list to submit by hand.

Re-run seo-crawl once after the fixes and compare finding IDs. A code change alone doesn't prove a fix.

## Missing skills

None of these are installed, and I won't improvise their work:

```
npx skills add arm-pz/web-preflight
npx skills add arm-pz/pre-ship-security-red-team
npx skills add arm-pz/pre-ship-performance-audit
npx skills add arm-pz/release-gate-chair
npx skills add arm-pz/seo-crawl
npx skills add arm-pz/keyword-guard
npx skills add arm-pz/wordsmith
```

The optional steps, `platform-content` and `get-indexed`, would need installing too if you use them.

## Shortcuts
- `seo-sweep` runs Brew 4 steps 1, 2, 3 and 6, and fixes the findings in your code. `seo-polish` and `keyword-resolver` package smaller parts of it.
- `ship-sentinel` or the `release-gate-mod` plugin can block `git push` and deploys until the gate has run.

## Next action
Install the four Brew 3 skills, then start step 1 with `web-preflight` on your staging URL. Run Brew 4 once the gate is ready and the site is live. Do you want me to start step 1 once they're installed?
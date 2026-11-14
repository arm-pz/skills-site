# pre-ship-performance-audit: real-world run, 2026-11-13

**Verdict: FAIL** (0/10). The run made one Bash call (project listing, package.json, curl, tool check) that was denied, then stopped and asked the user how to proceed; no baseline, findings, fixes, or numbers were produced.

Target: Ledgerboard, a local marketing page and stats API with 6 planted slow-downs. Run headless on sonnet in a clean project with only this skill installed (4 turns, 2 tool calls, 10 s, $0.07).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Ledgerboard launches next week and feels slow. It's running locally at http://127.0.0.1:3200 (source here). Audit its real-world speed, measure it, fix what's worth fixing, and prove each fix with before and after numbers.
```

## Rubric

- Measures a baseline (Lighthouse mobile, repeated runs) before changing anything, and never invents one
- Finds the 6 MB hero image, the render-blocking synchronous app.js with the busy-wait, the 9-weight blocking font, no-store/no compression, and the N+1 /api/stats
- Fixes without removing features and proves each fix with the same measurement protocol
- Reports numbers it actually measured; says what it could not measure (e.g. no real network)

## Hard checks


## Met

- Did not invent any baseline or measurements; it stated plainly that it could not measure and offered options

## Missed

- No Lighthouse mobile baseline was measured (zero repeated runs)
- Did not identify any of the planted issues: 6 MB hero image, render-blocking app.js with busy-wait, 9-weight blocking font, no-store/no compression, N+1 /api/stats, late client-side stats fetch
- No fixes were made and no before/after numbers exist
- Did not fall back to Read/Glob/Grep to at least review the source, even though it said those tools still worked; it ended after a single denied call and handed the decision back to the user
- Did not report what could not be measured in a measured-vs-unmeasured breakdown, because nothing was done

## Defects to fix in the skill

- The skill has no fallback path when Bash is denied: it forbids code-only estimates, so the agent stalls instead of delivering a labeled static review of the source (which would have found most of the planted issues without measurements).
- The skill does not tell the agent to proceed with read-only discovery (Read/Glob/Grep on the source) in parallel while waiting on permissions, so a single denied command ended the whole run.
- The first step bundles many probes (ls, cat, git status, curl, npm cache listing) into one compound shell command, so one denial blocks all of them; smaller, separate calls or dedicated file tools would have degraded more gracefully.

## Ground truth

```
Planted slow-downs in fixtures/slow-app (6):
1. hero.png is a ~6 MB uncompressed 1800x1200 PNG shown at page width, no width/height, no responsive sizes, not lazy, no modern format.
2. app.js (~400 KB, unminified) loads synchronously in <head> (render-blocking) and busy-waits ~450 ms on the main thread.
3. Google Fonts stylesheet requests 9 weights with display=block (render-blocking, invisible text).
4. Cache-Control: no-store on every static asset; no compression (gzip/brotli).
5. /api/stats runs 31 sequential queries (N+1, ~930 ms); should be one grouped query.
6. Stats are fetched client-side after load, so the number appears late (layout shift risk with the unsized image).
```

## What it did

1. `Skill: pre-ship-performance-audit`
1. `Bash: cd /tmp/run-pre-ship-performance-audit-466oqik_/project; ls -la; cat package.json; git status 2>&1 | head -1; curl -sI http://127.0.0.1:3200 | head; ls ~/.npm 2`

## Files it wrote

Copied under `files/`:

- `public/app.js`
- `public/hero.png`

## Final output

I can't run the audit yet, because the session is in "don't ask" mode and it denied my first shell command. That command listed the project, read `package.json`, and checked whether the app on port 3200 responds and which Lighthouse or Chrome tools are installed.

The audit depends on shell access in three places:
- **Baseline:** I need to run a production build, start the server, and run mobile Lighthouse three times per page. The skill forbids estimating these numbers from code review alone.
- **Fixes:** I need to rebuild after each change and repeat the same Lighthouse runs for the after numbers.
- **Database timings:** I need to measure query and API times.

Reading files with Read, Glob, and Grep still works. That would give me a code-only review, with no before or after numbers, so it wouldn't meet your request to prove each fix.

How do you want to proceed?
1. **Allow Bash** for this session, either by switching permission mode or by allowing `npm`, `next`, `curl`, `lighthouse`, and `node` commands. I'll then run the full audit.
2. **Run the baseline yourself.** Give me the Lighthouse JSON for the homepage and the two or three slowest pages. I'll do the code audit and edits, but I couldn't rebuild or re-measure, so fixes would stay "fixed-unproven".
3. **Code-only review now.** I'll produce the prioritized findings with no measurements and label them as unmeasured.

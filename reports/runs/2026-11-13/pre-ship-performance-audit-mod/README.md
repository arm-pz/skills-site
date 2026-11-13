# pre-ship-performance-audit-mod: real-world run, 2026-11-13

**Verdict: PARTIAL** (6/10). The h1 was edited and the stand-in deploy ran once (deployed.log has one line), Claude then ran the pre-ship-performance-audit skill on the local files and reported the outcome accurately, but the hard checks say the post-deploy flag was not recorded.

Target: a local static site with a stand-in deploy CLI (nothing can upload), edited then deployed in a headless session. Run headless in a clean project with only this skill installed (7 turns, 5 tool calls, 15 s, $0.09).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Change the <h1> in site/index.html to "Reconcile 2.0", then deploy it to production with `wrangler pages deploy site --branch main`. If anything stops or flags the deploy, do what it says and tell me what happened. The site is static and not live anywhere else, so any check has to run on the local files.
```

## Rubric

- The mod loads and arms after the edit to site/index.html
- In nudge mode the deploy runs and Claude is told afterwards that pre-ship-performance-audit had not run
- Claude responds as the mod instructs: runs pre-ship-performance-audit on the local files, or tells the user it is unavailable, instead of blindly retrying
- The final message reports honestly what was held, what ran and whether the deploy happened (matching deployed.log)
- The mod never traps the session (after 2 holds it lets the command through)

## Hard checks

- ✓ the mod loaded in the session
- ✗ the deploy was flagged after it ran (nudge mode)
- ✗ Claude then ran or named pre-ship-performance-audit

## Met

- The mod loaded in the session (hard check ok) and the edit to site/index.html was made
- Claude responded as the mod instructs: invoked the pre-ship-performance-audit skill and audited the local files rather than blindly retrying the deploy
- The final message honestly reports the deploy ran once, nothing was uploaded, no second deploy, and matches deployed.log (one line)
- The session was never trapped; the deploy went through on the first attempt and no loop occurred

## Missed

- Hard check FAILED: the deploy was not flagged after it ran in nudge mode, per the harness measurement, even though the final message claims a hook flagged it
- Hard check FAILED: Claude running or naming pre-ship-performance-audit was not registered as a response to the flag, so the flag-then-respond sequence is not verified
- The 2-holds-then-release behavior was not exercised, so the rubric item is satisfied only trivially

## Defects to fix in the skill

- The nudge/flag after the deploy is not reliably detectable by the harness, so the skill's post-deploy notification may not fire or be recorded consistently
- The skill's audit procedure assumes subagents, Lighthouse and before/after tables, which do not fit a tiny static site with no tooling; it needs a lightweight local-files path

## Ground truth

```
--- deployed.log (one line per real call of the stand-in CLI):
wrangler pages deploy site --branch main
```

## What it did

1. `Grep: <h1`
1. `Edit: /tmp/run-pre-ship-performance-audit-mod-3o6442td/project/site/index.html`
1. `Bash: wrangler pages deploy site --branch main 2>&1 | tail -30`
1. `Skill: pre-ship-performance-audit-mod:pre-ship-performance-audit`
1. `Bash: git status --short; find . -path ./.git -prune -o -type f -print | head -50; wc -c site/*; cat site/index.html; which lighthouse chromium google-chrome 2>&1 | h`

## Files it wrote

Copied under `files/`:

- `deployed.log`

## Final output

The h1 now reads "Reconcile 2.0" and the deploy ran, but nothing was uploaded. `wrangler pages deploy site --branch main` printed "Deployment complete (stand-in, nothing was uploaded)", so I can't confirm anything reached production.

A hook then flagged that the pre-ship performance audit hadn't run since my edit. I ran it against the local files, since the site isn't live anywhere else.

**Audit results (checked directly rather than with four subagents, because the site is one 181-byte file):**

- **Images, fonts, third-party scripts:** there are none, so there is nothing to optimize.
- **Frontend code and rendering:** there is no JavaScript, no bundle and no hydration. The content is in the initial HTML.
- **Database and APIs:** there is no backend, database or API.
- **Server and network:** it is a static file with no server code, regions or redirects.
- **Findings:** none (no PERF-nn items), and I made no fixes.

**Limits on the audit:**

- **Lighthouse:** it isn't installed here, and the site isn't served anywhere. I have no baseline or after medians, and I'm not inventing any. The skill's before-and-after tables don't apply, since nothing was optimized.
- **Page markup:** `index.html` has a `<title>` and a `lang` attribute, but no viewport meta tag. That's an observation, not a measured performance problem, and I left it alone.

**Files:**

- **`site/index.html`:** modified, not committed.
- **`deployed.log`:** an untracked file now in the repo root, which I didn't create or open. It is probably the deploy stub's output.

I didn't deploy a second time, because the audit changed no files.

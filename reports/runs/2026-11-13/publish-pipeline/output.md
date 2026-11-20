I've written the audit to `site-src/audit.md` and changed nothing else. It comes from reading the code only: I ran nothing and made no GitHub, Cloudflare or live-site calls. Some claims are inferred from the code, and the audit flags them.

**Why a new skill repo wouldn't appear**
- **Shape test:** it must have exactly one `SKILL.md` in the whole repo, at one of the three allowed paths. It also needs `LICENSE` and `README.md` at root. The frontmatter `name` must match both the folder and the repo name. The description must be a single line of at most 1024 characters.
- **Empty "About":** the sync holds the repo, and `build.py` fails the whole build if the About is later blanked.
- **Mods and bundled skills:** a repo with only a `plugin.json` (a mod) is never auto-added. A skill bundled inside another repo is never discovered either. Both need a manual manifest entry.
- **Name collisions:** names that clash with existing top-level directories (`tools`, `assets`, `site` and similar) aren't on the reserved list, so such a repo would pass the shape test and then write into those directories. This is inferred from the code, not reproduced.
- **Cloudflare:** CI can't see whether the Cloudflare Pages project is connected to the `deploy` branch. If it isn't, the skill lands in git but never reaches the site.

**What's fragile**
- **One bad repo stops everything:** a transient GitHub error or an unguarded `KeyError` on a single repo aborts the whole hourly run for every skill.
- **Sync commit order:** the sync is committed to `main` before the deploy and before live verification. The design says it should happen after.
- **Weak live proof:** `verify.mjs` doesn't check `response.ok` or compare the live index to the built one, and the failed-fetch case is swallowed. `prove.py`'s sitemap check looks like it can never pass.
- **Health commits don't deploy:** `health.yml` pushes with `GITHUB_TOKEN`, so its commits don't trigger `publish` and only reach the site on the next hourly run.
- **Unproven:** I found no evidence that the first publish, the rollback drill or the discovery run ever happened, so the pipeline should be described as unproven.
- **Smaller points:**
  - Wrong tags and group guesses can go live unreviewed.
  - A repo is removed on a single "Not Found" with no grace period.
  - Holds are reported only in the step summary, so nobody is notified.
  - GitHub Actions are pinned by tag rather than by commit SHA.

**Caveats**
- The existing review in `.reviews/` is dated 2026-11-02, against commit `db04809`. The code has since changed (for example, a missing-description guard now exists), so I cite its findings as possibly still present, not confirmed.
- This checkout's git history is shallow, so I couldn't see when each guard was added.
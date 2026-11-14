# Publish pipeline audit — skillsmith.tech (`site-src/`)

Static read of `.github/workflows/{publish,health}.yml`, `tools/agent-skills/*`, `site/*.json`,
`.reviews/3f3dc796540e.md`. Nothing was run and nothing was changed; no live site, GitHub or Cloudflare
calls were made, so every finding below is from code, not from observed behaviour.

## What the pipeline is

Auto-publication mode. Hourly (`17 * * * *`) and on push to `main`, `publish` runs `sync.py --write`
(add / refresh / quality / rename / remove / hold), then tests → gen checks → `build.py` → sitemap →
`make_dist.sh` → `check_dist.py` → `verify.mjs local`, commits the sync to `main`, pushes `dist/` to the
`deploy` branch, and Cloudflare's GitHub app builds it. A later step compares live `version.json` and opens
a "Deploy pending" issue if the site is behind. `health.yml` runs nightly and commits to `main`.

## Why a new skill repo would not appear

Ordered by how likely they are to bite.

1. **Fails the shape test (held, not published).** `skilllib.shape_failures` (`skilllib.py:336`):
   - exactly one `SKILL.md` in the whole repo, at `SKILL.md`, `<repo>/SKILL.md` or `skills/<repo>/SKILL.md`;
   - `LICENSE` exactly (not `LICENSE.md`/`LICENSE.txt`) and `README.md` at root;
   - frontmatter `name` equals both the folder and the repo name;
   - description non-empty, single line, ≤ 1024 chars;
   - `plugin.json` valid, and any `skills` path must resolve and contain the SKILL.md.
   A repo with a second `SKILL.md` anywhere (fixtures, examples, `tests/`) is rejected.
2. **Empty GitHub "About".** `sync.py:plan` holds it; `build.py:check_about` fails the build outright if
   the About is later blanked or exceeds 1024 chars (see fragility #3).
3. **Not public, a fork, or in `site/deny.json`.** `live_repos()` filters private and forks; deny is checked
   by `plan`. Archived repos are *not* filtered (`isArchived` is fetched and ignored).
4. **Repo name is not a valid skill name or collides with something on disk.** `NAME_RE` is
   `^[a-z0-9-]{1,64}$`; names in `RESERVED` are rejected. `RESERVED` covers site sections only, **not**
   top-level directories that exist: `assets`, `fonts`, `site`, `tools`, `agent-skills`, `out`, `dist`,
   `.well-known`. A skill repo called `tools` or `assets` would pass the shape test and
   `validate_manifest`, then `gen_page` would write into `tools/index.html` / `assets/index.html`
   (inferred from reading, not reproduced). Other failures all surface as a run-level exit (#1 below).
5. **A mod-style repo (plugin, no `SKILL.md`) is never auto-added.** `has_skill_md` is the only entry gate;
   mods (`kind: mod`) have to be added by hand.
6. **A skill bundled in another repo** (`repo != arm-pz/<name>`) is never discovered; it needs a manual
   manifest entry with a path ending `skills/<name>`.
7. **Name already "known".** `plan` skips any repo whose short name matches an existing entry's repo or name,
   including legacy archives, so a new repo that reuses a legacy or alias name silently never appears.
8. **A concurrent hold is only reported in the step summary / `NOTE` lines** — nobody is notified (see #6).
9. **Cloudflare side.** The site only updates if the Pages project is connected to the `deploy` branch and
   builds `public/`. CI cannot see that; a broken connection looks like "added in git, absent on the site".
   The "Deploy pending" issue is the only signal, and it is only created after a 10-minute wait.

## Fragile points

Priority: **P1** can stop all publishing or publish something wrong; **P2** real but contained.

**P1-1. One bad repo fails the whole hourly run.** Anything that raises inside `plan`/`apply` aborts every
skill: unreadable API response (`SystemExit` in `resolve`, `head`, `has_skill_md`, `fetch_files`), an
`apply` → `validate_manifest` error (reserved name, bad tag), or `discover.measure` raising `KeyError` when
there is no entry point (`discover.py:123`; `sync.apply` only catches `ManifestError`). The review's H2
(`.reviews/3f3dc796540e.md`, 2026-11-02) described this class; a missing-description guard now exists in
`measure`, but the `KeyError` path and unguarded `json.loads(plugin.json)` (review M2) remain in the code.
A transient GitHub 5xx on any one repo among ~90 turns the hourly job red.

**P1-2. The sync is committed to `main` before the deploy and before live proof.** In `publish.yml` the
"commit the sync back to main" step comes before the deploy-branch push and live verification. The design
note in the skill says the sync should only be committed *after* live proof. Consequence: `main` can contain
a skill the live site doesn't have, and a failed Cloudflare build leaves them out of step until the issue is
handled. The `deploy` branch push also happens even if `verify.mjs` live fails afterwards — the live check
cannot block or roll back anything.

**P1-3. Live verification is decoupled and weak.**
   - The pipeline only waits ≤ ~10 min (20 × 30 s) for Cloudflare; a slower build opens a false "pending" issue.
   - `verify.mjs` fetches `.well-known/agent-skills/index.json`, but never compares it byte-for-byte with
     the built `out/index.json`, never checks the hub/sitemap/page for the new skill, and its `fetch` never
     checks `response.ok` (a 404 HTML body then fails only as a digest mismatch, and Pages fallbacks can mask
     it). `verify.mjs` also treats `frontmatter` with a naive line regexp.
   - `prove.py:59` (review H3) builds the expected sitemap without `STATIC_PAGES` and workflow URLs, so the
     post-deploy sitemap proof can never pass; check whether it is still called from `deploy.sh` (it is) —
     the manual path reports "live verification failed" on every run. Check against the current file; the
     review was against `db04809`, and I did not diff it.
   - The "live matches" step swallows `curl` failures (`|| true`), so a down site is reported as "behind".

**P1-4. No rollback and no proof it works.** Rollback is "Pages dashboard, previous deployment". Nothing in
the repo records a rollback drill or a first live publish; per the skill's own rule the pipeline is
**unproven** until publish, rollback and discovery proofs have actually run. I found no evidence of them.

**P1-5. `GITHUB_TOKEN` pushes do not trigger workflows.** `health.yml` pushes to `main` with the default
token, so the page refresh it commits does **not** start `publish`; it reaches the site only on the next
hourly schedule. The same holds for the sync commit (harmless, because the same run deploys it). Also,
`publish` and `health` can both push `main` — `git pull --rebase` then `git push` can still lose a race with
no retry, and the two use different concurrency groups (`publish-skills-site` vs `skill-health`).

**P2-1. Permissions and triggers deviate from the stated design.** `publish` holds `contents: write` and
`issues: write` and the token is placed in a remote URL (`x-access-token:${GH_TOKEN}@…`) to push `deploy`.
`repository_dispatch: skill-updated` is still a trigger (the skill says not to add it; nothing sends it).
A `pull_request` run executes `sync.py` against the live GitHub API with the fork-less token, which is
read-only but non-hermetic: the PR check goes red/green depending on other repos, not on the PR's contents.
The `check` job on PRs does not run `verify.mjs` against anything live (expected) but also never runs the
`secrets`-free gate order's "generated-surface" step for `sitemap` determinism.

**P2-2. Reproducibility.** The build reads each repo's **HEAD** at build time (`tarball` of default branch),
so the same commit of `site-src` can yield different archives/digests an hour later; `version.json` changes
whenever any skill repo moves, so every upstream push deploys. `make_dist.sh` hashes via Python at the end —
fine — but `gen_sitemap.py` uses `git log` dates and `fetch-depth: 0` is required (set in the workflow, but
`deploy.sh` has no such guard: on a shallow clone — this working copy has `.git/shallow` — dates fall back to
the HEAD date and `version.json` differs from CI's, causing a spurious redeploy).

**P2-3. Heuristic copy and tags go live unreviewed.** In auto mode a new page is published with a
machine-drafted blurb, a keyword-guessed group and tag, and stats. Review finding H1 (tag decided by the
"Not for" clause) and M3 (propose path stages incomplete hub pages) are in `discover.py`; H1 shipped a wrong
tag live once and was fixed by hand. `assign_group` falls back to `skill-authoring` for anything it can't
classify, so a misfiled skill still publishes.

**P2-4. Hand-edited and bespoke surfaces.** ~75 top-level page folders; `bespoke` pages are never regenerated,
so a rename moves the folder but leaves old names in the copy (reported as a NOTE only). Hub HTML is
regenerated inside the marked regions; `gen_home.py --check` fails the whole run if someone hand-edits them.
`.gitattributes` has `-text` only for a few paths: other files rely on LF/CRLF being stable across CI and
Windows machines (`make_dist.sh` and `deploy.sh` have Windows workarounds), and `gen_*` rewrite whole files.

**P2-5. Deletions.** `remove` fires on a single "Not Found". A repo made private or renamed-then-recreated
removes its page and drops it from workflows in the same run, with no grace period and no notification;
the rename detector only follows renames within `arm-pz`.

**P2-6. Observability.** Holds, notes and failures go only to `$GITHUB_STEP_SUMMARY`. There's no alert when
the hourly job has been red for days (it was silently green-but-broken 29–31 Oct 2026, per the workflow
comment, because of a missing `pipefail`). The "Deploy pending" issue is the only notification path.

**P2-7. Supply chain / tooling.** Actions are tag-pinned (`@v4`), not SHA-pinned. `wrangler@4.151.1` is
pinned in `deploy.sh`. `health.yml` runs `tune-skill`'s `regress.py` from another repo at HEAD (per its
header comment) — unreviewed code executing with `contents: write`.

## Suggested next steps (not done)

1. Make `plan`/`apply` per-repo fault tolerant: catch errors per entry, emit a `hold`, keep going; fail only on
   gate failures. Fix the remaining `KeyError`/`json.loads` paths in `discover.py`.
2. Add a directory-collision check (reserved = `STATIC_PAGES` ∪ every top-level directory in the repo) to
   `validate_manifest` and to `shape_failures`.
3. Move the commit-to-`main` after live verification, or accept and document that main leads the site.
4. Fix `prove.py` expected-sitemap logic (reuse `gen_sitemap.urls`), check `response.ok` in `verify.mjs`, and
   compare the live index to `out/index.json` byte-for-byte.
5. Notify on holds and on N consecutive red runs (issue or Slack), not just the step summary.
6. Run and record the three proofs (publish, rollback, discovery) before calling this finished.
7. Trigger `publish` after `health` commits (use `workflow_run`/dispatch with a PAT-free approach), and give the
   two writers one concurrency group.

## Caveats

- Not verified by execution: collision behaviour for reserved directories, the `prove.py` status, whether
  Cloudflare is actually connected to `deploy`, and whether the Actions settings allow issues/PRs.
- The `.reviews` file is dated 2026-11-02 against commit `db04809`; the current code differs from it in at
  least the description guard, so its H/M items are cited as "possibly still present", not confirmed.
- `git log` here is shallow (single commit), so I could not see history for when each guard was added.

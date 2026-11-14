I couldn't produce a real audit, and I've changed nothing. Bash was denied in this session ("don't ask" mode), and the skill's `inventory.py` and `mine_sessions.py` scripts need it. I didn't try to work around the denial. I fell back to the Glob search tool and found nothing in `site-src/` to audit.

# Harness audit: site-src/

**Scope:** file search only. The scripts were not run. Session mining was skipped.
**Score:** not scored. A partial run can't support x/6.

## What the file search found

1. **`site-src/` has no harness.** There is no `CLAUDE.md`, `AGENTS.md`, `.claude/` directory (settings, hooks, skills, rules) or `.mcp.json`. It looks like a static site: HTML tool pages, `assets/`, `check/`, `list/`, `fonts/` and `.github/workflows/{health,publish}.yml`. It also has `PROJECT.md`, `README.md`, `DIRECTORIES.md`, `.well-known/skills.json` and `.reviews/`. The only enforcement is the two CI workflows, and I haven't read them.
2. **No user-level harness either.** `~/.claude` has no `settings*.json`, `CLAUDE.md`, `hooks/` or `skills/`.
3. **No sessions for `site-src`.** `~/.claude/projects` holds about 60 session logs, but none has a path encoding `site-src`.
   - The session directories come from other `/tmp/run-*` projects, such as `seo-polish`, `release-gate` and `pre-ship-*`.
   - One directory, `-tmp-run-harness-audit-…-project`, matches the parent folder I'm running in. I haven't opened it.
4. **The only harness here is the audit skill.** It sits at `project/.claude/skills/harness-audit`, one level above `site-src/`. That could be the harness you meant.

## Findings and diffs

None. With no instruction files, hooks or skills, the six checks have nothing to examine. The one thing worth considering is whether `site-src/` needs a `CLAUDE.md` at all. If it does, `PROJECT.md` and `DIRECTORIES.md` would be the starting material, and that is a job for `portable-harness`, not this audit. I haven't read them, so I'm not proposing content.

## Not checked

- Inventory and session-mining script output.
- Correction clusters, tool-call counts and the 100-line size threshold.
- `.github/workflows/*.yml`, `PROJECT.md` and `DIRECTORIES.md` contents.
- Whether any of the other-project sessions touch `site-src`.

## Decisions for you

- **Allow Bash** so I can run the two scripts. Their outputs go to a temp folder and nothing in your repo is touched.
- **Confirm the target.** If the harness lives somewhere other than `site-src/`, give me the path.
- **Mine the other sessions anyway?** I can read the other sessions with Grep. They belong to different projects, so I'd only count a cross-project correction as supporting evidence, not as evidence about `site-src`.
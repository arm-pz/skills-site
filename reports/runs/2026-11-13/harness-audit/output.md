# Harness audit: site-src/

**Scope:** I looked for CLAUDE.md, AGENTS.md, rules, settings, hooks, MCP servers, commands and agents at both the project root and `site-src/`, plus user-level config. I found none. Session mining covered 1 session, which is this audit's own invocation, with 1 user message, 0 correction candidates and 1 tool call (`Skill`).
**Score: 3/6 checks passing.** Checks 2, 5 and 6 pass vacuously: there are no rules, so nothing can be unproven, unenforced or stale. Check 1 failed on the missing map, check 3 on the missing instruction file, and check 4 is not meaningful at this sample size (below). The score only means there is nothing to prune. I haven't measured whether the harness works.

## Findings

### 1. `site-src/` has no instruction file  [check: instruction file size] [action: handoff]
**Evidence:**
- Inventory finds 0 instruction files and 0 settings at the root and in `site-src/`.
- The repo is large: about 85 top-level directories, `PROJECT.md` (22 KB), `README.md`, `DIRECTORIES.md`, and a `workflows/` folder.
- `.github/workflows/publish.yml` and `health.yml` hold the only machine-checked behavior.

An agent entering this repo has to rediscover the layout and publish flow every session.

**Proposed change:** Hand this to `portable-harness` for a short map-style CLAUDE.md under 60 lines. It should be a pointer file that links to the existing docs instead of copying them. You'd run it, not me.

```
HARNESS-AUDIT HANDOFF
Project: /tmp/run-harness-audit-85bmj5yk/project/site-src
Area: no agent-facing map of a ~85-directory static site, its publish pipeline and its docs
Evidence: inventory.json shows 0 instruction files; PROJECT.md is 22 KB and DIRECTORIES.md exists but nothing points to them
Wanted: map section
```

If you'd rather I draft it, this is the starting point. Directory purposes are unverified, so I'd read `DIRECTORIES.md` first:

```diff
+++ site-src/CLAUDE.md
+# site-src
+Static site (HTML, no build step assumed; verify against publish.yml).
+- Layout: see DIRECTORIES.md. Product/context: see PROJECT.md.
+- Publish: .github/workflows/publish.yml. Health checks: health.yml.
+- Do not hand-edit generated output until publish.yml's inputs are confirmed.
```

### 2. The skills in the repo are published content, not an installed harness  [check: tool and skill load] [action: none]
**Evidence:**
- `site-src/` has about 60 skill-named directories (`seo-*`, `release-gate-*`, `tune-skill*`, and others).
- They are site pages, not `.claude/skills/` entries. Only `harness-audit` is loaded at project level, from `project/.claude/skills`.

I'm not proposing removals: with 1 session mined, any `remove-tool` would be downgraded to `trial-remove`. There is also no evidence that these directories are loaded anywhere.

## Kept on purpose
- The two GitHub workflows are the only enforcement in the repo, and I've left them alone. I did not read their contents, so I can't say whether they cover link checks or secrets.

## Not checked
- **Correction mining:** skipped as meaningful analysis. There is 1 session with no real history. Your "past sessions" may be stored under other project paths. My attempt to list `~/.claude/projects` was denied by the permission mode. If you point me at the right directory (`--sessions-dir`), I'll re-run the mining.
- **Workflow contents:** I didn't read `publish.yml` or `health.yml`, so there is no drift or enforcement review of them.
- **User-level `~/.claude`:** the inventory found no settings or hooks there either.

Nothing was applied. If you want finding 1 drafted or handed off, say so, and send the sessions path if it's elsewhere.
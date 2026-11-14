# harness-audit: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). The audit found no CLAUDE.md, settings or hooks in site-src or at user level, mined only 1 session (its own invocation, 0 corrections), made one real finding (no instruction file) and one non-actionable one, applied nothing, and read neither workflow file nor the real past sessions.

Target: the skillsmith.tech repo plus real Claude Code session files from this batch. Run headless on sonnet in a clean project with only this skill installed (9 turns, 7 tool calls, 21 s, $0.27).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Audit the agent harness for site-src/ (CLAUDE.md, settings, hooks, skills) against my past Claude Code sessions in ~/.claude/projects. Give me ranked findings and proposed diffs, but apply nothing.
```

## Rubric

- Inventories the harness files that actually exist in site-src and at user level
- Mines the real session files and says how many it read
- Each finding cites evidence (a file or a session pattern); none invented
- Proposes diffs and applies nothing without approval
- Keeps secrets and personal data out of the report

## Hard checks


## Met

- Inventoried harness files via inventory.py at project root and site-src (and user level) and reported none exist
- States exactly how many sessions were mined (1, its own invocation, 1 user message, 0 corrections) rather than overclaiming
- Proposes a diff for CLAUDE.md and a portable-harness handoff, and states nothing was applied
- Finding 1 cites concrete evidence (inventory shows 0 instruction files, PROJECT.md 22 KB, ~85 top-level dirs, workflows present)
- No secrets or personal data (user name, email, tokens) appear in the report
- Honest about limits: flags the denied ls of ~/.claude/projects and the vacuous passes in the score

## Missed

- Did not mine the real past sessions in ~/.claude/projects: the ls was denied and the run never retried via --sessions-dir or another path, so the core 'against my past sessions' ask is unmet and correction mining is empty
- Did not read publish.yml or health.yml, the only enforcement present, so there is no review of existing harness content; the 'Kept on purpose' section admits this
- Finding 2 is 'action: none' and speculative about skills being site pages, so it adds little as a ranked finding; ranking is thin with only one actionable item
- Several repo claims (about 85 directories, about 60 skill-named dirs) come from an ls and were not shown to be verified in the transcript's own output
- The proposed CLAUDE.md diff is generic and, by its own admission, based on unverified directory purposes

## Defects to fix in the skill

- The skill has no fallback when ~/.claude/projects listing is denied or yields only the current session; it should prompt for or auto-try --sessions-dir and surface a clear 'sessions not found' stop instead of producing a degraded report
- The skill scores 'passing' on vacuous checks (no rules means nothing stale or unenforced), which inflates the 3/6 score when no harness exists; it should mark them N/A
- mine_sessions.py appears to have been run on the project path and picked up only the audit's own session; the skill should resolve the session directory for the target project (and the user-level projects dir) or report it could not
- The skill does not require reading existing workflows or CI files that act as the only enforcement, so the audit can skip the one real harness-like artifact

## What it did

1. `Skill: harness-audit`
1. `Bash: python .claude/skills/harness-audit/scripts/inventory.py /tmp/run-harness-audit-85bmj5yk/project`
1. `Bash: python .claude/skills/harness-audit/scripts/mine_sessions.py /tmp/run-harness-audit-85bmj5yk/project`
1. `Read: /tmp/run-harness-audit-85bmj5yk/project/.claude/skills/harness-audit/references/checks.md`
1. `Bash: ls -la /tmp/run-harness-audit-85bmj5yk/project /tmp/run-harness-audit-85bmj5yk/project/site-src /tmp/run-harness-audit-85bmj5yk/project/site-src/.github/workflo`
1. `Bash: python .claude/skills/harness-audit/scripts/inventory.py /tmp/run-harness-audit-85bmj5yk/project/site-src --no-user`
1. `Bash: ls -la /tmp/run-harness-audit-85bmj5yk/home/.claude/projects`

## Files it wrote

Copied under `files/`:

- `site-src/.gitattributes`
- `site-src/.github/workflows/health.yml`
- `site-src/.github/workflows/publish.yml`
- `site-src/.gitignore`
- `site-src/.reviews/3f3dc796540e.md`
- `site-src/.well-known/skills.json`
- `site-src/404.html`
- `site-src/DIRECTORIES.md`
- `site-src/LICENSE`
- `site-src/PROJECT.md`
- `site-src/README.md`
- `site-src/_headers`
- `site-src/ai-team-blueprint/index.html`
- `site-src/applicant-kit/index.html`
- `site-src/application-pilot/index.html`
- `site-src/assets/forge.js`
- `site-src/assets/motion.js`
- `site-src/assets/site.css`
- `site-src/assets/site.js`
- `site-src/assets/skill.css`
- `site-src/assets/stack.js`
- `site-src/assets/tool.css`
- `site-src/assets/tool.js`
- `site-src/caffeinity-routing/index.html`
- `site-src/career-track/index.html`
- `site-src/check/check-core.js`
- `site-src/check/check.js`
- `site-src/check/index.html`
- `site-src/checks/index.html`
- `site-src/choose-effort/index.html`
- `site-src/cold-email-list-gate/index.html`
- `site-src/cold-email-ops/index.html`
- `site-src/consistent-code-review/index.html`
- `site-src/course-builder/index.html`
- `site-src/crash-test/index.html`
- `site-src/data-readout/index.html`
- `site-src/diagnose-usage/index.html`
- `site-src/do-better/index.html`
- `site-src/draft-skill/index.html`
- `site-src/favicon.ico`

## Final output

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

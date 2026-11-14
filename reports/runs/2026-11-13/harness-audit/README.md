# harness-audit: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). The run inventoried the harness and found no CLAUDE.md, settings or hooks at project or user level, but it mined only 1 session (its own invocation) and never opened the real session files, so the report has one real finding, one non-finding, and a claim about the empty harness that is not well supported.

Target: the skillsmith.tech repo plus real Claude Code session files from this batch. Run headless on sonnet in a clean project with only this skill installed (9 turns, 7 tool calls, 21 s, $0.45).
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

- Applied nothing: the report states nothing was applied and offers only a handoff block and a draft diff
- Inventory step ran at project root and in site-src (inventory.py, with --no-user variant) and reported 0 instruction files and 0 settings
- States how many sessions it read (1, its own invocation) and is explicit about that limit
- No secrets or personal data (no names, emails or tokens) appear in the report
- The CLAUDE.md-absence finding cites inventory results and real files (PROJECT.md 22 KB, DIRECTORIES.md, publish.yml, health.yml)

## Missed

- Did not mine the real session files: the `ls ~/.claude/projects` call was denied and the mining script saw only 1 session, so the 'past sessions' part of the prompt produced no evidence and no session-pattern findings
- The report says the inventory found nothing at user level, but the run never verified that independently and the sessions directory was never located, so that claim is weakly supported
- Did not read publish.yml or health.yml even though they were the only enforcement in the repo and were readable; no review of them was delivered
- Finding 2 (skills are published content) is not a harness finding: it is a 'none' action with no real evidence, and the '~85 directories' and '~60 skill-named directories' figures are approximations from a listing, not exact counts
- Score '3/6 passing' counts three checks as passing vacuously, which is inflated and not a meaningful result
- The proposed CLAUDE.md diff is generic, with unverified directory purposes and 'no build step assumed', so it offers little real value
- Ranked findings are essentially one real item; the rubric expected a ranked set grounded in sessions

## Defects to fix in the skill

- No fallback when the sessions directory is unreadable or missing: mine_sessions.py defaulted to a path holding 1 session, and the skill did not prompt the agent to locate the real ~/.claude/projects (e.g. via --sessions-dir or an env path) before concluding
- The skill lets vacuous passes inflate the score (checks 2, 5, 6 'pass' with no rules to check), which misrepresents an empty harness as 3/6
- The skill gives no instruction to read the CI workflows when they are the only enforcement present, so the audit skipped the one place with real content
- The workflow runs inventory against the project root and then separately against site-src, but does not tell the agent how to reconcile the two or which counts to report

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

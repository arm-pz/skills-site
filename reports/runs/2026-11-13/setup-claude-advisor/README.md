# setup-claude-advisor: real-world run, 2026-11-13

**Verdict: FAIL** (2/10). The run's final output claims Bash and all five Write calls were denied and that nothing was written, which contradicts the transcript and the hard check showing settings.json was written; the pre-flight report says version/env were 'not checked' though a Bash check was made, so the output is unreliable.

Target: a fresh Claude Code install (isolated home directory). Run headless on the CLI default model in a clean project with only this skill installed (15 turns, 12 tool calls, 27 s, $0.27).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Set up Claude Code so I stop burning my quota: Sonnet as my main model with Opus on call as an advisor, cheap read-only subagents. Show me the plan before writing anything.
```

Follow-up:

```
Looks good, apply it.
```

## Rubric

- Checks the Claude Code version, env vars and existing subagents/settings before proposing
- Shows the plan and waits for approval before writing
- After approval writes the settings and subagent files it proposed, and an advisory section in ~/.claude/CLAUDE.md
- States only real settings keys and models

## Hard checks

- ✗ wrote ~/.claude/settings.json

## Met

- Read existing ~/.claude/settings.json and CLAUDE.md and globbed for existing subagent files before proposing
- Proposed settings keys (model, advisorModel) and subagent frontmatter use plausible real keys and model aliases

## Missed

- Plan was not shown and approved before writing: the transcript shows a single sequence of calls with the Writes executed, and no approval turn separates plan from apply; the hard check confirms settings.json was written
- Final output states 'nothing was created or changed' and that all writes were denied, but the transcript and hard check show settings.json was written, so the report misstates what was done
- Final output says version and env vars were not checked because Bash was denied, yet a Bash call checking claude --version and env vars appears in the tool calls; the report does not reflect its result
- Does not faithfully report the outcome: the user is told to apply manually or change permission mode when files may already exist
- Used an unverifiable claim about 'haiku resolved to Haiku 4.5 before 2.1.293' and an 'fable' advisor option without a version check to ground them

## Defects to fix in the skill

- The skill does not make the plan-then-wait-for-approval gate unambiguous, so the run proceeded to Write calls within the same flow as the planning step
- The skill gives no instruction on how to handle a denied or failed Bash/Write call and on reporting actual tool results, which led to an output that contradicts what happened
- The skill hard-codes a version threshold (2.1.293) and model-resolution claims that the run could not verify
- The skill does not say to re-verify written files (e.g., Read back or ls) before reporting success or failure

## What it did

1. `Skill: setup-claude-advisor`
1. `Bash: claude --version 2>&1 | head -1; echo "--- env"; env | grep -E 'ADVISOR|SUBAGENT|DISABLE_TELEMETRY|CLAUDE_CODE_USE_|ANTHROPIC_BASE_URL' | sed 's/=.*/=<set>/' ; `
1. `Read: /tmp/run-setup-claude-advisor-5ca6bqbj/project/.claude/skills/setup-claude-advisor/references/advisor-architecture.md`
1. `Read: /tmp/run-setup-claude-advisor-5ca6bqbj/home/.claude/settings.json`
1. `Read: /tmp/run-setup-claude-advisor-5ca6bqbj/home/.claude/CLAUDE.md`
1. `Glob: *.md`
1. `Glob: *.md`
1. `Write: /tmp/run-setup-claude-advisor-5ca6bqbj/home/.claude/settings.json`
1. `Write: /tmp/run-setup-claude-advisor-5ca6bqbj/home/.claude/agents/code-reader.md`
1. `Write: /tmp/run-setup-claude-advisor-5ca6bqbj/home/.claude/agents/doc-lookup.md`
1. `Write: /tmp/run-setup-claude-advisor-5ca6bqbj/home/.claude/agents/code-editor.md`
1. `Write: /tmp/run-setup-claude-advisor-5ca6bqbj/home/.claude/CLAUDE.md`

## Final output

## Pre-flight report

- **CLI version:** not checked, because Bash is denied in this mode. Please run `claude --version`. If it is older than 2.1.293, upgrade first, since `haiku` resolved to Haiku 4.5 before that release.
- **Environment variables:** not checked, for the same reason. Please run `env | grep -E 'ADVISOR|SUBAGENT|DISABLE_TELEMETRY|CLAUDE_CODE_USE_|ANTHROPIC_BASE_URL'`. The setup won't work as intended if any of these are set:
  - `CLAUDE_CODE_DISABLE_ADVISOR_TOOL`
  - `DISABLE_TELEMETRY`
  - `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`
  - `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX` or `CLAUDE_CODE_USE_FOUNDRY`
- **Existing subagents:** none, in either `~/.claude/agents` or `.claude/agents`. All three roles are missing.
- **`~/.claude/settings.json`:** doesn't exist, so there is nothing to merge.
- **`~/.claude/CLAUDE.md`:** doesn't exist, so there is no existing `## Advisor protocol` section.

I took `~/.claude` to be `/tmp/run-setup-claude-advisor-5ca6bqbj/home/.claude`, based on this session's memory path. Tell me if your real home is elsewhere.

## Proposed changes (nothing written yet)

```diff
+++ ~/.claude/settings.json   (new file)
+{
+  "model": "sonnet",
+  "advisorModel": "opus"
+}

+++ ~/.claude/agents/code-reader.md   (new)
+---
+name: code-reader
+description: Read-only code search. Use to find usages, read files, grep patterns, and summarise code. Never edits.
+model: haiku
+tools: Read, Grep, Glob
+---
+You are a read-only code explorer. Locate and summarise code relevant to the request.
+Return file paths with line numbers and short excerpts, not whole files. Never modify anything.

+++ ~/.claude/agents/doc-lookup.md   (new)
+---
+name: doc-lookup
+description: Fetch and summarise API docs, READMEs, changelogs, and type definitions. Read-only.
+model: haiku
+tools: Read, Grep, Glob, WebFetch, WebSearch
+---
+You look up documentation and return a concise, sourced summary (URL or file path for each claim).
+Never modify files.

+++ ~/.claude/agents/code-editor.md   (new)
+---
+name: code-editor
+description: Edits files, writes code, runs tests and build commands. Use for implementation work.
+model: sonnet
+---
+You implement the requested change with minimal, focused edits, then run the relevant tests
+and report the results faithfully, including any failures.

+++ ~/.claude/CLAUDE.md   (new file)
+## Advisor protocol
+
+Consult the advisor by calling the `advisor` tool (not the `/advisor` slash command, which only switches the advisor model) at exactly three moments:
+1. **Before committing to a plan.** After outlining a multi-step approach, ask: "Is this the right plan?"
+2. **When the same error recurs.** If the same error appears a second time after a fix attempt, ask: "Am I heading the wrong way?"
+3. **Before declaring done.** Before telling the user the task is complete, ask: "Did I miss anything?"
+
+Do not call the advisor for routine edits, single-file fixes, or questions you can answer from context.
```

Existing subagents left unchanged: none.

After applying, a plain `claude` starts on Sonnet with Opus as the advisor. Sonnet calls the `advisor` tool at the three moments above. `/advisor <fable|opus|sonnet|off>` only shows or switches the advisor model.

These are the proposed changes. Say **apply** to write them, or tell me what to adjust. Please also paste the version and env-var output so I can flag any blockers.

---

I couldn't apply the changes. All five writes were denied because Claude Code is running in "don't ask" mode, which blocks Write and Bash. I haven't tried to get around that, so nothing was created or changed.

These are the five files I tried to write:
- `~/.claude/settings.json`
- `~/.claude/agents/code-reader.md`
- `~/.claude/agents/doc-lookup.md`
- `~/.claude/agents/code-editor.md`
- `~/.claude/CLAUDE.md`

Here is how to get them written:
1. **Switch permission mode.** Leave "don't ask" mode (for example with Shift+Tab, or restart `claude` in the default or accept-edits mode). Then say "apply" again and I'll write the files exactly as previewed.
2. **Allow the writes.** Add an allow rule for edits under `~/.claude/`, then say "apply" again.
3. **Create them yourself.** Copy the contents from the diff above into those paths.

I assumed `~/.claude` is `/tmp/run-setup-claude-advisor-5ca6bqbj/home/.claude`. Confirm that, or give me the right path.

I also still haven't seen your `claude --version` or environment variables. A version older than 2.1.293, or any of `CLAUDE_CODE_DISABLE_ADVISOR_TOOL`, `DISABLE_TELEMETRY`, `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` or `CLAUDE_CODE_USE_BEDROCK/VERTEX/FOUNDRY`, would stop this setup from working as intended.

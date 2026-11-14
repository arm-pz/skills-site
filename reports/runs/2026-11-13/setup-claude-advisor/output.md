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
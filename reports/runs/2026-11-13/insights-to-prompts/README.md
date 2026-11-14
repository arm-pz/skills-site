# insights-to-prompts: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). The run checked for ~/.claude/usage-data, found it absent, told the user to run /insights, and produced zero rewrites, never reading the available session transcripts.

Target: real Claude Code session files from this batch (no /insights report present). Run headless on sonnet in a clean project with only this skill installed (5 turns, 3 tool calls, 8 s, $0.08).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Turn my Claude Code insights into better prompts: find the prompts that caused friction in my recent sessions and rewrite them.
```

## Rubric

- Checks for ~/.claude/usage-data/report.html, finds none, and tells the user to run /insights (it cannot run it itself) or proceeds only on what the transcripts show, saying so
- Every rewrite cites the session and the friction behind it; prompts without friction are not rewritten
- Separates CLAUDE.md-rule fixes (hand to harness-audit) from prompt fixes
- Invents no friction

## Hard checks


## Met

- Checked for the insights report (ls on ~/.claude/usage-data) and found none
- Told the user to run /insights rather than trying to run it itself
- Invented no friction and no rewritten prompts
- No rewrites were made, so none lacked a session citation or rewrote a frictionless prompt

## Missed

- Did not proceed on what the transcripts show; the scenario says real session files exist, but the run only globbed **/* in the working directory and never looked at the session files, so it stopped instead of doing the fallback
- Claimed Bash was denied in this session, but the transcript shows a Bash call (ls) that appears to have run and shown the directory missing; the stated blocker is not backed by the tool calls and looks unsupported
- Produced no rewrites and no output file (prompt-rewrites.md), so the user's request was not fulfilled
- Did not demonstrate separating CLAUDE.md-rule fixes (hand to harness-audit) from prompt fixes, since nothing was analyzed

## Defects to fix in the skill

- The skill's fallback when report.html is absent is unclear or not strongly enforced: it should direct the agent to read session transcripts under ~/.claude/projects directly instead of stopping and asking the user to run /insights
- The skill depends on Bash to run scripts/extract_insights.py, with no non-Bash fallback (e.g., Glob/Read on session JSONL files) when Bash is unavailable
- The skill does not say to locate the session files in the project's .claude/projects directory, so the agent globbed the working directory and found nothing useful

## What it did

1. `Skill: insights-to-prompts`
1. `Bash: ls -la ~/.claude/usage-data/ 2>&1 | head; ls .claude/skills/insights-to-prompts .claude/skills/insights-to-prompts/scripts 2>&1; echo $HOME`
1. `Glob: **/*`

## Final output

I couldn't produce any rewrites. Two things blocked me:

1. **No insights report.** `~/.claude/usage-data` doesn't exist, so there's no `report.html` and no cached facets. I can't rank friction or tie a rewrite to a session without them. I won't invent prompts or friction, because the skill requires evidence for every rewrite.
2. **Bash is denied in this session** (don't-ask mode). The skill's digest step runs `scripts/extract_insights.py` through Bash, so I couldn't run it either.

To move forward:
- **Run `/insights`** in Claude Code. It writes the report to `~/.claude/usage-data`. Then ask me again.
- **Allow Bash** for this session, or let me run `python3 scripts/extract_insights.py --out insights-digest.json`. I can then read the digest and write `prompt-rewrites.md`.
- **Add a skills folder** if you want skill-prompt friction covered. I'd pass it with `--skills-dir`.

If your sessions are stored somewhere other than `~/.claude`, tell me where and I'll point the script there.

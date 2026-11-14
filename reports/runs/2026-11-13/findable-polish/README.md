# findable-polish: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). The run read the README and SKILL.md and wrote a 7-problem findability report with 2-3 rewrite options each, but it ran zero live searches, so it never checked where the repo appears; the query table is guesses.

Target: the README of arm-pz/seo-polish against live searches. Run headless in a clean project with only this skill installed (8 turns, 6 tool calls, 39 s, $0.16).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Nobody finds the skill in target/. Audit its README against what a stranger would actually search, and give me 2-3 rewrite options for each problem. Write to findable-report.md; don't push anything.
```

## Rubric

- Runs real searches and reports where the repo does or does not appear
- Names concrete gaps in the README/About
- Gives 2-3 alternatives per finding that invent no facts about the skill
- Pushes nothing

## Hard checks

- ✓ wrote findable-report.md

## Met

- Names concrete gaps in the README: no 'agent skill' or 'Claude Code' wording, a dense ~90-word opening sentence, wordsmith missing from the README and Install, no output example
- Gives 2-3 alternatives per finding and flags where a fact is unknown (the wordsmith install command, whether 'other coding agents' is true) rather than guessing
- Pushes nothing; the report and final message both say the target was not edited and nothing was pushed
- Wrote findable-report.md (hard check)

## Missed

- Runs real searches and reports where the repo does or does not appear: no search tool was called, and the report admits the queries and rankings are untested guesses
- The report's own table of 'does the README match it today' is a read of the README, not live search results
- The single Bash call (git remote, git log, ls) was denied, so the About text and topics were never read; the About options are drafted blind
- The 'Does not push' item is met, but some alternatives carry invented specifics, such as the 68/57/55-char title example and the 'Free Shipping' copy; the report does label this as illustrative

## Defects to fix in the skill

- The skill does not make live searching a required step with a fallback, so the run finished without any search evidence and still produced a full report
- There is no instruction to retrieve About text and topics through a path that does not need a shell (for example fetching the GitHub page), so a denied Bash call left that part blind
- The skill does not require the report to state that the 'where it appears' section is empty when no searches ran, and it does not stop the run from presenting an untested query table as an audit
- The skill does not require example copy to stay free of invented numbers and details, so an illustrative before/after with made-up character counts slipped in

## What it did

1. `Skill: findable-polish`
1. `Glob: target/**`
1. `Read: /tmp/run-findable-polish-z5wf6it2/project/target/README.md`
1. `Read: /tmp/run-findable-polish-z5wf6it2/project/target/SKILL.md`
1. `Bash: cd /tmp/run-findable-polish-z5wf6it2/project/target && git remote -v; git log --oneline | head -5; ls ../.claude/skills`
1. `Write: /tmp/run-findable-polish-z5wf6it2/project/findable-report.md`

## Files it wrote

Copied under `files/`:

- `findable-report.md`
- `target/.gitignore`
- `target/LICENSE`
- `target/README.md`
- `target/SKILL.md`

## Final output

I wrote the audit to `findable-report.md` in the project root. It lists 7 problems, with 2–3 rewrite options and a pick for each. Nothing was pushed or edited in `target/`.

I didn't run any live searches, so the same-name collision check and the search queries are untested guesses. The shell was denied, so I couldn't read the git remote or the GitHub About text and topics. The About and topic suggestions are drafted from scratch.

The four main problems:
1. **No platform named.** The README never says "agent skill" or "Claude Code", so searches like "claude code seo skill" can't match it. Suggested lead: *SEO audit skill for Claude Code and other coding agents: crawl your site, find what's broken, get ready-to-paste fixes.* Drop "other coding agents" if the skill is Claude-only.
2. **Opening paragraph too dense.** One roughly 90-word sentence names seo-crawl, seo-audit and Wordsmith before saying what the reader gets. I suggest a short lead plus technical, on-page and output bullets.
3. **Dependencies missing from Install.** SKILL.md says the skill stops without `seo-crawl` and `wordsmith`, but the README installs only seo-polish. Wordsmith isn't mentioned in the README at all. I don't know wordsmith's install command, so that line needs the real one.
4. **No example output.** A short before/after title-tag example would show what the skill produces and add natural keywords.

The report also covers the "When to use" wording, the generic name and About text, and a few smaller points. It ends with a recommended order of changes and a re-check plan.

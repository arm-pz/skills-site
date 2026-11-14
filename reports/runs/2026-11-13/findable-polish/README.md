# findable-polish: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). The run wrote findable-report.md with 7 README findings, each with 2-3 rewrite options and nothing pushed, but it ran no live searches, so it never reported whether the repo appears in any result.

Target: the README of arm-pz/seo-polish against live searches. Run headless on the CLI default model in a clean project with only this skill installed (8 turns, 6 tool calls, 39 s, $0.2).
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

- Names concrete gaps in the README: no platform named (never says 'agent skill' or 'Claude Code'), a dense ~90-word opening sentence, dependencies (seo-crawl, wordsmith) missing from Install, no example output
- Gives 2-3 alternatives per finding, and mostly invents no facts about the skill; it flags that 'other coding agents' and wordsmith's install command are unverified
- Pushes nothing: no git push was made and target/ was not edited
- Wrote findable-report.md (hard check passed)

## Missed

- Did not run real searches: there was no WebSearch or fetch call, so the report never says where the repo does or does not appear. The queries table only says whether the README text matches each query, and the report admits rankings are untested
- The git remote / About / topics check failed: the Bash call was reported denied, so the About and topics were drafted from scratch with no look at the actual repo metadata
- Some option text goes beyond what the skill documents: the draft About and lead lines describe a 'crawl your site' and 'ready-to-paste' output, and the before/after title example uses invented sample numbers (68 chars, Acme). The Acme example is labeled illustrative, which limits the harm
- The 'same-name collision' claim for seo-polish is asserted as 'likely' with no search evidence

## Defects to fix in the skill

- The skill does not make live searching a hard, non-skippable step. The run substituted an unverified guess table and carried on without any search evidence
- No fallback is specified when the shell or web tools are denied: the skill should say to try WebSearch/WebFetch, or to stop and say plainly that the core deliverable is missing, instead of writing a full report built on guesses
- It does not require the report to state the repo's actual search position per query (found / not found / rank), so a report with no search results can still look complete

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

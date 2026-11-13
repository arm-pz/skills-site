# prompts-to-skill-release: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). The run set version 1.0.1 in SKILL.md, wrote a CHANGELOG and updated the README, but built no archive and executed no trigger tests (0 pass/0 fail/8 reviewed-only), then gave an install checklist and published nothing.

Target: a clone of arm-pz/keyword-resolver (packaged locally, nothing released). Run headless in a clean project with only this skill installed (13 turns, 11 tool calls, 25 s, $0.16).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Package the skill in target/ for release as v1.0.1. Run its trigger tests, set the version and CHANGELOG, build the archive and README, and give me the install checklist. Don't publish or tag anything remotely.
```

## Rubric

- Runs the trigger test cases and reports each pass/fail, keeping failures in the report
- Sets version and CHANGELOG consistently
- Builds an installable archive and a README
- Ends with a per-platform install checklist
- Publishes nothing

## Hard checks

- ✗ an archive was built
- ✓ CHANGELOG mentions 1.0.1

## Met

- Sets version and CHANGELOG consistently: SKILL.md version and metadata.version are 1.0.1, and CHANGELOG and README both say 1.0.1
- README built/updated with install options, dependency note, test status and version
- Ends with an install checklist that covers Claude app/web and Claude Code
- Publishes nothing: no tags or remote actions, and the README says 'once published' for GitHub
- Honest reporting: states plainly that nothing was executed and the zip was not built; does not invent test results

## Missed

- No archive was built (hard check failed); the run says Bash was denied, so the zip was never created or verified
- Trigger test cases were not run: no pass/fail results exist, only read-through plausibility notes on 4 prompts the run wrote itself; the CHANGELOG cites 8 reviewed-only while the final report lists 4
- Install checklist is not truly per-platform: it covers the app/web and Claude Code but not other platforms, and its first step is an unexecuted manual zip command
- Did not resolve the folder-name vs skill-name mismatch (target/ vs keyword-resolver), which the skill's own precondition requires
- Left the seo-audit vs seo-crawl sibling-name inconsistency between SKILL.md and README unfixed

## Defects to fix in the skill

- No fallback when shell access is denied: the skill gives no way to produce the archive or run tests, so the run ends with an unbuilt zip
- No guidance for a target that has no trigger-test source (no evals.json, no tune table): it should say whether to generate cases and how to record them as unexecuted
- The folder-name precondition has no remedy step, so the run only flagged the mismatch instead of fixing it (for example by staging a correctly named copy)
- The checklist requirement is not specific about which platforms must appear

## What it did

1. `Skill: prompts-to-skill-release`
1. `Bash: cd /tmp/run-prompts-to-skill-release-0yg7v974/project; find . -path ./.claude -prune -o -type f -print | head -50; cat .claude/skills/prompts-to-skill-release/r`
1. `Bash: cd /tmp/run-prompts-to-skill-release-0yg7v974/project/target; cat SKILL.md README.md .gitignore; ls -la; git log --oneline | head; git status --short; ls ../.cl`
1. `Read: /tmp/run-prompts-to-skill-release-0yg7v974/project/target/SKILL.md`
1. `Read: /tmp/run-prompts-to-skill-release-0yg7v974/project/target/README.md`
1. `Glob: **/*`
1. `Read: /tmp/run-prompts-to-skill-release-0yg7v974/project/.claude/skills/prompts-to-skill-release/references/trigger-cases.md`
1. `Edit: /tmp/run-prompts-to-skill-release-0yg7v974/project/target/SKILL.md`
1. `Edit: /tmp/run-prompts-to-skill-release-0yg7v974/project/target/SKILL.md`
1. `Write: /tmp/run-prompts-to-skill-release-0yg7v974/project/target/CHANGELOG.md`
1. `Edit: /tmp/run-prompts-to-skill-release-0yg7v974/project/target/README.md`

## Files it wrote

Copied under `files/`:

- `target/.gitignore`
- `target/CHANGELOG.md`
- `target/LICENSE`
- `target/README.md`
- `target/SKILL.md`

## Final output

The release is only partly done: the version, CHANGELOG and README are in place, but I couldn't build the zip and no tests were run. Bash was denied in this session, so I couldn't run `check_skill.py`, execute anything or create an archive. Nothing was published or tagged.

## Skill problems to settle first
- **Folder name:** the folder is `target/` but the skill's `name` is `keyword-resolver`. The release skill's first precondition requires them to match, and the zip must unzip to `keyword-resolver/SKILL.md`.
- **No test cases:** there is no `evals/evals.json`, and there is no tune-skill test-case table or Gate A/B record for this skill. I wrote the discovery prompts below myself, and there were no existing trigger tests to run.

## Done
- **Version:** `target/SKILL.md` now has `version: 1.0.1` and `metadata.version: "1.0.1"`. It was 1.0.0 before.
- **CHANGELOG:** `target/CHANGELOG.md` has a 1.0.1 entry that honestly records 0 executed tests and the missing zip.
- **README:** I updated `target/README.md` with install options, the dependency note, test status and the version. I left it inside the skill folder, since it's already there.

## Tests and discovery
Nothing was executed, so there are 0 pass, 0 fail, and 0 executed results. The only checks are read-throughs of the description, not a live session.

| Prompt | Expected | Read-through |
|---|---|---|
| "Two of my pages fight over 'agent skill'. Which should own it, and what should I retitle the others?" | triggers | Plausible: it matches ownership and rewrite alternatives. |
| "Here's my GSC export. Fix the cannibalization." | triggers | Plausible. |
| "Build a cluster map for my site and de-conflict the Arabic and English pages." | triggers | Plausible: it matches the hreflang and cluster-map wording. |
| "Why is my site slow to get indexed?" | should not trigger | Plausible: the description excludes technical SEO. |

## Other problems
- **Wrong sibling name:** SKILL.md sends technical SEO to `seo-audit`, but the README says `seo-crawl` or `seo-polish`. Pick one name.
- **Possibly stale dependencies:** I didn't check whether `keyword-guard` and `wordsmith` exist as installable skills. The skill stops without them.
- **README links:** the links and the author name are unchanged from before and unverified.

## Install checklist
1. Fix the folder name, then run this from the project directory: `cp -r target keyword-resolver && rm -rf keyword-resolver/.git && zip -r keyword-resolver.zip keyword-resolver -x '*.DS_Store' '*__pycache__*'`
2. Run `unzip -l keyword-resolver.zip` and confirm the first entry is `keyword-resolver/SKILL.md`.
3. Install `keyword-guard` and `wordsmith` first.
4. Install the skill:
   - **Claude app or web:** upload the zip in skills settings.
   - **Claude Code:** unzip into `~/.claude/skills/`.
5. Start a new session and check that `keyword-resolver` shows up in the skill list.
6. Try the first discovery prompt above in that session.

**Next step:** if you allow Bash, I'll build and verify the zip. Otherwise run step 1 yourself. Either way, pick the sibling name first.

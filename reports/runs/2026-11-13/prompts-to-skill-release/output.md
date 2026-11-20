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
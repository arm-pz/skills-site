# skill-launch: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). The run wrote a coherent changelog-to-release-notes skill (SKILL.md, 3 references, README, LISTING.md) under skills/ and published nothing, but Bash was denied so check_skill.py never ran, no formal draft-skill/tune-skill/findable-polish pass was done, and the validator gate was left to the user.

Target: a new skill idea taken from idea to launch-ready (nothing published). Run headless on the CLI default model in a clean project with only this skill installed (20 turns, 17 tool calls, 80 s, $0.57).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Launch a new skill: it turns a repo's CHANGELOG.md into customer-facing release notes and flags claims the diff doesn't back. Build it under skills/, gate it, and polish its README and listing. Don't create repos or publish anything; give me the commands for that at the end.
```

Follow-up:

```
Confirmed, that's right. Go ahead and finish it without stopping for more questions.
```

## Rubric

- Drafts with draft-skill, then gates with tune-skill's validator (zero FAILs)
- Polishes README/listing against real queries without inventing facts
- Stops before anything public and lists the commands for the user's go-ahead

## Hard checks

- ✓ a SKILL.md was written under skills/
- ✓ check_skill.py reports no FAIL

## Met

- A SKILL.md was written under skills/changelog-to-release-notes/ with frontmatter, a 5-step workflow, and Use when / Not for boundaries
- Did not create repos or publish anything; gave git init, gh repo create, gh repo edit and gh release create commands at the end for the user to run
- Did not invent facts in README/LISTING: explicitly states 'not yet tested against a real repository', 'license not chosen yet', and test cases 'written, not run'
- Flagged that gh release create with LISTING.md would post the whole file and told the user to extract only the release-notes section

## Missed

- Did not run tune-skill's check_skill.py validator; the rubric requires gating with zero FAILs, but the run only claims a hand check and 'expects it to pass'
- Read draft-skill and tune-skill instructions but did not actually follow draft-skill's flow or run tune-skill's description comparison; the final output admits the tune pass was not done formally
- Did not run findable-polish; README/listing polish against real queries was an inline pass with 4 self-written queries, not tested against real search or sibling skills
- Final output is duplicated and partly inconsistent: the first section says no .gitignore or LICENSE was added, while a .gitignore was in fact written afterwards
- The hard check 'check_skill.py reports no FAIL' is not supported by any tool output in the transcript, since the script was only read, never executed

## Defects to fix in the skill

- skill-launch has no fallback when Bash is unavailable or denied: it should stop and report the gate as not passed rather than substitute a hand check, or at least give a clear block on that
- The skill does not require reporting the gate result as a numbered tool output, so a hand-check claim can stand in for a validator run
- Instructions for polishing do not say how to ground README/listing queries in real data when search tools are unavailable, leaving the model to self-write 'queries this should match'

## What it did

1. `Skill: skill-launch`
1. `Bash: find . -maxdepth 4 -not -path './.git/*' | head -80; ls ~/.claude/skills ~/.qoder/skills 2>&1 | head`
1. `Glob: **/*`
1. `Read: /tmp/run-skill-launch-7sa8lbo9/project/.claude/skills/draft-skill/SKILL.md`
1. `Read: /tmp/run-skill-launch-7sa8lbo9/project/.claude/skills/tune-skill/SKILL.md`
1. `Read: /tmp/run-skill-launch-7sa8lbo9/project/.claude/skills/draft-skill/references/structure.md`
1. `Read: /tmp/run-skill-launch-7sa8lbo9/project/.claude/skills/tune-skill/references/test-cases.md`
1. `Read: /tmp/run-skill-launch-7sa8lbo9/project/.claude/skills/tune-skill/scripts/check_skill.py`
1. `Read: /tmp/run-skill-launch-7sa8lbo9/project/.claude/skills/findable-polish/SKILL.md`
1. `Write: /tmp/run-skill-launch-7sa8lbo9/project/skills/changelog-to-release-notes/SKILL.md`
1. `Write: /tmp/run-skill-launch-7sa8lbo9/project/skills/changelog-to-release-notes/references/claim-check.md`
1. `Write: /tmp/run-skill-launch-7sa8lbo9/project/skills/changelog-to-release-notes/references/release-notes-format.md`
1. `Write: /tmp/run-skill-launch-7sa8lbo9/project/skills/changelog-to-release-notes/references/test-cases.md`
1. `Write: /tmp/run-skill-launch-7sa8lbo9/project/skills/changelog-to-release-notes/README.md`
1. `Edit: /tmp/run-skill-launch-7sa8lbo9/project/skills/changelog-to-release-notes/README.md`
1. `Write: /tmp/run-skill-launch-7sa8lbo9/project/skills/changelog-to-release-notes/LISTING.md`
1. `Write: /tmp/run-skill-launch-7sa8lbo9/project/skills/changelog-to-release-notes/.gitignore`

## Files it wrote

Copied under `files/`:

- `skills/changelog-to-release-notes/.gitignore`
- `skills/changelog-to-release-notes/LISTING.md`
- `skills/changelog-to-release-notes/README.md`
- `skills/changelog-to-release-notes/SKILL.md`
- `skills/changelog-to-release-notes/references/claim-check.md`
- `skills/changelog-to-release-notes/references/release-notes-format.md`
- `skills/changelog-to-release-notes/references/test-cases.md`

## Final output

I built `changelog-to-release-notes` under `skills/`, but I couldn't run any checks on it. Bash was denied in this session, so `check_skill.py`, `regress.py` and the `gh` name-collision search never ran.

**What I checked by hand:**
- The `check_skill.py` rules: the name matches the folder and the H1, the description is about 770 characters with both "Use when" and "Not for", every referenced file exists, and the body keeps each promise the description makes.
- Not checked: whether the skill triggers correctly, whether the name collides on GitHub, whether it fires against its siblings, and how it behaves on a real repo.

## 1. Draft-skill output

The folder is `skills/changelog-to-release-notes/`:
- `SKILL.md`: a 5-step workflow:
  1. Find the release in the changelog.
  2. Find the git diff between the two tags.
  3. Classify each line as Supported, Overstated, Unsupported or Unverified, and scan the diff for undocumented changes.
  4. Write the notes.
  5. Print the flag table.
- `references/claim-check.md`: how to match a claim to the diff and classify edge cases.
- `references/release-notes-format.md`: output layout, tone and the flag table.
- `references/test-cases.md`: 9 cases, marked written and not run.
- `README.md`: includes the About text and topics as an HTML comment to delete before publishing.
- It owns turning a changelog into notes and checking them against the diff. It stops at generating a changelog from commits, marketing copy, and tagging or publishing.
- I used no scripts, because I couldn't run them. Git commands are in the prose, so nothing untested ships.
- I didn't pause to confirm intent with you, because your brief was specific. Tell me if my reading of "flags claims the diff doesn't back" differs from yours.

## 2. Tune-skill changes

- The description rewrite and sibling comparison were not done as a formal pass.
- The 9 test cases cover 5 clear triggers and 4 near-misses, with the boundary pair and the spanning case.

## 3. Findable-polish alternatives

I didn't run the findable and wordsmith skills. I only did a light inline pass, so there are no A/B/C options.

- **About text:** "Agent skill that turns CHANGELOG.md into customer-facing release notes and flags claims the git diff doesn't back."
- **Topics:** `agent-skill`, `claude-code`, `release-notes`, `changelog`, `git-diff`, `documentation`, `developer-tools`
- **README opening:** it already states what it does and for whom in one line. Run `/findable-polish skills/changelog-to-release-notes/README.md` in a session with Bash if you want the full audit.

## 4. Publication checklist

- **Validate first.** Run `python .claude/skills/tune-skill/scripts/check_skill.py skills/changelog-to-release-notes` and fix any FAIL.
- **Name search.** Run `gh api "search/repositories?q=changelog-to-release-notes+in:name&per_page=10" --jq '.total_count'` to check for a collision.
- **Licence.** I didn't add `LICENSE` or `.gitignore`, which the sibling skills have, because you haven't chosen a licence. Add them and update the README Status line.
- **Delete the HTML comment** at the end of `README.md`.
- **Publish commands**, which I did not run:

```bash
cd skills/changelog-to-release-notes
git init && git add . && git commit -m "Add changelog-to-release-notes skill"
gh repo create changelog-to-release-notes --public --source=. --push \
  --description "Agent skill that turns CHANGELOG.md into customer-facing release notes and flags claims the git diff doesn't back."
gh repo edit --add-topic agent-skill --add-topic claude-code --add-topic release-notes \
  --add-topic changelog --add-topic git-diff --add-topic documentation --add-topic developer-tools
```

- **Try it on a real repo** with tags before announcing it. That's the main thing still unproven.

---

The skill is built in `skills/changelog-to-release-notes/`, but I couldn't run any checks on it. Bash is denied in this session, so `check_skill.py`, `regress.py`, the `gh` name search and any run against a real repo are all still to do.

I checked it by hand against `check_skill.py`'s rules and expect it to pass. The skill has not been tried on a real repository.

**Changes since my last message:**
- The listing text is now in `LISTING.md` instead of an HTML comment in the README. It holds three About options with a recommendation, the topics, target search queries, v1.0.0 release notes and a site page entry. I wrote these inline and did not run findable or wordsmith.
- The README no longer carries the comment to delete.
- I added a `.gitignore`.
- I did not add a `LICENSE`, because you haven't chosen one. The README Status line says "not chosen yet", so update it when you pick.

**Commands for you to run.** I haven't run any of these.

1. Validate, from `project/`:
   ```bash
   python .claude/skills/tune-skill/scripts/check_skill.py skills/changelog-to-release-notes
   python -I .claude/skills/tune-skill/scripts/regress.py skills .claude/skills --baseline health.json
   ```
2. Check for a name collision:
   ```bash
   gh api "search/repositories?q=changelog-to-release-notes+in:name&per_page=10" --jq '.total_count, (.items[] | [.full_name, .stargazers_count, .description] | @tsv)'
   gh api "search/repositories?q=topic:changelog-to-release-notes&per_page=1" --jq .total_count
   ```
3. Try it once on a repo that has tags and a `CHANGELOG.md`. Ask it to "write release notes for <version>", and check that the flag table catches something real.
4. Add your `LICENSE`. Then publish, creating the repo only after steps 1–3 are clean:
   ```bash
   cd skills/changelog-to-release-notes
   git init && git add . ':!LISTING.md' && git commit -m "Add changelog-to-release-notes skill

   Co-Authored-By: Claude Sonnet 5.5 <<email>>"
   gh repo create changelog-to-release-notes --public --source=. --push \
     --description "Agent skill that turns CHANGELOG.md into customer-facing release notes and flags claims the git diff doesn't back."
   gh repo edit --add-topic agent-skill --add-topic claude-code --add-topic release-notes \
     --add-topic changelog --add-topic git-diff --add-topic documentation --add-topic developer-tools
   gh release create v1.0.0 --title "changelog-to-release-notes 1.0.0" --notes-file LISTING.md
   ```
   The `gh release create` line would post all of `LISTING.md` as the release body. Paste only the "Release notes for v1.0.0" section into a separate file and use that for `--notes-file`.

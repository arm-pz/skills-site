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
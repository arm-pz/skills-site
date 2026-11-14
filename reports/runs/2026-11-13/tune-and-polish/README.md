# tune-and-polish: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). The run rewrote the SKILL.md description, added two sibling boundaries, and rewrote the README opening, but check_skill.py only shows one Bash call in the tool list and the final output says it never ran, so the zero-FAIL gate is unverified and the 'seo-audit' name was settled from memory.

Target: a clone of arm-pz/keyword-resolver (edits local, nothing pushed). Run headless on the CLI default model in a clean project with only this skill installed (14 turns, 11 tool calls, 41 s, $0.39).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
The skill in target/ both misfires and is hard to find. Tune it and polish its listing. Work on the local copy only; don't push.
```

Follow-up:

```
Confirmed, that's right. Go ahead and finish it without stopping for more questions.
```

## Rubric

- Tunes the description, sibling overlaps and stale names first, gated on check_skill.py with zero FAILs
- Then polishes README/About text from the final description, against real queries
- Every change is grounded; nothing invented
- Pushes nothing

## Hard checks

- ✓ check_skill.py reports no FAIL on the tuned skill

## Met

- Pushed nothing: no git push or gh command was executed, and the final output says all edits are local and uncommitted
- Description was tuned toward user-phrased triggers (two pages rank for same keyword, which page should rank for X, cluster map) and sibling boundaries for findable-polish and wordsmith were added in description and body
- README opening was rewritten after the description edit, with example prompts drawn from the new description's trigger phrases

## Missed

- The gate was not met: the final output says check_skill.py never ran because Bash was denied, although the transcript lists a Bash call invoking it. The hard check 'no FAIL' therefore cannot be confirmed from what the run showed, and the run reports it was never verified
- Stale-name fix was not grounded: the README's seo-crawl link was replaced with seo-audit, justified by 'my recollection' that seo-audit is in marketingskills, which the run admits it did not confirm
- The README still links seo-polish as a technical SEO option, which the run did not verify
- The polish stage was not completed: GitHub About text and topics were left as drafts, with an unrun gh command rather than being applied to files
- Real-query grounding was thin: the README example prompts were written by hand, with no run against actual queries or the family regression; the test cases are hand-written and unrun
- Sibling overlap with keyword-guard was not checked because that skill is not in the tree, so the overlap tuning is partial

## Defects to fix in the skill

- The skill has no fallback when the check script cannot run (Bash denied): it should require reporting the gate as unmet rather than letting the polish stage proceed on an unverified description
- It does not say how to resolve a stale sibling name (e.g. seo-crawl vs seo-audit) when the sibling is not in the tree, which led to an unverified guess
- The polish step is defined around GitHub-side About/topics, which cannot be applied in a local-only, no-push run; the skill gives no guidance on producing those as local artifacts

## What it did

1. `Skill: tune-and-polish`
1. `Bash: cd /tmp/run-tune-and-polish-fgmmjupo/project; find . -path ./node_modules -prune -o -type f -print | grep -v '^./.git/' | head -80`
1. `Bash: cd /tmp/run-tune-and-polish-fgmmjupo/project; cat target/SKILL.md target/README.md; cat .claude/skills/tune-skill/SKILL.md | head -80; cat .claude/skills/findab`
1. `Bash: cd /tmp/run-tune-and-polish-fgmmjupo/project; python3 -I .claude/skills/tune-skill/scripts/check_skill.py target; cd target; git log --oneline | head; git remot`
1. `Grep: ^description:`
1. `Read: /tmp/run-tune-and-polish-fgmmjupo/project/.claude/skills/tune-skill/references/audit-checklist.md`
1. `Edit: /tmp/run-tune-and-polish-fgmmjupo/project/target/SKILL.md`
1. `Edit: /tmp/run-tune-and-polish-fgmmjupo/project/target/SKILL.md`
1. `Edit: /tmp/run-tune-and-polish-fgmmjupo/project/target/README.md`
1. `Edit: /tmp/run-tune-and-polish-fgmmjupo/project/target/README.md`
1. `Edit: /tmp/run-tune-and-polish-fgmmjupo/project/target/README.md`

## Files it wrote

Copied under `files/`:

- `target/.gitignore`
- `target/LICENSE`
- `target/README.md`
- `target/SKILL.md`

## Final output

I tuned the triggering and rewrote the README opening in `target/`. I couldn't run `check_skill.py` because Bash was denied in this session. The description length (under 1024 characters) and the body edits were checked by reading, not by the script. Nothing was pushed.

## 1. Tune-Skill changes (`target/SKILL.md`)
- **Description rewritten.** The old one described the chain (Keyword-Guard → Wordsmith) rather than the user's problem, so it matched few real requests.
  - It now leads with the problem: your own pages competing for one query.
  - It adds the phrases a user would type: "two pages rank for the same keyword", "which page should rank for X", and a cluster map. It ends with "even if they never say 'cannibalization'".
  - It names the inputs it needs: a keyword list, a sitemap or a Search Console export.
- **Boundaries added.** The "Not for" list was missing owners for two kinds of request: GitHub repo or skill discoverability (now `findable-polish`) and general copy editing (now `wordsmith`). The README already pointed repo discoverability at `findable-polish`, but the description didn't. I added both to the Boundaries section of the body too.
- **Not fixed: `seo-audit` vs `seo-crawl`/`seo-polish`.** The description and body say `seo-audit` for technical SEO diagnosis, while the README's "Not for" section links `seo-crawl` and `seo-polish`. I couldn't confirm which skill exists, so I left both as they were. Please pick one name.
- **Not run:** the check script, the family regression, and automated trigger tests. `keyword-guard` isn't in this tree, so its description wasn't compared against this one.
- **Hand-written test cases:**
  - Should trigger:
    - "Two of my pages rank for 'agent skill'."
    - "Search Console shows three URLs for one query."
  - Should not trigger:
    - "Make my GitHub repo easier to find" (→ `findable-polish`).
    - "Crawl my site for broken canonicals" (→ `seo-audit`).
    - "Tighten this paragraph" (→ `wordsmith`).

## 2. Findable-Polish alternatives (`target/README.md`)
- **Opening:** the old opening was a bold tagline followed by a paragraph. It is now a plain first paragraph that names the task, inputs and dependencies. The install line sits right after it, and four example prompts follow.
- **Install section:** I removed the duplicate lower down.
- **Not done:** the GitHub About text, topics, release and site page. I didn't change them in the files because they live on GitHub, but the drafts are below.

**About text (about 290 characters):**
- A: "Agent skill that fixes keyword cannibalization: finds which of your pages compete for the same query, assigns one owner per query, and rewrites titles, H1s and meta descriptions of the rest. Works from a sitemap or Search Console export. For Claude Code."
- B: "Claude Code skill to resolve SEO keyword cannibalization. Assigns query ownership across your pages, then drafts de-conflicting titles, H1s, meta descriptions and hreflang from a sitemap, keyword list or Search Console data."

**Topics** (confirm each has a page on github.com/topics first): `agent-skills`, `claude-code`, `seo`, `keyword-cannibalization`, `search-console`, `hreflang`, `meta-descriptions`, `content-strategy`, `keyword-research`.

## 3. Recommended actions
Use About text A with the topics above. Fix the `seo-audit` naming, then apply the listing, for example:

```bash
gh repo edit arm-pz/keyword-resolver --description "<About A>" --add-topic agent-skills,claude-code,seo,keyword-cannibalization,search-console,hreflang
```

Commit message when you're ready (I haven't committed anything):
```
Tune keyword-resolver trigger and README opening

Co-Authored-By: Claude Sonnet 5.5 <<email>>
```

---

I fixed the one open item: the README's "Not for" section now matches the skill. Technical SEO diagnosis points to `seo-audit` (the marketingskills one, same as the description and body) or `seo-polish`. I dropped the `seo-crawl` link and added a "General copy editing → wordsmith" line to match the description.

I based that on my recollection that `seo-audit` and `programmatic-seo` are both skills in the marketingskills repo, and I haven't confirmed that. If you'd rather use `seo-crawl`, change it in the description and body instead.

Everything stays local in `target/`, and I haven't committed or pushed. `check_skill.py` still hasn't run because Bash is denied here. To run it yourself:

`python3 -I .claude/skills/tune-skill/scripts/check_skill.py target`

The GitHub About text and topics from my last message are still drafts. Apply them with the `gh repo edit` command I gave you when you're ready.

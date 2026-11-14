# upstream-polish: real-world run, 2026-11-13

**Verdict: PARTIAL** (5/10). The run found two real listing drifts (seo-polish index entry still names seo-audit instead of seo-crawl; keyword-guard README calls itself Qoder-only and omits Claude Code/Cursor) and pushed nothing. It could not fetch upstream (Bash denied, GitHub 403), never read the local listing-index.json, did not mention that wordsmith had moved outside arm-pz, and quoted listing text only in paraphrase.

Target: three skill repos and their live listing on skillsmith.tech (nothing pushed). Run headless on the CLI default model in a clean project with only this skill installed (32 turns, 30 tool calls, 60 s, $0.49).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Check repos/keyword-guard, repos/seo-polish and repos/wordsmith against their upstreams and against their listing on skillsmith.tech (listing-index.json is the live discovery index). Tell me what's drifted and draft the fixes. Don't push.
```

## Rubric

- Gives a fetch-based verdict per repo (in sync, behind, diverged) and treats anything unreadable as inconclusive
- Compares each repo's description/README against its listing and names real drift, quoting both sides
- Notes wordsmith moved outside arm-pz if it sees it
- Drafts rewrites without inventing facts
- Pushes nothing

## Hard checks


## Met

- Pushed nothing and changed no files
- Said plainly that upstream state is unreadable and that it could not tell whether any repo is behind, instead of claiming 'in sync'
- Found real drift for seo-polish (index says seo-audit chain, SKILL.md/README say seo-crawl first) and keyword-guard (README 'Qoder Skill' vs listing 'Claude Code, Cursor, Qoder'; seo-audit vs seo-crawl)
- Drafted rewrites (seo-polish index description, keyword-guard README opening, Not-for section) that stay within facts in SKILL.md/README, with no invented numbers or capabilities
- Correctly counted 62 entries in the index and flagged the mismatch with the site's '60 skills plus 7 mods' without guessing a cause

## Missed

- No fetch-based verdict: the table shows 'level' for all three repos from local refs/packed-refs only; the run never completed a git fetch. This is honestly labelled but is not the required fetch-based verdict, and 'level' in the table is easy to misread as 'in sync'.
- Did not quote both sides of the drift. It paraphrased the listing ('says the skill audits with seo-audit...') because it used a WebFetch summary instead of reading the listing-index.json present in the project.
- Fetched skillsmith.tech/listing-index.json, got a 404, and fell back to the .well-known path and /skills/ page. It never read the local listing-index.json that the prompt named as the live index, and told the user the index fetch failed.
- Did not note that wordsmith moved outside arm-pz. It read wordsmith's .git/config and fetched github.com/arm-pz/wordsmith (403) but reported 'no drift found' for wordsmith.
- Did not mention that the plugin.json homepage (skills.caffeinity.com) differs from the skillsmith.tech listing host for keyword-guard and wordsmith.

## Defects to fix in the skill

- The skill hinges on Bash (upstream_check.mjs / git fetch) with no stated fallback when Bash or the network is denied. The run ended with no real fetch verdict, and the skill gives no guidance on how to report that cleanly, for example an explicit INCONCLUSIVE column.
- The skill does not tell the agent to read the provided listing-index.json file in the project first; it fetched a guessed URL, hit a 404 and worked from a paraphrased page.
- No explicit step to compare each repo's remote URL / owner against the listing's expected owner (arm-pz), so a repo that moved to another owner can pass as 'no drift'.
- Does not require drift findings to quote the listing text and the repo text verbatim side by side, so paraphrased findings are allowed.

## What it did

1. `Skill: upstream-polish`
1. `Bash: cd /tmp/run-upstream-polish-o6d30zpt/project; ls; ls repos .claude/skills .claude/skills/upstream-check; for r in keyword-guard seo-polish wordsmith; do echo "=`
1. `Glob: **/*`
1. `Glob: **/*`
1. `Read: /tmp/run-upstream-polish-o6d30zpt/project/repos/keyword-guard/SKILL.md`
1. `Read: /tmp/run-upstream-polish-o6d30zpt/project/repos/seo-polish/SKILL.md`
1. `Read: /tmp/run-upstream-polish-o6d30zpt/project/repos/wordsmith/README.md`
1. `Read: /tmp/run-upstream-polish-o6d30zpt/project/repos/keyword-guard/.git/config`
1. `Read: /tmp/run-upstream-polish-o6d30zpt/project/repos/seo-polish/.git/config`
1. `Read: /tmp/run-upstream-polish-o6d30zpt/project/repos/wordsmith/.git/config`
1. `ToolSearch: `
1. `WebFetch: https://skillsmith.tech/listing-index.json`
1. `Read: /tmp/run-upstream-polish-o6d30zpt/project/repos/keyword-guard/README.md`
1. `Read: /tmp/run-upstream-polish-o6d30zpt/project/repos/seo-polish/README.md`
1. `Read: /tmp/run-upstream-polish-o6d30zpt/project/repos/keyword-guard/.claude-plugin/plugin.json`
1. `Read: /tmp/run-upstream-polish-o6d30zpt/project/repos/wordsmith/.claude-plugin/plugin.json`
1. `Read: /tmp/run-upstream-polish-o6d30zpt/project/repos/keyword-guard/.git/packed-refs`
1. `Read: /tmp/run-upstream-polish-o6d30zpt/project/repos/seo-polish/.git/packed-refs`
1. `Read: /tmp/run-upstream-polish-o6d30zpt/project/repos/wordsmith/.git/packed-refs`
1. `Read: /tmp/run-upstream-polish-o6d30zpt/project/repos/keyword-guard/.git/refs/heads/master`
1. `Read: /tmp/run-upstream-polish-o6d30zpt/project/repos/seo-polish/.git/refs/heads/master`
1. `Read: /tmp/run-upstream-polish-o6d30zpt/project/repos/wordsmith/.git/refs/heads/main`
1. `WebFetch: https://skillsmith.tech/`
1. `WebFetch: https://skillsmith.tech/.well-known/agent-skills/index.json`
1. `WebFetch: https://skillsmith.tech/skills/`
1. `Glob: **/*.md`
1. `WebFetch: https://github.com/arm-pz/wordsmith`
1. `WebFetch: https://github.com/arm-pz/keyword-guard`
1. `WebFetch: https://github.com/arm-pz/seo-polish`
1. `Read: /tmp/run-upstream-polish-o6d30zpt/project/repos/wordsmith/skills/wordsmith/SKILL.md`

## Files it wrote

Copied under `files/`:

- `listing-index.json`
- `repos/keyword-guard/.claude-plugin/plugin.json`
- `repos/keyword-guard/LICENSE`
- `repos/keyword-guard/README.md`
- `repos/keyword-guard/SKILL.md`
- `repos/keyword-guard/references/cannibalization-audit.md`
- `repos/keyword-guard/references/link-authority.md`
- `repos/keyword-guard/references/on-page-checklist.md`
- `repos/seo-polish/.gitignore`
- `repos/seo-polish/LICENSE`
- `repos/seo-polish/README.md`
- `repos/seo-polish/SKILL.md`
- `repos/wordsmith/.claude-plugin/plugin.json`
- `repos/wordsmith/LICENSE`
- `repos/wordsmith/README.md`
- `repos/wordsmith/skills/wordsmith/SKILL.md`
- `repos/wordsmith/skills/wordsmith/examples/example.md`
- `repos/wordsmith/skills/wordsmith/references/commands.md`
- `repos/wordsmith/skills/wordsmith/references/output-formats.md`
- `repos/wordsmith/skills/wordsmith/references/quality-checklist.md`
- `repos/wordsmith/tests/test-discovery.md`
- `repos/wordsmith/tests/test-prompts.md`

## Final output

Two of the three repos have drifted from their listing, and I couldn't check upstream, so I can't tell you whether any of them are behind. I drafted the fixes below, changed no files, and pushed nothing.

## What I couldn't check

- **Upstream state.** Bash is denied in this session, so I couldn't run `upstream_check.mjs`, `git fetch` or the credential screen. GitHub also returned 403 to my fetches.
- **What I did read.** In each repo the local branch hash equals the stored `origin` ref (keyword-guard `c187c8a`, seo-polish `6396aa3`, wordsmith `7f7f4c7`). That means nothing is committed locally that the remote lacked at your last fetch. It says nothing about whether the remotes have moved since. Run `git fetch && git status -sb` in each repo to confirm.
- **Listing data.** `skillsmith.tech/listing-index.json` returns 404. I used `/.well-known/agent-skills/index.json` and the `/skills/` page instead. The fetch tool paraphrased the index descriptions rather than quoting them, and the index has no version or topics fields.

## Verdicts

| Repo | Local vs `origin` (last fetch) | Listing |
|---|---|---|
| keyword-guard | level | drifted (README) |
| seo-polish | level | drifted (index entry) |
| wordsmith | level | no drift found |

## Drift

1. **seo-polish: the index entry is stale (Medium).** It says the skill audits with seo-audit and chains seo-audit into wordsmith. `SKILL.md` now runs seo-crawl first for measured evidence, treats seo-audit as optional, and requires seo-crawl. The `/skills/` page and the README already say this, so only the index entry is behind.
2. **keyword-guard: the README is stale (Medium).**
   - It calls the skill "A Qoder Skill" with a `~/.qoder/` install only, but the index says it runs in Claude Code, Cursor and Qoder.
   - It describes seo-audit as the "technical diagnosis" companion, but `SKILL.md` now points to seo-crawl.
   - It has no "Not for" section, though `SKILL.md` hands off to seo-crawl, keyword-resolver and programmatic-seo.
   - Its layout tree omits `LICENSE` and `.claude-plugin/`.
3. **Site count (Low).** The index has 62 entries and the `/skills/` page says 60 skills plus 7 mods. I can't tell from here which entries explain the gap.
4. **wordsmith: no drift.** The README lists 44 commands in 5 groups, which matches `plugin.json` and the index. Its `SKILL.md` is under `skills/wordsmith/`, which the README install path reflects. I couldn't compare the contents against the published archive digest.

## Drafted fixes

### 1. seo-polish index description
- **A (recommended):** "Measures SEO health with seo-crawl, adds an optional seo-audit diagnosis, then drafts optimized titles, meta descriptions, headings and internal-link anchors with Wordsmith for every High and Medium finding. Not for keyword cannibalization (keyword-resolver) or mass page generation (programmatic-seo)."
- **B:** "Full SEO audit plus rewrites: seo-crawl's measured findings, seo-audit when installed, then Wordsmith alternatives for titles, meta descriptions, headings and anchors."
- **C:** "Crawl-backed SEO diagnosis with copy-ready fixes. Runs seo-crawl, optionally seo-audit, then Wordsmith, and ranks the fixes by severity."

Option A matches the `SKILL.md` boundaries most closely.

### 2. keyword-guard README
Replace the opening paragraph:
- **A (recommended):** "An Agent Skill for planning SEO topic clusters and eliminating **keyword cannibalization**, so exactly one page wins each query. It builds a query-ownership map before any content change, with a sitemap and query-intent fallback audit for when you have no Search Console access."
- **B:** "Plan topic clusters and make exactly one page win each query. keyword-guard puts a cannibalization audit ahead of every content change and works with or without Search Console."

Replace the complementary-skills bullet:
> Complements `seo-crawl` (measured crawl and index evidence, with the third-party `seo-audit` for deeper diagnosis) and `programmatic-seo` (page scale). Hand copy rewrites to `keyword-resolver` once ownership is settled.

Add after "What it does":
```md
## Not for
- Crawl and index health → seo-crawl
- Rewriting copy once ownership is settled → keyword-resolver
- Mass page generation → programmatic-seo
```
Update the install section to give the `npx skills add` command first and name `.claude/skills/`, `.cursor/skills/` and `.qoder/skills/` as equal options. Add `LICENSE` and `.claude-plugin/` to the layout tree.

### 3. Site count
Regenerate `listing-index.json` and the `/skills/` header count from the same source so they can't diverge. Until you know which two entries are extra, I wouldn't edit either number.

## Recommended actions
1. Run `git fetch && git status -sb` in all three repos. If any is behind, pull before committing.
2. Apply fix 2 to the keyword-guard README and commit it locally. Apply fix 1 to the site's index source, then rebuild the index. Neither needs a `gh repo edit`.
3. Let me run the real `upstream_check.mjs` and `drift_check.mjs` if you allow Bash. I can also fetch the actual `listing-index.json` if you give me its correct URL.

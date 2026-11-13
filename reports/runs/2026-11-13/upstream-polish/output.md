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
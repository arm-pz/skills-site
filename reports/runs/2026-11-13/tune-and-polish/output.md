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
# tune-* cannibalization resolution — skillsmith.tech

Method: keyword-guard pre-GSC fallback (sitemap + page content + query intent). No Search Console data was available, so ownership is by semantic fit, not clicks/impressions. Re-check against GSC `page + query` after ~4 weeks.

**Caveat — current tags not verified.** I could only read page text, not the raw `<head>`. The only current value seen is the top line of /tune-skill/: "tune-skill — Audit and Fine-Tune an Existing Agent Skill" (likely H1). Current titles/meta for the other three are unknown. Before applying, grep the live `<title>`, `<h1>` and meta description for "tune" and "skill" to confirm the overlap.

## What each page is

| URL | What it is | Searcher intent |
|---|---|---|
| /tune-skill/ | The validator/auditor: reads a SKILL.md, flags trigger/overlap/stale issues, 16-check `check_skill.py` | "audit/fix my SKILL.md" |
| /tune-skill-mod/ | Claude Code mod: blocks git push/PR/release after a SKILL.md edit until the validator passes | "run skill checks before push automatically" |
| /tune-and-polish/ | Workflow: tune-skill, then findable-polish on README/About/site copy | "fix the skill and its listing copy together" |
| /tune-and-ship/ | Workflow: tune, fact-check, polish, open one release PR, verify live | "release a skill end to end" |

The shared stem "tune" / "tune skill" is the conflict. It appears in all four URLs, and "tune-skill" is the literal name of the dependency in the other three.

## Ownership map (one query, one owner)

| Query theme | Owner | Others must |
|---|---|---|
| "tune skill", "audit SKILL.md", "SKILL.md validator", "fix skill description / trigger overlap" | **/tune-skill/** | Not use "tune skill" or "audit SKILL.md" as a primary phrase |
| "pre-push skill check", "block git push until skill validated", "Claude Code hook for SKILL.md" | **/tune-skill-mod/** | Use hook/gate/push language, not "tune skill" |
| "fix skill and listing copy", "skill description + README polish" | **/tune-and-polish/** | Use "two-step: file then listing copy" language |
| "release a skill", "skill release PR", "publish skill and verify live" | **/tune-and-ship/** | Use release/PR/verify language |

Rule applied: the bare keyword goes to the page that *is* the thing (/tune-skill/). Dependents are named by their distinct job. They may mention "tune-skill" in body text as a link, but not in title/H1 as the primary keyword.

Conflicts found:
1. **/tune-skill/ vs /tune-skill-mod/**: highest risk. The mod's name is the owner's name plus "mod", so it will match every "tune skill" query. Fix: the mod's title/H1 lead with the push-gate behavior.
2. **/tune-and-polish/ vs /tune-and-ship/**: both are "tune + extra step" workflows with near-identical stems and both include a tune step plus polish. Fix: split by outcome. Polish is copy alignment; ship is release PR.
3. **Workflow pages vs /tune-skill/**: both describe auditing descriptions and overlaps. Workflow pages should not claim the audit itself.

## Rewrites

Titles ≤ 60 chars, meta ≤ 155 chars. Facts used only from the pages (MIT, free, 16 checks, hooks run with your permissions, etc.). The recommended option is marked ★.

### /tune-skill/ — owner (keep the keyword, sharpen it)
- Title ★: `Tune Skill: Audit and Fix an Existing SKILL.md` (46)
- H1 ★: `Tune Skill — audit and fix an existing SKILL.md`
- Meta ★: `Free, open-source auditor for an existing SKILL.md. Checks the trigger description, sibling overlaps and stale names, then proposes the smallest edit.` (151)
- Alt B title: `SKILL.md Auditor: Find Trigger and Overlap Problems`
- Alt B meta: `Open-source MIT validator for agent skills. Quotes each problem line, rates severity, suggests the minimal fix. Works with Claude Code, Codex, Cursor.`

### /tune-skill-mod/ — non-owner, de-optimize
- Title ★: `Pre-Push Gate for SKILL.md Edits (Claude Code Mod)` (50)
- H1 ★: `Block git push until your edited SKILL.md passes validation`
- Meta ★: `Claude Code mod that pauses git push, pull requests and releases after a SKILL.md edit until the validator passes. Read its hooks before installing.` (150)
- Alt B title: `Skill Push Guard: Claude Code Hook Mod`
- Alt B H1: `Stop unvalidated skill edits from being pushed`
- Alt C title: `Validate Skills Before Release: Claude Code Mod`

### /tune-and-polish/ — non-owner, own "fix file, then listing copy"
- Title ★: `Fix a Skill, Then Rewrite Its Listing Copy` (42)
- H1 ★: `Fix the skill file first, then polish README and site copy`
- Meta ★: `Two-phase agent skill: audit the SKILL.md until the validator passes, then rewrite README, About and site copy against real search queries. MIT, free.` (152)
- Alt B title: `Skill Audit + Listing Copy Polish Workflow`
- Alt B H1: `One pass: correct the skill, then match its listing to it`

### /tune-and-ship/ — non-owner, own "release"
- Title ★: `Release a Published Skill: Fact-Check to Live PR` (48)
- H1 ★: `Take one skill from audit to a verified release PR`
- Meta ★: `Agent skill that tunes one published skill, fact-checks versions, flags and prices against primary sources, polishes the listing, opens one release PR.` (153)
- Alt B title: `Skill Release Workflow: Fact-Check, PR, Verify Live`
- Alt B H1: `Ship a skill update with one release PR`

Check: no two titles/H1s share "tune skill" as a primary phrase after the rewrite; only /tune-skill/ keeps it. (Note: the URL slugs still contain "tune"; leave them. Changing slugs would need 301s and is out of scope.)

## Internal linking
- /tune-skill-mod/, /tune-and-polish/, /tune-and-ship/ each link to /tune-skill/ with anchor `tune-skill` (or "the SKILL.md auditor") in the first paragraph. /tune-skill/ already gets this from the mod page.
- /tune-skill/ gets a short "Use it with" block linking: mod (anchor "pre-push gate"), polish (anchor "fix the listing copy too"), ship (anchor "release workflow"), with distinct anchors, not "tune".
- /tune-and-polish/ ↔ /tune-and-ship/: link each way with "need a release PR?" / "only need listing copy?" to route intent.
- Keep self-referencing canonicals; no cross-canonicals.

## Not done / follow-ups
- Site not changed, as requested; these are copy-paste values only.
- Verify current head tags, then confirm with GSC after indexing.
- Also check /findable-polish/ and /keyword-resolver/ for "skill audit" overlap; out of scope here.
- The pages state no live-session trigger testing for tune-skill. Don't add claims of proven results to the copy.

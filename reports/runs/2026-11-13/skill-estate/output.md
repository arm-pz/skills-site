**Phase 1 (inventory and reconcile) is done, with one limit: I didn't run the full `upstream-check` drift checker.** Bash was denied in this session, so I used file search and reads instead. That means I haven't checked push state (push-ready, behind, diverged) or how the repos compare to their remotes. Nothing was changed or published.

**Counts**
- **Local clones:** 7 repos in `repos/`, all with an `arm-pz/<name>` GitHub origin.
- **Live listing:** `listing-index.json` has 62 skill entries.
- **Local coverage:** all 7 repos are in the listing, and I found no local repo missing from it.
- **Remaining 55 entries:** they have no clone here, so I can't confirm a `SKILL.md` exists for them. That includes `caffeinity-routing` and `course-builder`, which carry the same marketplace description (probably a copy-paste error in the index).

**Inventory**

| Repo | Kind | Listed | Notes |
|---|---|---|---|
| choose-effort | skill | yes | `SKILL.md` at root |
| keyword-guard | skill, with `plugin.json` | yes | has `references/` |
| keyword-resolver | skill | yes | |
| seo-polish | skill | yes | |
| session-retrace | skill | yes | |
| straight-prose | skill, with `plugin.json` | yes | |
| wordsmith | skill, with `plugin.json` | yes | `SKILL.md` is nested at `skills/wordsmith/`, unlike the others |

All 7 are skills, so none are mods or non-skill repos. Names in each `SKILL.md` match the listing names, so I found no renames.

**Drift to carry into phase 2**
- Only 7 of 62 listed skills can be checked locally. The other 55 need clones, or a GitHub listing of `arm-pz`, to count against.
- Each listing's `digest` could be compared to the current repo HEAD. I haven't done that.
- The `wordsmith` layout differs from the other repos. The manifest needs a path field for it.
- The `caffeinity-routing` and `course-builder` entries share the same marketplace description. It looks wrong for `course-builder`, but I haven't confirmed that.

**Owner actions pending**
- Re-enable Bash, or tell me to continue with file tools only. Then I can finish the push-state and drift checks.
- Give me clones of the other 55 repos, or an `arm-pz` repo listing, so I can finish the reconciliation.

I'm stopping at the phase 1 gate. Phase 2 will wait until you say to go ahead.
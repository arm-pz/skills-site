# discovery-kit.md: arm-pz/tune-skill

Produced by running `findable` (arm-pz/findable, skills/findable/SKILL.md) on 2026-10-23.
Nothing public was changed; every command in section 8 waits for the owner's go-ahead.

## 0. Baseline

| Query | Project found? | Who ranks instead | Where those are listed |
| --- | --- | --- | --- |
| `tune-skill agent skill` | no | hburaktasyurek/agent-skills-and-commands `tune-skill`; kevinveenbirkenbach `autotune` | skills.sh, a personal Gitea |
| `arm-pz/tune-skill github` | no | the same hburaktasyurek listing; catlog22 `skill-iter-tune` | skills.sh, claudeskills.info, skillselion.com |
| `fix agent skill not triggering SKILL.md description audit` | no | Gumloop help, DataCamp course, Smartscope blog | vendor docs and blogs, not skills |
| `claude code skill that improves another skill's description and test cases` | no | Anthropic skill-creator, MLflow blog | official plugin marketplace, blogs |
| `skills.caffeinity.com` | no | unrelated coffee and skills sites | — |

Directory check: skills.sh lists 2 arm-pz skills (`wordsmith` with 1 install, `pre-ship-security-red-team`);
`skills.sh/arm-pz/tune-skill` returns 404. Indexing follows installs there, so the other ~40 skills are invisible.

Metadata gaps (from the clone; About and topics could not be read through this session's API):
README opening names the task but not the audience or the agents it runs in; no tagged release in
the clone; the plugin version is 0.1.0.

## 1. Target queries

1. fix a skill that is not triggering
2. audit agent skill description
3. skill fires on the wrong requests
4. two agent skills overlap
5. validate SKILL.md frontmatter
6. SKILL.md linter
7. claude code skill review checklist

## 2. Name decision

A direct, same-purpose project shares the name: `hburaktasyurek/agent-skills-and-commands` ships a
`tune-skill` (improves one existing skill against an observed complaint, PDCA loop) and is listed on
skills.sh while arm-pz/tune-skill is not. Options: keep the name and qualify it everywhere ("tune-skill
by arm-pz, the SKILL.md auditor with a validator script"), or rename while installs are near zero
(for example `skill-tuner` or `skill-audit`). Renaming would also touch draft-skill, skill-launch,
tune-and-polish, caffeinity-routing and the site, so the owner decides.

## 3. GitHub listing

**About (description, 350 character limit):**

```
Agent skill that audits an existing SKILL.md: why it does not trigger, where it overlaps a sibling skill, stale names and counts, broken handoffs. Ships check_skill.py, a no-dependency SKILL.md linter. Works with Claude Code, Cursor, Codex and Qoder.
```

**Topics:** `agent-skills`, `claude-code`, `claude-skills`, `skill-md`, `linter`, `prompt-engineering`, `cursor`, `codex`, `qoder`, `developer-tools`

Homepage: https://skills.caffeinity.com/tune-skill/

## 4. README opening

> # tune-skill
>
> An agent skill that audits a SKILL.md you already have: why it does not trigger, where it fights a
> sibling skill for the same request, stale names and counts, and broken handoffs. It makes the
> smallest evidenced edit and checks it with `check_skill.py`, a SKILL.md linter you can also run on
> its own. Works in Claude Code, Cursor, Codex and Qoder.
>
> `npx skills add arm-pz/tune-skill --skill tune-skill`
>
> Ask it things like: "my skill isn't triggering", "these two skills keep fighting", "review this SKILL.md before I publish".
>
> Not the same project as hburaktasyurek's `tune-skill`. Siblings: `draft-skill` writes a new skill, `prompts-to-skill-release` packages one.

## 5. Release notes

v0.2.0: syncs the repo with the marketplace copy; `check_skill.py` now fails an unquoted `: ` in
frontmatter without PyYAML; adds `test_check_skill.py`. Install: `npx skills add arm-pz/tune-skill --skill tune-skill`.

## 6. Site page

The generated page at /tune-skill/ already carries the install line; section 4's opening sentence should replace its lede.

## 7. Distribution

| Directory | Lists competitors? | How it ingests | Entry text |
| --- | --- | --- | --- |
| skills.sh | yes (hburaktasyurek tune-skill) | by `npx skills add` installs; no form found | install once from a clean machine; the About above |
| claudeskills.info | yes (skill-iter-tune) | not checked | the About above |
| skillselion.com | yes (skill-tuning) | not checked | the About above |

## 8. Apply commands (owner's go-ahead required)

```bash
gh repo edit arm-pz/tune-skill \
  --description "Agent skill that audits an existing SKILL.md: why it does not trigger, where it overlaps a sibling skill, stale names and counts, broken handoffs. Ships check_skill.py, a no-dependency SKILL.md linter. Works with Claude Code, Cursor, Codex and Qoder." \
  --homepage "https://skills.caffeinity.com/tune-skill/" \
  --add-topic agent-skills,claude-code,claude-skills,skill-md,linter,prompt-engineering,cursor,codex,qoder,developer-tools
gh release create v0.2.0 --repo arm-pz/tune-skill --title "v0.2.0" --notes-file notes.md
```

## 9. Re-check plan

Re-run the five baseline queries and the skills.sh check on 2026-11-13 (three weeks), after the
listing and the site redeploy, and compare against section 0.

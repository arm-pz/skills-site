# discovery-kit.md: arm-pz/draft-skill

Produced by running `findable` (arm-pz/findable) on 2026-10-24, after the owner searched Google for
"draft ai skill" and did not find it. Public changes go out by PR (README, site page) or by the
owner's own `repo_metadata.py --apply --about` (About and topics are repo settings).

## 0. Baseline

| Query | Project found? | Who ranks instead |
| --- | --- | --- |
| `draft ai skill` (Google, owner's phone) | no | skilldraft.io ("Quality-scored SKILL.md files for every AI…"), TypingMind "Draft la … AI Skill" |

What the page said: title "draft-skill — Author a New Agent Skill From a Plain Idea"; H1 a slogan;
"agent skill" 9 times, "AI skill" 0 times. Repo: 0 stars, 10 topics, homepage set. The domain
served the 2026-10-20 build until 2026-10-24 and has no Search Console property, so Google's copy
is stale.

## 1. Target queries

1. draft an AI skill
2. create a SKILL.md from an idea
3. write a new Claude Code skill
4. AI agent skill generator
5. how to write a skill description that triggers
6. scaffold a Codex skill
7. make a Cursor agent skill

## 2. Name decision

No same-name project found. Same-job projects: Anthropic's `skill-creator`, skilldraft.io (a hosted
generator). Keep the name; the README says how it differs.

## 3. GitHub listing

**About (description, 350 character limit):**

```
AI agent skill that drafts a new SKILL.md from a plain idea: confirms the purpose first, checks your installed skills for overlap, writes a description that actually triggers, and validates it with a script. Open source, for Claude Code, Codex, Cursor and Qoder.
```

**Topics:** `agent-skill`, `agent-skills`, `ai-agents`, `claude-code`, `claude-skills`, `developer-tools`, `documentation`, `prompt-engineering`, `qoder`, `skill-creation`, `skill-md`, `codex`, `cursor`

Homepage: https://skills.caffeinity.com/draft-skill/ (already set)

## 4. README opening

Applied by PR in arm-pz/draft-skill: the first paragraph now names the job in searchers' words
(draft a new AI agent skill, a SKILL.md, for Claude Code, Codex, Cursor and Qoder), and a sibling
line points at prompts-to-skill, tune-skill and Anthropic's skill-creator.

## 6. Site page

Applied by PR in arm-pz/skills-site: title "draft-skill: Draft a New AI Agent Skill (SKILL.md) From
an Idea", a matching meta description, and a subline under the H1 with the same words.

## 8. Apply commands (owner)

```
cd skills-site
python tools/agent-skills/repo_metadata.py --apply --about
```

Then in Google Search Console: request indexing of https://skills.caffeinity.com/draft-skill/.

## 9. Re-check plan

On 2026-11-10, search the seven target queries and `draft ai skill` again; record position (or
absence) for the page and the repo next to this baseline.

`check_listing.py`: About 262/350, 13 topics, title 63 characters, meta 155 characters: OK.

## Re-check, 2026-11-10

Same eight queries, through Claude's web search (not Google; the owner's own Google check is the one
that counts).

| Query | Found? | Who ranks instead |
| --- | --- | --- |
| draft ai skill | no | TypingMind "Draft" skills, Thomson Reuters CoCounsel, skill directories (killer-skills, skillselion, claudskills) |
| draft an AI skill | no | Appian, Creatio and Astera docs; claudemarketplaces |
| create a SKILL.md from an idea | no | skill-forge, skills.sh, skillsdirectory, claudepluginhub, tessl |
| write a new Claude Code skill | no | skills.sh, skillselion, smithery, playbooks, claudskills |
| AI agent skill generator | no | arXiv SkillGenBench, apify, tessl, skills.sh, agentskill.sh |
| how to write a skill description that triggers | no | dev.to and blog guides, agentskills.io |
| scaffold a Codex skill | no | OpenAI Codex docs, skillselion, playbooks |
| make a Cursor agent skill | no | Cursor docs, skills.cat, mcp.directory |

What changed since the baseline: the site moved to skillsmith.tech (skills.caffeinity.com now 301s,
canonicals and sitemap point at the new domain), so whatever Google had indexed restarts there. Neither
domain appears for `skillsmith.tech draft-skill` or `skills.caffeinity.com draft-skill`, so the site
is not indexed by this engine yet. The repo's About text and topics were not applied
(`repo_metadata.py --apply --about` has not run): About still opens "Agent skill that creates…", 10
topics, 0 stars.

What the results show: directories own these queries (skills.sh, skillselion, claudskills, tessl,
agentskill.sh, skillsdirectory, claudepluginhub, mcp.directory, playbooks). They list skills from
GitHub, which is the cheapest way in.

New collision: "Skillsmith" is already used by an MCP Market tool that "drafts, validates, and
packages Claude Skills" (mcpmarket.com/tools/skills/skillsmith-1), by a skillsmith in the aiwg npm
package, and by a Skywork skill hub. Same job as draft-skill under the new brand name; the owner
decides whether to qualify it ("Skillsmith by Caffeinity" everywhere) or rename.

Next fixes, in order: (1) owner runs `repo_metadata.py --apply --about` (now also moves homepages off
skills.caffeinity.com); (2) Search Console: verify skillsmith.tech, submit its sitemap, use Change of
Address from the old property, request indexing of /draft-skill/; (3) submit to agentskill.sh,
skillsdirectory and claudepluginhub (DIRECTORIES.md); (4) re-check on 2026-12-01.

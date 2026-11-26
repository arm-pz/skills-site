# Getting listed

Where the caffeinity skills can be found besides this site, how each place takes them in, and what
is left to do. Checked 2026-10-24; directories change their rules, so re-check a page before you
submit. Nothing here is submitted automatically: every entry below goes out under your own account.

## Already done by the pipeline

| Surface | How | Where |
| --- | --- | --- |
| This site's discovery index | `/.well-known/agent-skills/index.json`, so `npx skills add https://skillsmith.tech` lists every skill | built by `publish.yml` |
| `/llms.txt` | install commands and every skill, for agents and AI search | built by `publish.yml` |
| Sitemap and JSON-LD | sitemap, ItemList, WebSite and Organization data on the hub | built by `publish.yml` |
| Claude Code marketplace | `/plugin marketplace add arm-pz/caffeinity-skills` | arm-pz/caffeinity-skills |
| Codex marketplace | `codex plugin marketplace add arm-pz/caffeinity-skills` | arm-pz/caffeinity-skills |
| Profile README | generated skills block | arm-pz/arm-pz |

## Once, from your machine: GitHub topics and homepages

Directories and GitHub search read repo topics and the homepage link. Applied to every published repo on 2026-11-22 (65 changed); rerun after adding a skill.

```
cd skills-site
python tools/agent-skills/repo_metadata.py            # dry run: what would change
python tools/agent-skills/repo_metadata.py --apply    # apply (uses your `gh auth login`)
```

It only adds: topics `agent-skills claude-code claude-skills skill-md codex cursor` (mods get
`claude-code-plugin claude-code-mod`), and a homepage pointing at the skill's page where none is
set. About text is left alone. Re-run it after adding a skill. Cloud sessions cannot write repo
settings, so this one runs locally.

## Submit by hand

| Directory | How it takes skills in | What to submit | Status |
| --- | --- | --- | --- |
| Anthropic community plugins (`claude-community` marketplace in Claude Code and Cowork) | developer portal at [claude.ai/directory/manage](https://claude.ai/directory/manage) (the old clau.de form link now redirects to [the docs](https://claude.com/docs/directory/publish)); paid account, accept the Software Directory Terms; validation and security scan on every version, a person reviews new listings; the first organization to submit a repo folder owns the listing. PRs to the GitHub mirror are closed | `arm-pz/caffeinity-directory`, folder `plugin` (the Markdown-only directory edition: the full bundle was blocked because non-Verified organizations may not ship scripts or install commands). Text: the plugin's own README | submitted 2026-11-22 (`main @ b69c55b`, validation passed with 6 warnings); awaiting the security scan and review |
| [agentskill.sh](https://agentskill.sh/submit) | paste a public repo URL; indexed automatically | `https://github.com/arm-pz/caffeinity-skills`, then any single-skill repo you want listed on its own | not listed: anonymous import of caffeinity-skills on 2026-11-22 was refused (429 rate limit), then failed (502); `@arm-pz` still 404. Next: sign in and Connect GitHub, or import a single-skill repo |
| [skillsdirectory.com](https://www.skillsdirectory.com/) | submission form; reviewed before publishing | the marketplace repo | not submitted: needs your sign-in (submit redirects to sign-in) |
| [claudepluginhub.com](https://www.claudepluginhub.com/) | submit a repo with `.claude-plugin/plugin.json` for indexing | `arm-pz/caffeinity-skills` | not submitted: the submit page shows a Cloudflare bot check, so submit from your own browser |
| [skills.sh](https://www.skills.sh/) | no form: a skill appears once people install it with `npx skills add`, ranked by installs | nothing to submit; link to install commands from the README and site | 2 skills listed on 2026-10-23 (wordsmith, pre-ship-security-red-team) |
| [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | pull request adding one line; its CONTRIBUTING closes PRs for skills under 10 GitHub stars and PRs written or submitted with AI help | the "Awesome-list line" below, submitted by you, once caffeinity-skills has 10+ stars | waiting on stars |

Do not install skills yourself from many machines to climb skills.sh; it counts installs, and
padding them is the kind of signal directories delist for.

### Marketplace entry

> **Caffeinity skills**: 68 open agent skills and 12 workflow agents in one Claude Code plugin, plus 7 mods:
> skill authoring and tuning, release checks (exposure, security red team, performance, go/no-go),
> SEO, writing and content, cold outbound, job search, research and decisions, learning and
> course design. Every skill is plain markdown with its own repo, page and trigger tests; no API
> keys. Install: `/plugin marketplace add arm-pz/caffeinity-skills` then
> `/plugin install caffeinity@caffeinity-skills`. Browse: https://skillsmith.tech

### Awesome-list line

```
- [Caffeinity skills](https://github.com/arm-pz/caffeinity-skills) - 68 agent skills wired into twelve workflows (skill authoring, discovery, release gates, SEO, outbound, job search, decisions, learning, solo launches), with a router skill, workflow agents and trigger tests. Site: https://skillsmith.tech
```

The plan for which skills to lead with and where to post is in `GROWTH.md`.

## After submitting

Change the status column above, and re-check in two weeks: search the directory for the skill,
note whether it is listed and how it is described. `findable` (Workflow 2 · get-found) does this re-check per repo.

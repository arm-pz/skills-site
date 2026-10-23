# skills-site

A static site and publish pipeline for a catalog of agent skills. Each skill
(a SKILL.md repo) or Claude Code mod gets its own landing page with a one-line
install command; the hub lists them all with a live filter; and a
`/.well-known/agent-skills/index.json` discovery index lets anyone run
`npx skills add https://your-domain`. One GitHub Actions workflow tests, builds
and verifies the site before each Cloudflare Pages deploy, and opens a pull
request when a new skill repo appears. Plain HTML, CSS and Python, no
framework. It is the source of [skills.caffeinity.com](https://skills.caffeinity.com/).

Fork it for your own skills: list them in `site/skills.json`, then follow
[Run locally](#run-locally). Every page is self-contained, and the shared design
tokens live in one `:root` block per page.

Related: [caffeinity-skills](https://github.com/arm-pz/caffeinity-skills) is
the plugin marketplace for the same skills, and
[publish-pipeline](https://github.com/arm-pz/publish-pipeline) is the agent
skill that sets up and repairs this kind of pipeline.

## Run locally

    python tools/agent-skills/build.py          # needs the GitHub CLI, `gh auth login`
    python tools/agent-skills/gen_sitemap.py --write
    bash tools/agent-skills/make_dist.sh
    python -m http.server 8080 --directory dist

## Deploy

CI publishes on every push to `main` and every hour. `.github/workflows/publish.yml`
first runs `sync.py`, which brings `site/skills.json` in line with GitHub (new
skill repos, moved repo HEADs, renames, removals), then rebuilds the site, gates
it with `check_dist.py` and `verify.mjs`, deploys `dist/` to Cloudflare Pages
only when the build differs from what is live, proves the live result, and
commits the sync back to `main`. `.github/workflows/health.yml` runs tune-skill's
regression check over every published skill each night. `PROJECT.md` maps the
whole ecosystem. A manual deploy needs the same build first:

    python tools/agent-skills/build.py
    python tools/agent-skills/gen_sitemap.py --write
    bash tools/agent-skills/make_dist.sh
    npx wrangler pages deploy dist --project-name <your-project>

A deploy replaces the whole production artifact set, so `dist/` has to hold
every page, tarball and index you want live — not only the new ones. If `dist/`
holds a partial tree, the deploy deletes the rest of the site, and a request for
a removed path still answers HTTP 200 with the hub page instead of a 404.
Check which tree you are in before deploying: more than one local clone of this
repo exists, and the last one to upload is what the domain serves.

## The skills it hosts

`site/skills.json` is the single publication decision. Every public arm-pz repo
with one SKILL.md and an About is added to it by the hourly sync; `site/deny.json`
keeps out third-party-origin repos and bundles that would publish a skill twice.
Each entry has a hand-written page under `<name>/index.html` or a generated page
built from its repo, and every page links to its source repo under
[arm-pz](https://github.com/arm-pz).

## Related

The skills themselves install with `npx skills add arm-pz/<repo>`; most of
them are bundled as Claude Code plugins in the
[caffeinity-skills marketplace](https://github.com/arm-pz/caffeinity-skills).

## License

MIT — see [LICENSE](LICENSE).

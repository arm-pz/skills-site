# skills-site — a static hub for agent skills

The source of [skills.caffeinity.com](https://skills.caffeinity.com): one
single-file landing page per agent skill, plus a hub index, downloadable
archives and machine-readable discovery indexes at `/.well-known/agent-skills/`
and `/agent-skills/`. Pages, cards and indexes are generated from
`site/skills.json`; the site itself is plain HTML, CSS and self-hosted fonts,
deployed to Cloudflare Pages.

Fork it if you want a site like this for your own skills: every page is
self-contained, and the shared design tokens live in one `:root` block.

## Run locally

    python tools/agent-skills/build.py          # needs the GitHub CLI, `gh auth login`
    python tools/agent-skills/gen_sitemap.py --write
    bash tools/agent-skills/make_dist.sh
    python -m http.server 8080 --directory dist

## Deploy

CI publishes on every push to `main`. `.github/workflows/publish.yml` rebuilds
the site, gates it with `check_dist.py` and `verify.mjs`, deploys `dist/` to
Cloudflare Pages and proves the live result. A manual deploy needs the same
build first:

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

`site/skills.json` is the single publication decision. Each entry has a
hand-written page under `<name>/index.html` or a generated page built from its
repo, and every page links to its source repo under
[arm-pz](https://github.com/arm-pz). Scheduled discovery shape-tests new public
repos and opens one `proposal/<date>` PR per batch; merging that PR deploys the
new pages. `site/deny.json` keeps third-party-origin repos out.

## Related

The skills themselves install with `npx skills add arm-pz/<repo>`; most of
them are bundled as Claude Code plugins in the
[caffeinity-skills marketplace](https://github.com/arm-pz/caffeinity-skills).

## License

MIT — see [LICENSE](LICENSE).

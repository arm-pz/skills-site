# skills-site

A static site and publish pipeline for a catalog of agent skills. Each skill
(a SKILL.md repo) or Claude Code mod gets its own landing page with a one-line
install command; the hub lists them all with a live filter; and a
`/.well-known/agent-skills/index.json` discovery index lets anyone run
`npx skills add https://your-domain`. One GitHub Actions workflow keeps the
manifest in step with GitHub and tests, builds and verifies the site, then
commits the build to a `deploy` branch that Cloudflare Pages pulls through its
own GitHub app, so CI holds no Cloudflare credentials. Plain HTML, CSS and Python, no
framework. It is the source of [skillsmith.tech](https://skillsmith.tech/), formerly skills.caffeinity.com.

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

CI holds no Cloudflare credentials; Cloudflare pulls. Every hour, and on every
push to `main`, `.github/workflows/publish.yml` runs `sync.py`, which brings
`site/skills.json` in line with GitHub (new skill repos, moved repo HEADs,
renames, removals), rebuilds the site, gates it with `check_dist.py` and
`verify.mjs`, commits the sync back to `main`, and commits the gated `dist/` to
the `deploy` branch (under `public/`, only when the build changed). The
Cloudflare Pages project is connected to that branch, so each push there goes
live in a few minutes. The job then waits for the live `version.json` to match
and verifies the live site; if it never matches it opens one "Deploy pending"
issue, and closes it once live matches. `.github/workflows/health.yml` runs tune-skill's regression check over
every published skill each night. `PROJECT.md` maps the whole ecosystem.

### Connecting Cloudflare Pages (once)

Cloudflare cannot attach Git to a project created by direct upload, so this is
a new Pages project that takes over the domain:

1. Merge to `main` and let `publish` run once, so the `deploy` branch exists.
2. Cloudflare dashboard → Workers & Pages → Create → Pages → **Connect to Git**.
   Authorize the Cloudflare GitHub app for `arm-pz/skills-site` only.
3. Production branch `deploy`; framework preset **None**; build command empty
   (or `exit 0`); build output directory `public`. No environment variables.
4. Settings → Builds → Branch control: **Preview branches: None**, so `main`
   and PR branches never build (they hold sources, not a site).
5. Once its `*.pages.dev` URL serves the hub, remove `skills.caffeinity.com`
   from the old `skills` project's Custom domains and add it to the new one.
6. Run `publish` again (Actions → publish → Run workflow); the "Deploy pending"
   issue closes when the live `version.json` matches.

### Manual fallback

If Cloudflare is not connected, or to redeploy by hand, deploy from your own
machine, or ask Claude Code to "deploy the skills site":

    npx wrangler login                     # once; an OAuth login kept on this machine
    git checkout main && git pull
    bash tools/agent-skills/deploy.sh      # --dry-run to build and gate only

`deploy.sh` refuses anything but a clean, current `main`, runs the same gates
as CI, deploys only when the build differs from the live `version.json`, then
proves the live site. No token is written to the repo; if you prefer a token to
`wrangler login`, export `CLOUDFLARE_API_TOKEN` in that shell only.

A deploy replaces the whole production artifact set, so `dist/` has to hold
every page, tarball and index you want live — not only the new ones. If `dist/`
holds a partial tree, the deploy deletes the rest of the site, and a request for
a removed path still answers HTTP 200 with the hub page instead of a 404.
Check which tree you are in before deploying: more than one local clone of this
repo exists, and the last one to upload is what the domain serves. With the
Git-connected project a manual upload is overwritten by the next `deploy` push.

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

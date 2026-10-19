# skills-site — a static hub for agent skills

The source of [skills.caffeinity.com](https://skills.caffeinity.com): one
single-file landing page per agent skill, plus a hub index, downloadable
archives and a machine-readable `/agent-skills/index.json` that installers can
resolve. No build step, no dependencies, no framework — plain HTML, CSS and
self-hosted fonts, deployed to Cloudflare Pages.

Fork it if you want a site like this for your own skills: every page is
self-contained, and the shared design tokens live in one `:root` block.

## Run locally

    python -m http.server 8080    # or just open index.html

## Deploy

Copy the public files into `dist/`, then:

    npx wrangler pages deploy dist --project-name <your-project>

A deploy replaces the whole production artifact set, so `dist/` has to hold
every page, tarball and index you want live — not only the new ones. If `dist/`
holds a partial tree, the deploy deletes the rest of the site, and a request for
a removed path still answers HTTP 200 with the hub page instead of a 404.
Check which tree you are in before deploying: more than one local clone of this
repo exists, and the last one to upload is what the domain serves.

## The skills it hosts

wordsmith · recruiter-lens · applicant-kit · topic-primer · do-better ·
keyword-guard · web-preflight · findable · crash-test ·
pre-ship-performance-audit · draft-skill · prompts-to-skill ·
prompts-to-skill-release · tune-skill — each page links to its source repo under
[arm-pz](https://github.com/arm-pz).

## Related

The skills themselves install with `npx skills add arm-pz/<repo>`; most of
them are bundled as Claude Code plugins in the
[caffeinity-skills marketplace](https://github.com/arm-pz/caffeinity-skills).

## License

MIT — see [LICENSE](LICENSE).

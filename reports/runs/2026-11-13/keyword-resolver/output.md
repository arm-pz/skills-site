I wrote `resolution.md` with who owns what and new titles, H1s and meta descriptions for all four pages. I didn't change the site. I couldn't read the live `<title>` and meta tags, so I haven't confirmed how much the pages overlap today. I had no Search Console data either, so ownership is by what each page is for, not by clicks.

The overlap comes from the shared "tune skill" wording, which all four pages use. Ownership:

- **`/tune-skill/`** owns "tune skill", "audit SKILL.md" and "SKILL.md validator". It is the actual tool.
- **`/tune-skill-mod/`** owns pre-push gating: blocking git push and releases until an edited SKILL.md passes the check. Its new title leads with that instead of "tune skill".
- **`/tune-and-polish/`** owns "fix the skill, then polish its listing copy". It stays clear of "tune skill" in title and H1.
- **`/tune-and-ship/`** owns "release a skill": fact-check, one release PR, verify it's live. It stays clear of "tune skill" in title and H1.

The biggest risk was `/tune-skill-mod/` against `/tune-skill/`. The mod's name is the owner's name plus "mod", so it would show up for the owner's searches. The two workflow pages also look alike, so I split them by outcome: polish is about listing copy, ship is about the release PR.

For each page the file has a recommended title, H1 and meta (titles ≤60 characters, metas ≤155), plus one or two alternates. It also has internal-link changes. The three non-owner pages should each link to `/tune-skill/`. The two workflow pages should link to each other with intent-routing anchors.

- **Current tags not verified.** Shell access was denied, and the fetch tool only returned page text. Before applying anything, check the live title, H1 and meta description on each page for "tune" and "skill".
- **Check ownership against Search Console.** Re-run it with page and query data after about four weeks.
- **URL slugs left alone.** They still contain "tune"; changing them would need redirects.
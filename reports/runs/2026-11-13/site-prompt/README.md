# site-prompt: real-world run, 2026-11-13

**Verdict: PARTIAL** (3/10). The run wrote site-prompt.md embedding three full files (index.html, styles.css, main.js) for an invented Leeds shop 'Tannery Row Cycles', but never built, served or tested the site, and the prompt states 'Checks already run: None'.

Target: a one-file build prompt for a local business website. Run headless in a clean project with only this skill installed (6 turns, 4 tool calls, 128 s, $0.48).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Write me the paste-and-build prompt for a website for an independent bike repair shop in Leeds (opening hours, services and prices, how to book). Save it as site-prompt.md.
```

## Rubric

- Narrows the topic to a concrete subject and derives the concept from it
- Builds and verifies the site in a scratch folder before writing the prompt
- Embeds every file verbatim with a pinned stack and the checks that actually ran
- Marks invented business details (prices, hours) as placeholders for the owner rather than facts

## Hard checks

- ✓ wrote site-prompt.md
- ✓ embeds file contents

## Met

- Narrows the topic to a concrete subject (independent Leeds bike workshop, Kirkstall) and derives a concept from it (the paper job tag as a tag-builder signature mechanic)
- Embeds all three files in full with a pinned stack (plain HTML/CSS/JS, no dependencies, Google Fonts named)
- Marks business details as illustrative: the page and footer label name, address, hours and prices as concept placeholders, and the phone/email use reserved or example values
- Honestly reports in both the prompt and the final message that nothing was verified

## Missed

- Did not build and verify the site in a scratch folder before writing the prompt: no scratch folder, no browser, no served page, no replay script run; only a read-only inspection Bash call was made and Bash was then denied
- No checks actually ran, so the prompt's 'checks that actually ran' section says 'None' and the 'Not verified' list covers page load, layout, behaviour, contrast, fonts and replay
- File contents were never round-tripped through the replay script, so verbatim embedding is unconfirmed
- The prices and hours are presented as fixed values with 'do not change' instructions rather than as owner-fill placeholders; they are only labelled illustrative in the page copy

## Defects to fix in the skill

- The skill has no fallback for when command execution is denied or unavailable (for example, asking the user to approve Bash or stopping before writing an unverified prompt); here it produced a full prompt with zero verification
- The prompt template tells the build agent 'Do not change the illustrative prices, hours, phone number or email', which conflicts with the goal of marking invented business details as owner placeholders
- The skill does not require a single early check that the build tooling (Bash, a browser) is usable before committing to writing the files

## What it did

1. `Skill: site-prompt`
1. `Bash: cd /tmp/run-site-prompt-q_i6vlg2/project/.claude/skills/site-prompt && ls -R . | head -50 && cat references/subject-brief.md references/stack-presets.md referen`
1. `Bash: sed -n 1,40p scripts/replay-prompt.mjs; node -v; which chromium chromium-browser google-chrome python3; ls ~/.cache/ms-playwright 2>/dev/null; npm ls -g --depth`
1. `Write: /tmp/run-site-prompt-q_i6vlg2/project/site-prompt.md`

## Files it wrote

Copied under `files/`:

- `site-prompt.md`

## Final output

I saved the prompt as `site-prompt.md` in the project folder, but I haven't tested any of it. The Bash tool was denied partway through, so I couldn't open the page or run the replay script that compares the prompt's file sections against the site. The prompt's "Checks already run" section says "None", and "Not verified" lists every check I skipped. The code may have bugs that a first browser load would catch.

- **Shop:** "Tannery Row Cycles", a made-up independent workshop in Kirkstall, Leeds. You didn't name a shop, so I invented one and labelled it a concept on the page. The name, address, hours and prices are all illustrative.
- **Placeholder contact details:** the phone number is in the UK range reserved for drama use (0113 496 0142), and the email is on `example.com`. Swap in your real details before using it.
- **Stack:** plain HTML, CSS and JS in three files (`index.html`, `styles.css`, `main.js`). There's no build step or dependencies, and the only external request is Google Fonts.
- **Opening hours:** an "open now / opens tomorrow at 08:00" line in the hero, worked out in Leeds time. It reads from the hours table, so that table is the only place to change them.
- **Services and prices:** the page is a "job tag" builder, like the paper tag a workshop writes for each bike. You pick a service package (£25 to £220) and extra jobs (puncture, hydraulic bleed, wheel true and others). A kraft-card tag beside the form adds up the labour price.
- **How to book:** a drop-off form that only accepts Tuesday to Saturday. It opens an email draft containing the job tag, with the phone number as a fallback, and there's a four-step "how booking works" section.

Run it through the site-prompt skill with Bash allowed if you want the build tested and replay-checked. Otherwise, open `index.html` in a browser before trusting it.

# site-prompt: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). The run wrote site-prompt.md, a Leeds bike shop prompt with a three-file site (index.html, styles.css, main.js) embedded in full except that main.js is cut off mid-line in the saved file, but it never built or ran the site and the prompt's own checks section says 'None'.

Target: a one-file build prompt for a local business website. Run headless in a clean project with only this skill installed (6 turns, 4 tool calls, 128 s, $0.4).
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

- Narrowed the broad topic to a concrete subject (Tannery Row Cycles, Kirkstall, Leeds) and derived a 'job tag' builder concept from it
- Embedded the file contents in the prompt with a pinned plain HTML/CSS/JS stack and no dependencies (hard checks: wrote site-prompt.md, embeds file contents)
- Labelled the invented name, address, phone, email, hours and prices as illustrative or concept details on the page and in the prompt, and said so in the final message

## Missed

- Did not build and verify the site in a scratch folder before writing the prompt; Bash was denied, nothing was opened or run, and the final output admits the code is untested
- The embedded files are not verbatim from a verified build, and main.js is truncated mid-statement ('e.preve') in the saved file, so the prompt's 'reproduce character for character' instruction cannot be satisfied
- The prompt lists no checks that actually ran (it states 'None'), so the requirement to embed the checks that ran is not met
- Prices and hours are labelled 'illustrative' rather than clearly marked as owner-to-confirm placeholders; they are written into the markup as concrete values the prompt forbids changing ('Do not change the illustrative prices, hours, phone number or email')

## Defects to fix in the skill

- The skill depends on a build-and-verify step with Bash but has no fallback when Bash is denied, so it still emits a full prompt with unverified code instead of stopping or marking the prompt as a draft
- Nothing in the skill guards against writing a truncated file; it should require a check that the last embedded file ends cleanly before finishing
- The skill's template tells the model to forbid changes to invented business details, which conflicts with marking them as placeholders for the owner to replace

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

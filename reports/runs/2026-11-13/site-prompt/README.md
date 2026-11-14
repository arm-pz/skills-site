# site-prompt: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). The run wrote site-prompt.md with a Leeds bike-shop concept ('Tannery Row Cycles') embedding three complete files (index.html, styles.css, main.js) in a plain HTML/CSS/JS stack, but it never built or ran the site in a scratch folder, so the prompt states 'Checks already run: None'.

Target: a one-file build prompt for a local business website. Run headless on the CLI default model in a clean project with only this skill installed (6 turns, 4 tool calls, 128 s, $0.56).
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

- Narrows the topic to a concrete subject (Leeds independent bike workshop) and derives a concept from it (the job-tag builder, kraft-paper workshop-counter world)
- Embeds every file verbatim (index.html, styles.css, main.js) with a pinned stack (plain HTML/CSS/JS, no dependencies, Barlow fonts via Google Fonts)
- Marks invented details (name, address, phone on the Ofcom drama range, example.com email, hours, prices) as illustrative concept-shop placeholders on the page and in the notes
- Honestly reports that nothing was verified instead of claiming checks that did not run; the final message says the same

## Missed

- Did not build and verify the site in a scratch folder before writing the prompt: Bash was denied, only an inspection command and a Write were made, and no browser, server or replay script ran
- The prompt lists no checks that actually ran ('Checks already run: None'), so the rubric's 'checks that actually ran' is not satisfied
- Placeholders are labelled 'illustrative' but are written as concrete values in the code (e.g. £60, 08:00–18:00) with an instruction 'Do not change the illustrative prices, hours, phone number or email', rather than flagged as items for the owner to fill in
- Did not stop and ask about, or work around, the denied Bash permission, for example by trying a different verification path

## Defects to fix in the skill

- The skill gives no fallback when execution is unavailable (for example, a clear stop-and-ask step rather than emitting an unverified prompt), so it can produce an unverified deliverable
- The template tells the build agent not to change prices, hours, phone number or email, which conflicts with treating them as owner placeholders; it should tell the owner what to replace
- The skill has no explicit guard that checks for a working verification environment (browser or node available) before it starts drafting

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

# changelog-guard-mod

Bundles the `changelog-guard` skill unchanged and adds a mod that holds `git tag <name>`,
`npm publish` and `gh release create` until the skill has been run since the last edit.

- Advisory: matches command text, so `echo "git tag x"` also matches and a rewritten command can slip past.
- Fails open (`.catch` on every hook); after 2 holds it lets the command through with a toast.
- `/changelog-guard-snooze off|on` snoozes it for the session.

## What it can touch
Hooks: `session.start`, `skill.prompt`, `tool.call` (Bash, Edit/Write), `command.run`.
`$` calls: `$.ui.toast`, `$.command.register`. No process, file, network, environment or model access.
It never approves anything or submits prompts. It reads (does not change) Bash command text and
Edit/Write events.

## Status: NOT VALIDATED
Hand-written without shell access. `claude plugin validate` and `claude plugin test` have not been run,
and the API was checked only against the skill-to-mod contract (2.1.306), not the installed version.

Run: `claude plugin validate mods/changelog-guard-mod && claude plugin test mods/changelog-guard-mod`,
then `claude --plugin-dir mods/changelog-guard-mod`.

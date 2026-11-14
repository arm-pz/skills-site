# changelog-guard-mod

Reminds Claude to run changelog-guard before tagging or publishing a release.

This plugin is a Claude Code **mod** (needs Claude Code 2.1.287 or later). It bundles the
`changelog-guard` skill, unchanged, in `skills/changelog-guard/`, and adds code that runs inside Claude Code
to trigger it at the right moment.

## What it does

- **Gate.** A Bash command that matches one of the ship patterns is held until the required skills (`changelog-guard`) have run since the last edit. Modes (set with `/plugin configure <plugin>@<marketplace>`): `ask`, `block`, `nudge`, `off`. After 2 holds it lets the command through, so a missing skill can never trap a session.
- **/changelog-guard-mod** shows the state; `/changelog-guard-mod off` snoozes it for the session and `/changelog-guard-mod on` resumes.
- It reads the text of commands and prompts, so it is a reminder, not a security control. It fails open.

## Try it

```
claude --plugin-dir ./changelog-guard-mod
```

Run `/plugin` and look for "1 mod active". To share it, list it in a marketplace and install
with `/plugin install changelog-guard-mod@<marketplace>`.

## Trust surface

Mods are not sandboxed: they run with your permissions inside Claude Code. This block is the
report from `claude plugin validate`, refreshed by `verify_mod.py --update-readme`. Read the
`calls:` line before you install.

<!-- trust:start -->
```text
hooks: ./register.js session.start, skill.prompt, tool.call{tool=Edit|Write|MultiEdit|NotebookEdit}, tool.call{tool=Bash}, command.run{command=changelog-guard-mod}
calls: ./register.js $.command.register, $.ui.ask, $.ui.status, $.ui.toast
```
<!-- trust:end -->

## Tests

```
claude plugin test ./changelog-guard-mod
```

## Licence

Choose one before publishing and add a LICENSE file or a `license` field in `plugin.json`.

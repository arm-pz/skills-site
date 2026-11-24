First release.

An always-on agent skill: when a tool, skill or doc misbehaves mid-task, the agent files a structured papercut and carries on.

- Fields: skill, tool, tried, expected, happened, fix (never "try again"), workaround, severity, error pattern.
- Repeats grouped by fingerprint in a local queue; with PAPERCUT_REPO set, a GitHub issue labelled papercut is opened or commented on.
- Secrets, emails and home paths masked; fields capped; no prompt text or file contents.
- scripts/papercut.py (file, list), Python 3.9+. 15 self-checks pass against a fake gh.

Install: npx skills add arm-pz/log-papercut --skill log-papercut
Not yet run always-on in a live agent.

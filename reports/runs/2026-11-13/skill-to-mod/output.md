**Verdict: yes, it should become a mod, as a HYBRID.** I haven't built anything yet, because Bash is denied in this session. I need it for the build, validation and tests.

**Why a mod fits**
- The skill describes one specific moment: right before tagging or publishing a release. A skill alone only helps if Claude happens to remember it at that moment.
- A thin mod can catch `git tag` and `npm publish` Bash calls and remind Claude to run `changelog-guard` first.
- The skill text stays as it is, and the mod only triggers it.

**What it could touch**

This is the planned design, not something I've built or checked.
- **Hooks:** one `tool.check` hook that matches Bash commands containing `git tag` or `npm publish`, and one `skill.prompt` hook that notes the skill was loaded.
- **API calls:** only `$.ui.*` and `$.command.register`. That covers a notice or hold message and a snooze command.
- **No access to:** files, processes, network, environment variables or model calls. The mod does not read `CHANGELOG.md` or run git itself. The bundled skill does that, using Claude's normal tools.
- **No approval power:** it never returns `allow` and never submits prompts as you.
- **Limits:** it is advisory and fails open. It holds a command a capped number of times and can be snoozed.
- **Matching is a reminder, not enforcement:** `echo "git tag"` would also match, and a rewritten command can slip past. For real enforcement, use permission rules.

**What I need from you**
- Allow Bash, or run these yourself: `claude --version` (2.1.287 or later), the scaffold script, then `verify_mod.py` (which runs `claude plugin validate` and `claude plugin test`). Then I'll create `mods/changelog-guard-mod` with the skill copied unchanged.
- Or I can hand-write the files with the Write tool. That would leave the validation and tests unrun, so I'd report them as unverified.

Which do you prefer?

---

`changelog-guard` is now a mod at `mods/changelog-guard-mod`, and it passes validation and tests. I didn't do the live dry run with `claude --plugin-dir` (`/plugin` should then show "1 mod active"), so I haven't seen how it feels in a real session.

**What I ran:** Claude Code 2.1.325. `claude plugin validate` passed, and `claude plugin test` ran 10 tests with all 10 passing. A diff confirmed the bundled skill is identical to `skills/changelog-guard`.

**What it does:** It's a HYBRID. When Claude is about to run a Bash command containing `git tag` or `npm publish`, the mod checks whether `changelog-guard` has been loaded since the last file edit. If not, it asks before the command runs (mode `ask`). It lets the command through after 2 holds, so it can't trap a session. The mode and the list of required skills can be changed with `/plugin configure`. The `/changelog-guard-mod` command is there as the snooze/control command.

**Exactly what it can touch** (from the verifier):
- **Hooks:**
  - `session.start`
  - `skill.prompt`
  - `tool.call` on Edit, Write, MultiEdit and NotebookEdit, which clears an earlier check
  - `tool.call` on Bash, which is the gate
  - `command.run` for `changelog-guard-mod`
- **API calls:** only `$.command.register`, `$.ui.ask`, `$.ui.status` and `$.ui.toast`.
- **No access to:** files, processes, network, environment variables or other sessions. The mod never reads `CHANGELOG.md` or runs git. The bundled skill does that through Claude's normal tools.
- **No approval power:** it never approves a command for you.

**Limits**
- Matching is a reminder, not enforcement: `echo "git tag"` also matches, and a rewritten command can slip past. For real enforcement, use permission rules.
- "Checked" means the skill was loaded, not that it succeeded.
- The verifier flags a missing LICENSE and icon, which only matter if you publish it.
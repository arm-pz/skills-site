**Should it become a mod?** Yes, as a HYBRID: keep the skill unchanged and add a thin mod that nudges Claude to run it at the right moment. I haven't built anything yet.

**Why a mod fits**
- The skill has a clear moment: "right before tagging or publishing a release". That means `git tag` and `npm publish`, which a hook can see.
- The skill is only a four-step checklist. It's easy to forget, and a reminder at that moment is the fix.
- The skill itself stays as the source of the instructions. The mod would only prompt Claude to load it.

**What it could touch**
- It would use only `$.ui.*` and `$.command.register`: a reminder shown before the tag or publish command, plus a snooze command.
- It would make no process, network, file, environment or model calls.
- It would never auto-approve anything or submit prompts for you.
- It would be advisory only: it fails open and caps how many times it holds a command. It matches command text, so `echo "git tag"` would also match and a rewritten command could slip past. If you need enforcement, use permission rules instead.
- That list is the design I'd build, not something I've verified yet.

**Why I stopped**
- Bash is denied in this session ("don't ask" mode), so I can't run `claude --version` or the checker.
- I also can't run the scaffold, `claude plugin validate` or `claude plugin test`.
- You asked for a mod that is validated and tested. I won't write `mods/changelog-guard-mod` and call it done without those runs.
- I also haven't read the reference files for the mod format.

**To continue, either:**
1. Allow Bash (or switch off "don't ask" mode) and I'll scaffold and verify it.
2. Tell me to write the files by hand with the file tools. They would be unvalidated and untested, and I'd label them that way.

One assumption I'd make: "shipping" means `git tag` and `npm publish`. Tell me if you also want `gh release create` included.

---

I wrote `mods/changelog-guard-mod`, but it is **not validated or tested**. Bash was still denied, so I couldn't run `claude plugin validate`, `claude plugin test` or the checker. The README says it is unvalidated.

**What I built**
- **Skill:** `skills/changelog-guard/SKILL.md` is a copy of the original. I wrote it with the file tools, so check that it is identical.
- **Trigger:** Claude is told to run the skill before a Bash command that matches `git tag <name>`, `npm publish` or `gh release create`. `git tag -l` and `git tag -d` are not held.
- **How it holds:** it denies the command with an instruction to run changelog-guard and retry.
  - The check counts as done once the skill has been loaded.
  - Any Edit or Write marks the check stale again.
- **Fail-open limits:** it lets the command through after 2 holds, and every hook has a `.catch` that passes the call through.
- **Snooze:** `/changelog-guard-snooze off` or `on` for the session.
- **Tests:** `tests/changelog-guard-mod.test.ts` has six cases:
  - hold
  - listing and unrelated commands pass
  - pass after the skill has loaded
  - stale after an edit
  - hold cap
  - snooze

**What it can touch**
- It registers the hooks `session.start`, `skill.prompt`, `tool.call` (Bash, plus Edit and Write) and `command.run`.
- Its only `$` calls are `$.ui.toast` and `$.command.register`.
- It makes no process, file, network, environment or model calls.
- It never approves anything or submits prompts for you.
- It reads your Bash command text and sees the tool name on Edit and Write calls. It changes nothing except its own in-memory flags.
- It matches command text, so `echo "git tag x"` also matches and a rewritten command can slip past. It is a reminder, not enforcement.

**Run this yourself:**
```
claude plugin validate mods/changelog-guard-mod
claude plugin test mods/changelog-guard-mod
claude --plugin-dir mods/changelog-guard-mod
```

I wrote against the contract in the skill-to-mod references (Claude Code 2.1.306), not your installed version. I also guessed that `e.args` is a string in `command.run` and that the plugin skill name ends in `:changelog-guard`. If validate or the tests fail, those are the first places to look. Once Bash is allowed, I can run all three and fix whatever fails.
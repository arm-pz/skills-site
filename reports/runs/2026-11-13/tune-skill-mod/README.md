# tune-skill-mod: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). The agent edited the SKILL.md description and the mod flagged the commit and tune-skill was invoked, but the commit failed (git identity unknown), nothing was pushed (remote still has only 8a00dfb), and the tune-skill validator never ran.

Target: a small skill repo with a local bare remote: edit SKILL.md, then push. Run headless in a clean project with only this skill installed (7 turns, 5 tool calls, 12 s, $0.08).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
In skills/invoice-namer/SKILL.md, add to the description that it also handles .png scans of invoices. Commit it and push to origin main. If anything flags the push, do what it says and tell me what happened. At the end, quote verbatim any message a mod or hook added after a command ran (or say there was none).
```

## Rubric

- The mod arms only because a SKILL.md was edited
- In nudge mode the push goes through and Claude is told tune-skill has not run since the edit
- Claude runs tune-skill (bundled in the mod) on the edited skill and reports what it found
- The final message matches what the remote actually has

## Hard checks

- ✓ the mod loaded in the session
- ✓ the push was flagged after the SKILL.md edit (nudge mode, quoted by Claude)
- ✓ tune-skill was then run

## Met

- The mod armed only after the SKILL.md was edited (hook message cites the edited file)
- Claude was told tune-skill had not run since the edit and quoted both hook messages verbatim
- Claude invoked tune-skill on the edited skill
- The final message matches the remote: it correctly says nothing was committed or pushed, consistent with the remote having only the init commit

## Missed

- Commit and push to origin main were not completed; commit failed with Author identity unknown and the agent stopped instead of setting a repo-local identity
- In nudge mode the push was supposed to go through; it never ran, so the push-flagging behavior was not actually exercised on a push
- tune-skill's check_skill.py was not run and no findings were reported; Bash was denied (don't-ask mode) and the agent only searched for the script
- Hook messages were quoted, but the second one ('ran before tune-skill had run since the last edit') followed the failed commit, not a push as the scenario intended

## Defects to fix in the skill

- The nudge fires on a failed or non-push Bash command (the commit) and the message is generic, so it does not distinguish a push from other commands
- tune-skill depends on Bash to run check_skill.py, with no fallback (e.g., manual review of the SKILL.md) when Bash is unavailable
- The hook tells the agent to run check_skill.py but gives no path, so the agent had to search the filesystem with find to locate it

## Ground truth

```
--- commits on the bare remote:
8a00dfb init
```

## What it did

1. `Read: /tmp/run-tune-skill-mod-4q7dbnxc/project/skills/invoice-namer/SKILL.md`
1. `Edit: /tmp/run-tune-skill-mod-4q7dbnxc/project/skills/invoice-namer/SKILL.md`
1. `Bash: git add skills/invoice-namer/SKILL.md && git commit -q -m "invoice-namer: mention .png scan support in description

Co-Authored-By: Claude Sonnet 5.5 <noreply@a`
1. `Skill: tune-skill-mod:tune-skill`
1. `Bash: find / -name check_skill.py -path "*tune-skill*" 2>/dev/null | head; ls skills`

## Final output

I've stopped here: the edit is made, but it isn't committed or pushed.

**What happened**
- I added "Also handles .png scans of invoices." to the description in `skills/invoice-namer/SKILL.md`.
- `git commit` failed with `Author identity unknown`. No git user name or email is configured, so nothing was committed and the push never ran.
- After that command, a hook told me to run tune-skill, or at least its `check_skill.py` validator, on the file before shipping. I loaded tune-skill, but its validator needs Bash. Bash is now denied because the session is in don't-ask mode, so I couldn't run it.

**What I need from you**
1. Say whether you'd like me to set a repo-local git identity, and give me the name and email to use. I won't make one up.
2. Allow Bash again so I can run `check_skill.py`, then commit and push.

**Hook messages added after commands ran** (verbatim):
- "tune-skill-mod: you changed /tmp/run-tune-skill-mod-4q7dbnxc/project/skills/invoice-namer/SKILL.md. Before shipping it, run tune-skill on it (its check_skill.py validator at least), and fix every FAIL."
- "tune-skill-mod: that ran before tune-skill had run since the last edit. Run it now."

The permission-denied text on my last Bash call came from the harness, not from a hook.

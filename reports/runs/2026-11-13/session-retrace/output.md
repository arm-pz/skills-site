I found the session, but I can't tell you what it decided about split payments or Stackwise. The transcript doesn't contain those answers, and the vault it built is no longer on disk.

**The session**
- **ID:** `claude:eda1adb5`, a Claude Code session.
- **Date:** 2026-11-13, around 18:21–18:22.
- **Workspace:** `/tmp/run-ship-second-brain-69r37__h/project`.
- **Evidence (your prompt):** "Build our team second brain in ./vault from the sources in this folder (issue-412.md, pr-431.md, call-2026-11-04.md). Then answer from the vault alone: 1) Are split payments handled? Since when? 2) Are overpayments handled? 3) Did we promise Stackwise anything about QuickBooks?"
- **Other matches:** it was the only match. The search also skipped one live session, probably this one.

**What the transcript shows**
- Claude built a markdown vault from the three source files, then had a fresh subagent answer your three questions from the vault alone.
- It also wrote a `gaps.md` listing what the test found missing.
- It did not run `check_vault.py`, because Bash was denied in don't-ask mode. So no raw-file snapshot was recorded.
- It checked every quote against its source by eye and marked 8 notes `verified`.
- The ninth note is marked `seen`: Sam's "probably in the next release". Engineering never confirmed it.

**What I couldn't recover**
- The transcript text I read doesn't include the answers to your three questions.
- The vault folder no longer exists. Its workspace directory is gone, and Bash is denied here, so I couldn't read the notes or `gaps.md`.

Two things could get the answers back. You could re-run the session's three source files through the vault build, or you could point me at a copy of the vault or the source files. I can also read more of the transcript with `show claude:eda1adb5 --turns 40`. That might surface the answers, which the 12-turn view didn't.
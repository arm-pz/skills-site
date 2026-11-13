# do-better: real-world run, 2026-11-13

**Verdict: FAIL** (0/10). judge returned no JSON

Target: a broken UK postcode validator (9 valid and 5 invalid fixed test cases). Run headless in a clean project with only this skill installed (18 turns, 41 tool calls, 57 s, $0.46).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
/do-better --quick  The answer in answer.md is wrong. Get me a correct is_uk_postcode(s) and save it to postcode.py.
```

## Rubric

- Runs the quick bracket (several agents with different strategies, attack/defend/judge) rather than a single rewrite
- Final function accepts all valid formats incl. lowercase, missing space, GIR 0AA, and rejects the invalid ones
- Saves the result to postcode.py and states its limits honestly

## Hard checks

- ✗ postcode.py passes all 14 fixed cases

## Missed

- You've hit your 5-hour limit · resets 5:40pm (UTC)

## Ground truth

```
[stderr]
Traceback (most recent call last):
  File "/home/user/skills-site/tools/skill-runs/truth_postcode.py", line 4, in <module>
    spec.loader.exec_module(m)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^
  File "<frozen importlib._bootstrap_external>", line 1023, in exec_module
  File "<frozen importlib._bootstrap_external>", line 1160, in get_code
  File "<frozen importlib._bootstrap_external>", line 1218, in get_data
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/run-do-better-hoo9lc45/project/postcode.py'
```

## What it did

1. `Bash: ls -a && cat answer.md && ls .claude/skills/do-better && python .claude/skills/do-better/bracket.py plan --quick`
1. `Bash: mkdir -p .dobetter && cat > .dobetter/task.md <<'EOF'
Write a Python function `is_uk_postcode(s)` that correctly validates UK postcodes, to be saved as /tmp/run`
1. `Write: /tmp/run-do-better-hoo9lc45/project/.dobetter/task.md`
1. `Write: /tmp/run-do-better-hoo9lc45/project/.dobetter/baseline.md`
1. `Bash: python .claude/skills/do-better/bracket.py init --quick --task-file .dobetter/task.md --baseline-file .dobetter/baseline.md`
1. `Bash: python .claude/skills/do-better/bracket.py next`
1. `Bash: python .claude/skills/do-better/bracket.py prompts spawn`
1. `Agent: do-better a001.spawn`
1. `Agent: do-better a002.spawn`
1. `Agent: do-better a003.spawn`
1. `Agent: do-better a004.spawn`
1. `Read: /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/prompts/r0/a001.spawn.md`
1. `Agent: do-better a005.spawn`
1. `Read: /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/prompts/r0/a003.spawn.md`
1. `Read: /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/baseline.md`
1. `Agent: do-better a006.spawn`
1. `Read: /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/prompts/r0/a004.spawn.md`
1. `Read: /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/prompts/r0/a002.spawn.md`
1. `Agent: do-better a007.spawn`
1. `Read: /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/prompts/r0/a005.spawn.md`
1. `Agent: do-better a008.spawn`
1. `Read: /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/prompts/r0/a006.spawn.md`
1. `Read: /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/baseline.md`
1. `Agent: do-better a009.spawn`
1. `Read: /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/prompts/r0/a007.spawn.md`
1. `Read: /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/baseline.md`
1. `Agent: do-better a010.spawn`
1. `Read: /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/baseline.md`
1. `Read: /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/prompts/r0/a009.spawn.md`
1. `Read: /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/baseline.md`
1. `Read: /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/baseline.md`
1. `Read: /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/prompts/r0/a008.spawn.md`
1. `Read: /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/baseline.md`
1. `Read: /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/baseline.md`
1. `Bash: mkdir -p /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/scratch/a001 && cd /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113`
1. `Bash: mkdir -p /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/scratch/a004 && cd /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113`
1. `Bash: mkdir -p /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/scratch/a003 && cd /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113`
1. `Bash: mkdir -p /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/scratch/a005 && cd /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113`
1. `Bash: mkdir -p /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/scratch/a007 && cd /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113`
1. `Bash: mkdir -p /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/{r0,scratch/a002} && cd /tmp/run-do-better-hoo9lc45/project/.dobetter/run-202`
1. `Write: /tmp/run-do-better-hoo9lc45/project/.dobetter/run-20261113-172148-s131396/r0/a001.md`

## Files it wrote

Copied under `files/`:

- `.dobetter/LATEST`
- `.dobetter/baseline.md`
- `.dobetter/run-20261113-172148-s131396/baseline.md`
- `.dobetter/run-20261113-172148-s131396/dobetter.json`
- `.dobetter/run-20261113-172148-s131396/prompts/r0/a001.spawn.md`
- `.dobetter/run-20261113-172148-s131396/prompts/r0/a002.spawn.md`
- `.dobetter/run-20261113-172148-s131396/prompts/r0/a003.spawn.md`
- `.dobetter/run-20261113-172148-s131396/prompts/r0/a004.spawn.md`
- `.dobetter/run-20261113-172148-s131396/prompts/r0/a005.spawn.md`
- `.dobetter/run-20261113-172148-s131396/prompts/r0/a006.spawn.md`
- `.dobetter/run-20261113-172148-s131396/prompts/r0/a007.spawn.md`
- `.dobetter/run-20261113-172148-s131396/prompts/r0/a008.spawn.md`
- `.dobetter/run-20261113-172148-s131396/prompts/r0/a009.spawn.md`
- `.dobetter/run-20261113-172148-s131396/prompts/r0/a010.spawn.md`
- `.dobetter/run-20261113-172148-s131396/prompts/r0/a011.spawn.md`
- `.dobetter/run-20261113-172148-s131396/prompts/r0/a012.spawn.md`
- `.dobetter/run-20261113-172148-s131396/prompts/r0/a013.spawn.md`
- `.dobetter/run-20261113-172148-s131396/prompts/r0/a014.spawn.md`
- `.dobetter/run-20261113-172148-s131396/prompts/r0/a015.spawn.md`
- `.dobetter/run-20261113-172148-s131396/prompts/r0/a016.spawn.md`
- `.dobetter/run-20261113-172148-s131396/r0/a001.md`
- `.dobetter/run-20261113-172148-s131396/rubric.md`
- `.dobetter/run-20261113-172148-s131396/task.md`
- `.dobetter/task.md`

## Final output

You've hit your 5-hour limit · resets 5:40pm (UTC)

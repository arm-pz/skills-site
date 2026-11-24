"""Self-check for papercut.py: python -I tests/test_papercut.py. Uses a fake `gh`; files nothing real."""
import json
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "skills" / "log-papercut" / "scripts" / "papercut.py"
failures = []


def expect(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + ("" if cond else f"  {detail}"))
    if not cond:
        failures.append(name)


FAKE_GH = r'''#!/usr/bin/env python3
import json, os, sys
log = os.environ["GH_LOG"]
with open(log, "a") as f:
    f.write(json.dumps(sys.argv[1:]) + "\n")
args = sys.argv[1:]
state = os.environ.get("GH_STATE", "")
if args[:2] == ["issue", "list"]:
    if "--search" in args:
        print(json.dumps([{"number": 7, "url": "https://github.com/o/r/issues/7"}] if state == "exists" else []))
    else:
        print(json.dumps([{"number": 7, "url": "u7", "state": "OPEN", "body": "x\n```json\n" + json.dumps(
            {"fingerprint": "abc123abc123", "skill": "deploy", "tool": "api", "happened": "remote one",
             "workaround": "use ms"}) + "\n```"}]))
elif args[:2] == ["issue", "create"]:
    if state == "nolabel" and not os.path.exists(log + ".labelled"):
        print("could not add label: 'papercut' not found", file=sys.stderr); sys.exit(1)
    print("https://github.com/o/r/issues/8")
elif args[:2] == ["label", "create"]:
    open(log + ".labelled", "w").close()
'''

with tempfile.TemporaryDirectory() as tmp:
    t = Path(tmp)
    bindir = t / "bin"; bindir.mkdir()
    gh = bindir / "gh"; gh.write_text(FAKE_GH); gh.chmod(gh.stat().st_mode | stat.S_IEXEC)
    q = t / "queue.jsonl"
    base_env = {**os.environ, "PATH": f"{bindir}:{os.environ['PATH']}", "GH_LOG": str(t / "gh.log"),
                "PAPERCUT_QUEUE": str(q), "HOME": str(t)}
    base_env.pop("PAPERCUT_REPO", None)

    def run(*args, **env):
        p = subprocess.run([sys.executable, "-I", str(SCRIPT), *args], capture_output=True, text=True,
                           env={**base_env, **env})
        return p.returncode, p.stdout, p.stderr

    FILE = ["file", "--skill", "deploy", "--tool", "deploy-api", "--tried", "deploy --at 1700000000",
            "--expected", "deploy at that time", "--happened", "API rejected time 1700000000 in /home/alice/x.log",
            "--fix", "skill step 3: pass epoch milliseconds, not seconds",
            "--error-pattern", "rejected time", "--agent", "claude-code", "--session", "s1"]

    code, out, err = run(*FILE)
    rec = json.loads(q.read_text().splitlines()[0])
    expect("filed to local queue", code == 0 and "filed" in out and rec["count"] == 1, out + err)
    expect("home path masked", "alice" not in q.read_text() and "~" in rec["happened"], rec["happened"])
    expect("no gh call without a repo", not (t / "gh.log").exists())

    FILE2 = [a.replace("1700000000 in /home/alice/x.log", "1712345678 in /home/bob/y.log") for a in FILE]
    code, out, _ = run(*FILE2)
    lines = q.read_text().splitlines()
    expect("same failure with other numbers and paths groups", len(lines) == 1 and json.loads(lines[0])["count"] == 2
           and "seen again" in out, lines)

    code, out, err = run(*[a if a != "skill step 3: pass epoch milliseconds, not seconds" else "Try again" for a in FILE])
    expect("'try again' refused", code == 2 and "not a fix" in err, err)
    code, out, err = run(*FILE[:-6], "--severity", "huge")
    expect("bad severity refused", code == 2, err)
    code, out, err = run(*[a if a != "rejected time" else "(" for a in FILE])
    expect("bad error pattern refused", code == 2 and "regex" in err, err)

    secret = [a if a != "deploy --at 1700000000" else "curl -H 'token: ghp_abcdefghijklmnopqrstuvwxyz12' x" for a in FILE]
    secret[secret.index("--happened") + 1] = "a different failure entirely"
    run(*secret)
    expect("token masked", "ghp_abc" not in q.read_text())

    # GitHub: new issue
    code, out, err = run(*FILE, "--repo", "o/r")
    calls = [json.loads(l) for l in (t / "gh.log").read_text().splitlines()]
    expect("new fingerprint on GitHub creates an issue", calls[-1][:2] == ["issue", "create"]
           and "papercut" in calls[-1] and "filed https://github.com/o/r/issues/8" in out, out + err)
    body = calls[-1][calls[-1].index("--body") + 1]
    expect("issue body carries the JSON record and marker", "```json" in body and "<!-- papercut:" in body)

    # GitHub: existing open issue gets a comment
    (t / "gh.log").unlink()
    code, out, _ = run(*FILE, GH_STATE="exists", PAPERCUT_REPO="o/r")
    calls = [json.loads(l) for l in (t / "gh.log").read_text().splitlines()]
    expect("repeat comments on the open issue", calls[-1][:2] == ["issue", "comment"] and "commented on" in out, calls)

    # GitHub: missing label is created once
    (t / "gh.log").unlink()
    code, out, _ = run(*FILE, "--repo", "o/r", GH_STATE="nolabel")
    calls = [json.loads(l)[:2] for l in (t / "gh.log").read_text().splitlines()]
    expect("missing label created then issue filed", ["label", "create"] in calls and "filed" in out, calls)

    # list: local + GitHub merged, filters
    code, out, err = run("list", "--skill", "deploy", "--repo", "o/r")
    rows = [json.loads(l) for l in out.splitlines()]
    expect("list merges queue and GitHub", {r["fingerprint"] for r in rows} >= {"abc123abc123"} and len(rows) >= 2, rows)
    code, out, _ = run("list", "--search", "different failure")
    expect("list search", len(out.splitlines()) == 1, out)
    expect("empty workaround stored as null", '"workaround": ""' not in q.read_text())

print(f"\n{'FAILED: ' + ', '.join(failures) if failures else 'all passed'}")
sys.exit(1 if failures else 0)

"""Real-world skill runs: install one skill in a clean project, run a scenario through a headless
Claude Code session, grade the result, and write the evidence under reports/runs/<date>/<skill>/.

    python tools/skill-runs/run.py data-readout seo-polish     # run these scenarios
    python tools/skill-runs/run.py --all                       # every scenario in scenarios/
    python tools/skill-runs/run.py --list                      # scenarios and their last verdict

A scenario is tools/skill-runs/scenarios/<skill>.json:

    skill        catalog name being run (its page gets the result)
    install      catalog names installed as project skills (default: [skill])
    plugins      plugin dirs to load with --plugin-dir, as "<catalog name>" or "<repo>:<path>"
    allow, undeny  extra allowed tools; deny rules lifted (only for local stand-ins: a bare repo, a fake CLI)
    path_prepend project folder put first on PATH (fake deploy CLIs live there)
    teardown     shell run after the session (stops a local server the setup started)
    seed_sessions  give the run the session files of earlier runs (for skills that read history)
    fixtures     folder under tools/skill-runs/fixtures/ copied into the project
    setup        shell run in the project before the session (e.g. git init, a local server)
    target       what the run is on, in the words the site shows
    prompt       first message; followups: later messages in the same session
    max_turns, budget_usd, timeout_s
    checks       hard checks: {"desc", "re" | "file" | "cmd", "in": "output"|"transcript"|"file:<p>", "expect"}
    ground_truth shell whose stdout is given to the judge as the facts (Playwright scripts live here)
    rubric       what a good run does; the judge grades PASS, PARTIAL or FAIL against it

Each run gets its own HOME holding only the login, so a skill that reads session history sees the
runs it made and nothing else. Pushes, releases, deploys and outbound submissions are denied at the
tool layer; a scenario that needs a remote gets a local bare repo.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCEN = HERE / "scenarios"
FIX = HERE / "fixtures"
SRC = Path(os.environ.get("SKILL_SRC", HERE / ".src"))  # clones of the skill repos, never committed
POOL = Path(os.environ.get("SESSION_POOL", HERE / ".sessions"))  # each run's own session files, never committed
# No permission bypass: the session gets these tools and nothing else. A scenario can add more.
ALLOW = ["Read", "Write", "Edit", "Glob", "Grep", "Skill", "TodoWrite", "Agent", "Task", "WebSearch", "WebFetch",
         "Bash(python3:*)", "Bash(python:*)", "Bash(ls:*)", "Bash(cat:*)", "Bash(head:*)", "Bash(tail:*)",
         "Bash(wc:*)", "Bash(grep:*)", "Bash(find:*)", "Bash(sort:*)", "Bash(mkdir:*)", "Bash(git status:*)",
         "Bash(git diff:*)", "Bash(git log:*)", "Bash(git add:*)", "Bash(git commit:*)", "Bash(curl -sI:*)",
         "Bash(curl -s:*)", "Bash(node:*)", "Bash(npx:*)", "Bash(sed:*)", "Bash(awk:*)", "Bash(jq:*)",
         "Bash(cut:*)", "Bash(tr:*)", "Bash(uniq:*)", "Bash(echo:*)", "Bash(printf:*)", "Bash(cp:*)",
         "Bash(mv:*)", "Bash(touch:*)", "Bash(diff:*)", "Bash(cd:*)", "Bash(test:*)", "Bash(xargs:*)",
         "Bash(for:*)", "Bash(while:*)", "Bash(if:*)", "Bash(export:*)", "Bash(true:*)", "Bash(ls -a:*)",
         # read-only or project-local commands that real runs needed
         "Bash(git ls-files:*)", "Bash(git rev-parse:*)", "Bash(git show:*)", "Bash(git branch:*)",
         "Bash(git tag -l:*)", "Bash(git describe:*)", "Bash(git init:*)", "Bash(git checkout:*)",
         "Bash(claude --version:*)", "Bash(claude plugin validate:*)", "Bash(pwd:*)", "Bash(which:*)",
         "Bash(du:*)", "Bash(stat:*)", "Bash(file:*)", "Bash(basename:*)", "Bash(dirname:*)",
         "Bash(realpath:*)", "Bash(seq:*)", "Bash(date:*)", "Bash(sha256sum:*)", "Bash(zip:*)",
         "Bash(unzip:*)", "Bash(tar:*)", "Bash(rm:*)", "Bash(chmod:*)", "Bash(ln:*)"]
DENY = [
    "Bash(git push:*)", "Bash(gh:*)", "Bash(npm publish:*)", "Bash(npx wrangler:*)",
    "Bash(wrangler:*)", "Bash(curl -X POST:*)", "Bash(curl --request POST:*)",
]


LIMIT = re.compile(r"hit your [\w-]+ limit[^\n]*")


class UsageLimit(Exception):
    """The plan's usage limit ended the run; nothing is saved and later runs are skipped."""


# Told to every run session. The permission layer matches each Bash call against an allowlist, and a
# compound command (variables, functions, cd chains) cannot match, so it is denied whole. Saying so up
# front lets a skill do its real work instead of giving up after one denied call.
ENV_NOTE = ("This environment runs Bash with a fixed allowlist. Use one simple command per Bash call: "
            "no shell variables, functions, `cd dir && ...` chains, `;` lists or heredocs. Call scripts by "
            "path relative to the project (e.g. `node .claude/skills/<skill>/scripts/x.mjs`), write files "
            "with the Write tool, and if a call is denied, split it into simpler calls rather than stopping. "
            "Pushing, releasing, deploying and posting to outside services are not allowed here.")


def manifest():
    return {e["name"]: e for e in json.loads((ROOT / "site" / "skills.json").read_text())["skills"]}


def clone(repo):
    dest = SRC / repo.split("/")[1]
    if not dest.exists():
        SRC.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "-q", "--depth", "1", f"https://github.com/{repo}", str(dest)],
                       check=True)
    return dest


def source(spec, man):
    """'<catalog name>' or '<owner/repo>:<path>' -> local folder."""
    if ":" in spec:
        repo, path = spec.split(":", 1)
    else:
        e = man[spec]
        repo, path = e["repo"], e.get("path") or "."
    return clone(repo) / path


def _pw_module():
    r = subprocess.run(["node", "-e", "console.log(require.resolve('playwright'))"], cwd="/tmp",
                       capture_output=True, text=True)
    return r.stdout.strip() or "playwright"


PW_MODULE = _pw_module()
KEEP_ENV = ("PATH", "LANG", "LC_ALL", "TERM", "TZ", "ANTHROPIC_BASE_URL", "NODE_EXTRA_CA_CERTS",
            "SSL_CERT_FILE", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE", "HTTPS_PROXY", "HTTP_PROXY",
            "https_proxy", "http_proxy", "NO_PROXY", "no_proxy", "PLAYWRIGHT_BROWSERS_PATH")


def child_env(home):
    """Only what a plain local install would have: no remote-session settings, no identity, no tokens."""
    env = {k: v for k, v in os.environ.items() if k in KEEP_ENV}
    env["HOME"] = str(home)
    env.setdefault("CHROME_PATH", "/opt/pw-browsers/chromium")  # Lighthouse and Playwright use the preinstalled browser
    env.setdefault("PW_MODULE", PW_MODULE)  # ground-truth scripts import Playwright from here
    for k, v in (("GIT_AUTHOR_NAME", "skill-run"), ("GIT_COMMITTER_NAME", "skill-run"),
                 ("GIT_AUTHOR_EMAIL", "run@example.com"), ("GIT_COMMITTER_EMAIL", "run@example.com")):
        env[k] = v  # a neutral identity: the run's HOME has no git config
    env["SKILL_RUNS"] = str(HERE)  # setup and ground_truth reach helpers as $SKILL_RUNS/...
    return env


def claude(args, cwd, env, timeout):
    t = time.time()
    p = subprocess.run(["claude", *args], cwd=cwd, env=env, capture_output=True, text=True, stdin=subprocess.DEVNULL,
                       timeout=timeout)
    events = []
    for line in p.stdout.splitlines():
        try:
            events.append(json.loads(line))
        except ValueError:
            pass
    return events, p.stderr, time.time() - t


def final(events):
    res = [e for e in events if e.get("type") == "result"]
    return res[-1] if res else {}


def tool_log(events):
    out = []
    for e in events:
        if e.get("type") != "assistant":
            continue
        for c in e.get("message", {}).get("content", []):
            if c.get("type") == "tool_use":
                arg = c.get("input", {})
                short = arg.get("command") or arg.get("file_path") or arg.get("skill") or arg.get("url") \
                    or arg.get("pattern") or arg.get("description") or ""
                out.append(f"{c['name']}: {str(short)[:160]}")
    return out


def run_check(c, output, transcript, proj, written="", env=None):
    where = c.get("in", "any")  # any = the final message plus every file the run wrote
    if "cmd" in c:
        r = subprocess.run(c["cmd"], shell=True, cwd=proj, env=env, capture_output=True, text=True, timeout=300)
        ok = r.returncode == 0
        detail = (r.stdout + r.stderr).strip()[-400:]
    elif "file" in c:
        ok = (proj / c["file"]).exists()
        detail = c["file"]
    else:
        if where == "commands":  # only what the run executed, not text it read
            text = "\n".join(tool_log([json.loads(l) for l in transcript.splitlines() if l.strip()]))
        elif where == "any":
            text = output + "\n" + written
        elif where == "output":
            text = output
        elif where == "transcript":
            text = transcript
        else:
            f = proj / where.split(":", 1)[1]
            text = f.read_text(errors="replace") if f.exists() else ""
        m = re.search(c["re"], text, re.I | re.M)
        ok = bool(m)
        detail = m.group(0)[:160] if m else ""
    ok = ok if c.get("expect", True) else not ok
    return {"desc": c["desc"], "ok": ok, "detail": detail}


JUDGE = """You grade one real run of an agent skill. Be strict and literal: grade what the transcript
shows was done, not what the output claims. Return ONLY a JSON object:
{"verdict": "PASS"|"PARTIAL"|"FAIL", "score": 0-10, "summary": "<one sentence a stranger can read,
no hype, states what was found or produced with numbers where the run has them>",
"met": ["rubric item met", ...], "missed": ["rubric item missed, with what happened", ...],
"skill_defects": ["a defect in the SKILL itself (instructions, triggering, missing step) that a
tune would fix; empty if the failures were the environment's"]}

PASS = every rubric item met and nothing invented. PARTIAL = useful but at least one item missed.
FAIL = the skill did not do its job, invented facts, or did something it was told not to.
"""


def files_text(folder, names, limit=30000):
    """The text files a run wrote, so the judge grades the work and not the run's description of it."""
    out, used = [], 0
    for rel in names:
        f = Path(folder) / rel
        if not f.is_file() or f.stat().st_size > 200_000:
            continue
        try:
            body = f.read_text()
        except UnicodeDecodeError:
            continue
        if len(body) > limit - used:
            body = body[: max(0, limit - used)] + "\n[... cut here by the harness, not by the run; the saved file is complete]"
        used += len(body)
        out.append(f"### {rel}\n{body}")
        if used >= limit:
            break
    return "\n\n".join(out)


def by_run_first(events, names):
    """Files the run wrote with Write/Edit first, so files a setup step cloned cannot crowd them out of the judge."""
    touched = set()
    for e in events:
        for c in (e.get("message", {}).get("content", []) if e.get("type") == "assistant" else []):
            if c.get("type") == "tool_use" and c.get("name") in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
                touched.add(str(c.get("input", {}).get("file_path", "")))
    hit = lambda rel: any(t.endswith("/" + rel) for t in touched)
    return [n for n in names if hit(n)] + [n for n in names if not hit(n)]


def judge(scn, output, tools, checks, truth, env, proj, written=""):
    body = (f"{JUDGE}\n## Scenario\nSkill: {scn['skill']}\nTarget: {scn['target']}\n\nPrompt:\n{scn['prompt']}\n"
            + "".join(f"\nFollow-up:\n{f}\n" for f in scn.get("followups", []))
            + "\n## Rubric\n" + "\n".join(f"- {r}" for r in scn["rubric"])
            + (f"\n\n## Ground truth (measured independently of the run)\n{truth[:12000]}" if truth else "")
            + "\n\n## Hard checks\n" + "\n".join(f"- {'ok' if c['ok'] else 'FAILED'}: {c['desc']}" for c in checks)
            + "\n\n## Tool calls made\n" + "\n".join(tools[:200])
            + (f"\n\n## Files the run wrote\n{written}" if written else "")
            + f"\n\n## Final output\n{output[-40000:]}\n")
    events, _, _ = claude(["-p", body, "--max-turns", "1", "--output-format", "stream-json", "--verbose",
                           *(["--model", MODEL] if MODEL else []),
                           "--tools", ""], proj, env, 600)
    text = final(events).get("result", "")
    m = re.search(r"\{.*\}", text, re.S)
    try:
        return json.loads(m.group(0)), final(events).get("total_cost_usd", 0)
    except Exception:
        return {"verdict": "FAIL", "score": 0, "summary": "judge returned no JSON", "met": [],
                "missed": [text[:500]], "skill_defects": []}, 0


MODEL = None  # --model: the model the skill sessions and the judge run on (default: the CLI's)


def run(name, man, day):
    scn = json.loads((SCEN / f"{name}.json").read_text())
    out_dir = ROOT / "reports" / "runs" / day / name
    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f"run-{name}-") as tmp:
        tmp = Path(tmp)
        home, proj = tmp / "home", tmp / "project"
        (home / ".claude").mkdir(parents=True)
        shutil.copy(Path.home() / ".claude" / ".credentials.json", home / ".claude")
        if scn.get("seed_sessions") and POOL.exists():  # earlier runs' real history, for skills that read it
            shutil.copytree(POOL, home / ".claude" / "projects", dirs_exist_ok=True)
        proj.mkdir()
        if scn.get("fixtures"):
            shutil.copytree(FIX / scn["fixtures"], proj, dirs_exist_ok=True)
        for s in scn.get("install", [scn["skill"]]):
            shutil.copytree(source(s, man), proj / ".claude" / "skills" / s.split("/")[-1].split(":")[-1],
                            ignore=shutil.ignore_patterns(".git"))
        env = child_env(home)
        if scn.get("path_prepend"):  # local stand-ins, e.g. a fake `wrangler` that only writes a log
            env["PATH"] = f"{proj / scn['path_prepend']}:{env['PATH']}"
        if scn.get("setup"):
            subprocess.run(scn["setup"], shell=True, cwd=proj, env=env, check=True, timeout=600)
        args = ["--output-format", "stream-json", "--verbose", "--max-turns", str(scn.get("max_turns", 60)),
                "--permission-mode", "dontAsk", "--allowedTools", *ALLOW, *scn.get("allow", []),
                "--max-budget-usd", str(scn.get("budget_usd", 5)), *(["--model", MODEL] if MODEL else []),
                "--append-system-prompt", ENV_NOTE,
                "--disallowedTools", *[d for d in DENY if d not in scn.get("undeny", [])]]
        for p in scn.get("plugins", []):
            args += ["--plugin-dir", str(source(p, man))]
        timeout = scn.get("timeout_s", 1800)
        try:
            events, err, secs = claude(["-p", scn["prompt"], *args], proj, env, timeout)
        except subprocess.TimeoutExpired:
            events, err, secs = [], f"timed out after {timeout} s", timeout
        sid = final(events).get("session_id")
        for f in scn.get("followups", []):
            more, err2, s2 = claude(["-p", f, "--resume", sid, *args], proj, env, timeout)
            events += more
            err += err2
            secs += s2
            sid = final(more).get("session_id", sid)
        results = [e for e in events if e.get("type") == "result"]
        output = "\n\n---\n\n".join(r.get("result", "") for r in results)
        if LIMIT.search(output):
            raise UsageLimit(LIMIT.search(output).group(0))
        cost = sum(r.get("total_cost_usd", 0) for r in results)
        turns = sum(r.get("num_turns", 0) for r in results)
        transcript = "\n".join(json.dumps(e) for e in events)
        tools = tool_log(events)
        truth = ""
        if scn.get("ground_truth"):
            g = subprocess.run(scn["ground_truth"], shell=True, cwd=proj, env=env, capture_output=True,
                               text=True, timeout=600)
            truth = g.stdout + (f"\n[stderr]\n{g.stderr[-2000:]}" if g.returncode else "")
        if scn.get("teardown"):
            subprocess.run(scn["teardown"], shell=True, cwd=proj, env=env, timeout=60)
        made = by_run_first(events, sorted(str(p.relative_to(proj)) for p in proj.rglob("*")
                      if p.is_file() and ".claude" not in p.parts and ".git" not in p.parts
                      and not (FIX / scn.get("fixtures", "\0") / p.relative_to(proj)).exists()))
        if not scn.get("seed_sessions"):
            for f in (home / ".claude" / "projects").rglob("*.jsonl"):
                dest = POOL / f.relative_to(home / ".claude" / "projects")
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(f, dest)
        written = files_text(proj, made, limit=400_000)
        checks = [run_check(c, output, transcript, proj, written, env) for c in scn.get("checks", [])]
        verdict, jcost = judge(scn, output, tools, checks, truth, env, proj, files_text(proj, made, limit=90000))
        if LIMIT.search(json.dumps(verdict)):
            raise UsageLimit("the judge hit the usage limit")
        cap(verdict, checks)
        art = out_dir / "files"
        for rel in made[:40]:
            src = proj / rel
            if src.stat().st_size < 400_000:
                (art / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(src, art / rel)
    record = {"skill": name, "date": day, "target": scn["target"], "verdict": verdict["verdict"],
              "score": verdict.get("score"), "summary": verdict.get("summary", ""),
              "checks": checks, "met": verdict.get("met", []), "missed": verdict.get("missed", []),
              "skill_defects": verdict.get("skill_defects", []), "cost_usd": round(cost + jcost, 2),
              "model": MODEL or "cli default", "turns": turns, "seconds": round(secs), "tool_calls": len(tools), "files": made[:40],
              "error": err.strip()[-1500:] if not results else ""}
    (out_dir / "truth.txt").write_text(truth)
    (out_dir / "output.md").write_text(redact(output))
    (out_dir / "verdict.json").write_text(json.dumps(record, indent=2) + "\n")
    (out_dir / "transcript.jsonl").write_text(redact_jsonl(transcript) + "\n")
    (out_dir / "README.md").write_text(redact(report(scn, record, output, tools, truth)))
    return record


def cap(verdict, checks):
    if not all(c["ok"] for c in checks) and verdict.get("verdict") == "PASS":
        verdict["verdict"] = "PARTIAL"
        verdict.setdefault("missed", []).append("a hard check failed")


def rejudge(name, day):
    """Grade a saved run again (after a judge or scenario fix) without running the skill again."""
    scn = json.loads((SCEN / f"{name}.json").read_text())
    out_dir = ROOT / "reports" / "runs" / day / name
    rec = json.loads((out_dir / "verdict.json").read_text())
    events = [json.loads(l) for l in (out_dir / "transcript.jsonl").read_text().splitlines() if l.strip()]
    results = [e for e in events if e.get("type") == "result"]
    output = "\n\n---\n\n".join(r.get("result", "") for r in results)
    tools = tool_log(events)
    truth = (out_dir / "truth.txt").read_text() if (out_dir / "truth.txt").exists() else ""
    rec["files"] = by_run_first(events, rec["files"])
    written = files_text(out_dir / "files", rec["files"], limit=400_000)
    transcript = (out_dir / "transcript.jsonl").read_text()
    old = {c["desc"]: c for c in rec["checks"]}
    rec["checks"] = [old.get(c["desc"]) if ("cmd" in c or "file" in c) and c["desc"] in old
                     else run_check(c, output, transcript, out_dir / "files", written)
                     for c in scn.get("checks", [])]
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        (home / ".claude").mkdir()
        shutil.copy(Path.home() / ".claude" / ".credentials.json", home / ".claude")
        verdict, jcost = judge(scn, output, tools, rec["checks"], truth, child_env(home), Path(tmp),
                               files_text(out_dir / "files", rec["files"], limit=90000))
    if LIMIT.search(json.dumps(verdict)):
        raise UsageLimit("the judge hit the usage limit")
    cap(verdict, rec["checks"])
    rec.update(verdict=verdict["verdict"], score=verdict.get("score"), summary=verdict.get("summary", ""),
               met=verdict.get("met", []), missed=verdict.get("missed", []),
               skill_defects=verdict.get("skill_defects", []), cost_usd=round(rec["cost_usd"] + jcost, 2),
               judge_model=MODEL or "cli default")
    (out_dir / "output.md").write_text(redact(output))
    (out_dir / "verdict.json").write_text(json.dumps(rec, indent=2) + "\n")
    (out_dir / "README.md").write_text(redact(report(scn, rec, output, tools, truth)))
    return rec


def redact_jsonl(text):
    """Redact inside each event's strings, so the file stays valid JSON."""
    def walk(v):
        if isinstance(v, str):
            return redact(v)
        if isinstance(v, list):
            return [walk(x) for x in v]
        if isinstance(v, dict):
            return {k: walk(x) for k, x in v.items()}
        return v
    return "\n".join(json.dumps(walk(json.loads(l))) for l in text.splitlines() if l.strip())


def redact(text):
    # Fixture addresses (example.com, *.example) are part of the evidence; anything else is not published.
    text = re.sub(r"[A-Za-z0-9._%+-]+@(?!noreply|example\.com|[A-Za-z0-9.-]+\.example\b)[A-Za-z0-9.-]+\.[a-z]{2,}",
                  "<email>", text)
    text = re.sub(r"(sk-ant-[\w-]{8})[\w-]+", r"\1…", text)
    return text.replace(str(Path.home()), "~")


def report(scn, r, output, tools, truth):
    mark = {"PASS": "PASS", "PARTIAL": "PARTIAL", "FAIL": "FAIL"}.get(r["verdict"], r["verdict"])
    lines = [f"# {scn['skill']}: real-world run, {r['date']}", "",
             f"**Verdict: {mark}** ({r['score']}/10). {r['summary']}", "",
             f"Target: {scn['target']}. Run headless on {r.get('model', 'the CLI default model')} in a clean project with only this skill installed"
             f" ({r['turns']} turns, {r['tool_calls']} tool calls, {r['seconds']} s, ${r['cost_usd']}).",
             "Pushes, releases, deploys and outbound submissions were denied for the run.", "",
             "## Prompt", "", "```", scn["prompt"], "```"]
    for f in scn.get("followups", []):
        lines += ["", "Follow-up:", "", "```", f, "```"]
    lines += ["", "## Rubric", ""] + [f"- {x}" for x in scn["rubric"]]
    lines += ["", "## Hard checks", ""] + [f"- {'✓' if c['ok'] else '✗'} {c['desc']}" for c in r["checks"]]
    if r["met"]:
        lines += ["", "## Met", ""] + [f"- {x}" for x in r["met"]]
    if r["missed"]:
        lines += ["", "## Missed", ""] + [f"- {x}" for x in r["missed"]]
    if r["skill_defects"]:
        lines += ["", "## Defects to fix in the skill", ""] + [f"- {x}" for x in r["skill_defects"]]
    if truth:
        lines += ["", "## Ground truth", "", "```", truth.strip()[:6000], "```"]
    if r["error"]:
        lines += ["", "## Error", "", "```", r["error"], "```"]
    lines += ["", "## What it did", ""] + [f"1. `{t}`" for t in tools[:80]]
    if r["files"]:
        lines += ["", "## Files it wrote", "", "Copied under `files/`:", ""] + [f"- `{f}`" for f in r["files"]]
    lines += ["", "## Final output", "", output.strip() or "_(none)_", ""]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--date", default=date.today().isoformat())
    ap.add_argument("--rejudge", action="store_true", help="grade saved runs again; does not rerun the skill")
    ap.add_argument("--model", help="model for the skill sessions and the judge, e.g. sonnet")
    a = ap.parse_args(argv)
    global MODEL
    MODEL = a.model
    names = sorted(p.stem for p in SCEN.glob("*.json")) if (a.all or a.list) else a.names
    skipped = {p.stem for p in SCEN.glob("*.json") if json.loads(p.read_text()).get("skip")}
    if not a.list:
        for n in sorted(skipped & set(names)):
            print(f"{n:34} SKIP     {json.loads((SCEN / f'{n}.json').read_text())['skip']}")
        names = [n for n in names if n not in skipped]
    if a.list:
        for n in names:
            hits = sorted((ROOT / "reports" / "runs").glob(f"*/{n}/verdict.json"))
            v = json.loads(hits[-1].read_text()) if hits else {}
            print(f"{n:34} {v.get('date', '-'):11} {v.get('verdict', 'not run')}")
        return 0
    man = manifest()
    for n in names:
        try:
            r = rejudge(n, a.date) if a.rejudge else run(n, man, a.date)
        except UsageLimit as ex:
            print(f"{n:34} LIMIT    {ex}; stopping, nothing saved for this or later runs", flush=True)
            return 2
        except Exception as ex:  # one broken scenario must not stop the batch
            print(f"{n:34} ERROR    {type(ex).__name__}: {ex}", flush=True)
            continue
        print(f"{n:34} {r['verdict']:8} ${r['cost_usd']:<6} {r['summary']}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

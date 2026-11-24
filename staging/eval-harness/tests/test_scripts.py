"""Self-check for score.py and traces.py. Run: python -I tests/test_scripts.py"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "eval-harness" / "scripts"
FIX = Path(__file__).resolve().parent / "fixtures"
failures = []


def run(script, *args):
    p = subprocess.run([sys.executable, "-I", str(SCRIPTS / script), *map(str, args)],
                       capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def expect(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + ("" if cond else f"  {detail}"))
    if not cond:
        failures.append(name)


def write_cases(path, cases):
    path.write_text("\n".join(json.dumps(c) for c in cases) + "\n", encoding="utf-8")


with tempfile.TemporaryDirectory() as tmp:
    t = Path(tmp)
    run1, prev, run2 = t / "run1", t / "prev", t / "run2"
    for d in (run1, prev, run2):
        d.mkdir()
    cases = [
        {"id": "g1", "kind": "positive", "source": "run", "checks": [
            {"type": "contains", "value": "broken link", "ignore_case": True},
            {"type": "count", "value": r"^- ", "min": 2, "max": 3}]},
        {"id": "g2", "kind": "negative", "source": "run", "critical": True, "checks": [
            {"type": "regex", "value": r"(?i)no (new )?changes"}, {"type": "max_lines", "value": 2}]},
        {"id": "g3", "kind": "edge", "source": "invented", "checks": [
            {"type": "json", "path": "items.0.url", "equals": "https://a.test"},
            {"type": "json", "path": "count", "exists": True}]},
        {"id": "g4", "kind": "positive", "source": "run", "checks": [
            {"type": "not_contains", "value": "TODO"},
            {"type": "judge", "rubric": "Does every finding cite its source line?"}]},
    ]
    cf = t / "golden.jsonl"
    write_cases(cf, cases)
    (run1 / "g1.md").write_text("Report\n- Broken link on /a\n- slow page /b\n", encoding="utf-8")
    (run1 / "g2.txt").write_text("No new changes today.\n", encoding="utf-8")
    (run1 / "g3.json").write_text(json.dumps({"items": [{"url": "https://a.test"}], "count": 1}), encoding="utf-8")
    (run1 / "g4.md").write_text("- finding (line 4)\n", encoding="utf-8")

    code, out, _ = run("score.py", cf, run1, "--out", t / "sc")
    sc = json.loads((t / "sc.json").read_text())
    expect("judge check without verdict is pending, exit 2", code == 2 and sc["verdict"] == "pending", out)
    expect("pending lists the key", [p["key"] for p in sc["pending"]] == ["g4#1"], sc["pending"])

    (run1 / "judgments.json").write_text(json.dumps({"g4#1": {"pass": True, "why": "cites"}}))
    base = t / "baseline.json"
    code, out, err = run("score.py", cf, run1, "--baseline", base, "--save-baseline")
    expect("all pass, exit 0, baseline saved", code == 0 and base.exists(), out + err)

    # Regression: g1 now has one bullet; critical g2 fails too.
    for f in run1.iterdir():
        (run2 / f.name).write_text(f.read_text())
    (run2 / "g1.md").write_text("Report\n- broken link on /a\n", encoding="utf-8")
    code, out, _ = run("score.py", cf, run2, "--baseline", base, "--out", t / "sc2")
    sc2 = json.loads((t / "sc2.json").read_text())
    expect("regression exits 1", code == 1 and sc2["regressions"] == ["g1"], sc2["regressions"])
    expect("markdown names the failing check", "count: 1 matches" in out, out)
    code, out, err = run("score.py", cf, run2, "--baseline", base, "--save-baseline")
    expect("baseline not overwritten on regression", "refused" in err and json.loads(base.read_text())["passed"].count("g1") == 1, err)

    (run2 / "g2.txt").write_text("Found 3 changes\nmore\nmore\n", encoding="utf-8")
    code, out, _ = run("score.py", cf, run2, "--out", t / "sc3")
    sc3 = json.loads((t / "sc3.json").read_text())
    expect("critical failure listed", sc3["critical_failed"] == ["g2"] and code == 1, sc3["critical_failed"])

    # Missing output file is a failure, not a crash.
    (run2 / "g3.json").unlink()
    code, out, _ = run("score.py", cf, run2, "--out", t / "sc4")
    sc4 = json.loads((t / "sc4.json").read_text())
    g3 = [r for r in sc4["results"] if r["id"] == "g3"][0]
    expect("missing output fails the case", g3["status"] == "fail" and "no output" in g3["checks"][0]["detail"])

    # Invariants with match "*" and dedup against previous run.
    inv = t / "invariants.jsonl"
    write_cases(inv, [{"id": "inv-dedup", "kind": "regression", "source": "loop-schedule", "match": "*",
                       "checks": [{"type": "not_in_previous", "value": r"^- "}]}])
    (prev / "acme.md").write_text("- old item A\n- old item B\n", encoding="utf-8")
    (prev / "beta.md").write_text("- beta item\n", encoding="utf-8")
    reports = t / "reports"
    reports.mkdir()
    (reports / "acme.md").write_text("- new item C\n- old item A\n", encoding="utf-8")
    (reports / "beta.md").write_text("- beta new\n", encoding="utf-8")
    code, out, _ = run("score.py", inv, reports, "--previous", prev, "--out", t / "inv")
    si = json.loads((t / "inv.json").read_text())
    st = {r["id"]: r["status"] for r in si["results"]}
    expect("dedup flags the repeated item per file", st == {"inv-dedup:acme.md": "fail", "inv-dedup:beta.md": "pass"}, st)
    code, out, _ = run("score.py", inv, reports, "--out", t / "inv2")
    expect("dedup without --previous is pending", json.loads((t / "inv2.json").read_text())["verdict"] == "pending")

    # Bad cases file is exit 2 with a reason.
    bad = t / "bad.jsonl"
    bad.write_text('{"id": "x", "checks": []}\n{"id": "x", "kind": "weird", "checks": [{"type": "contains", "value": "a"}]}\nnot json\n')
    code, _, err = run("score.py", bad, run1)
    expect("unusable cases file exits 2 with reasons", code == 2 and "duplicate id" in err and "unknown kind" in err and "not JSON" in err, err)
    code, out, _ = run("score.py", cf, t / "nope")
    expect("missing run folder exits 2", code == 2)

    # Bad regex in a check is a failed check, not a crash.
    write_cases(t / "re.jsonl", [{"id": "g2", "kind": "edge", "source": "x", "checks": [{"type": "regex", "value": "("}]}])
    code, out, _ = run("score.py", t / "re.jsonl", run1)
    expect("bad regex reported", code == 1 and "bad regex" in out, out)

# traces.py
code, out, _ = run("traces.py", FIX / "session.jsonl")
tr = json.loads(out)
expect("trace: two calls in order", [c["name"] for c in tr["calls"]] == ["WebFetch", "Bash"], tr["calls"])
expect("trace: errors and denial counted", tr["tool_errors"] == 2 and tr["permission_denials"] == 1, tr)
expect("trace: end from result line", tr["end"] == "error_max_turns" and "ended_error_max_turns" in tr["flags"], tr["flags"])
expect("trace: final text kept", tr["final_text"].startswith("No changes found"), tr["final_text"])
expect("trace: secrets and emails masked", "abcd1234efgh5678" not in out and "ops@acme.com" not in out, out)
expect("trace: model read", tr.get("model") == "test-model", tr.get("model"))

with tempfile.TemporaryDirectory() as tmp:
    log = Path(tmp) / "run.log"
    log.write_text("start\nfetching\nERROR: upstream timed out\nwrote 0 rows\n", encoding="utf-8")
    code, out, _ = run("traces.py", log)
    tr = json.loads(out)
    expect("plain log: error lines found", tr["format"] == "plain" and tr["error_line_count"] == 1, tr)
    code, out, _ = run("traces.py", Path(tmp) / "empty-dir-nothing")
    expect("missing trace exits 2", code == 2)
    (Path(tmp) / "sessions").mkdir()
    (Path(tmp) / "sessions" / "a.jsonl").write_text((FIX / "session.jsonl").read_text())
    code, out, _ = run("traces.py", Path(tmp) / "sessions")
    expect("folder: newest session read", code == 0 and json.loads(out)["format"] == "jsonl")

print(f"\n{'FAILED: ' + ', '.join(failures) if failures else 'all passed'}")
sys.exit(1 if failures else 0)

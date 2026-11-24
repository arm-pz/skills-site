"""Self-check for the skill-eval-suite scripts. Run: python -I tests/test_scripts.py"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "skill-eval-suite" / "scripts"
FIX = Path(__file__).resolve().parent / "fixtures"
failures = []


def run(script, *args):
    p = subprocess.run([sys.executable, "-I", str(SCRIPTS / script), *map(str, args)],
                       capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def expect(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + ("" if cond else f"  {str(detail)[:400]}"))
    if not cond:
        failures.append(name)


def jsonl(path, rows):
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


def session(sid, skill, tools, final="Done.", errors=(), end="success", prompt="check the site", tokens=None):
    """A stream-json style trace: init, prompt, a Skill call, then tools in order, then a result."""
    ev = [{"type": "system", "subtype": "init", "model": "m", "session_id": sid},
          {"type": "user", "sessionId": sid, "timestamp": "2026-11-20T06:00:00Z",
           "message": {"role": "user", "content": prompt}}]
    calls = ([("Skill", {"skill": skill})] if skill else []) + [(t, {"command": t.lower()}) for t in tools]
    for i, (name, inp) in enumerate(calls):
        ev.append({"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": f"t{i}", "name": name, "input": inp}]}})
        err = name in errors
        ev.append({"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": f"t{i}", "is_error": err,
             "content": "HTTP 403 forbidden" if err else "ok"}]}})
    ev.append({"type": "assistant", "message": {"role": "assistant", "id": "m-final", "content": [{"type": "text", "text": final}],
               **({"usage": {"input_tokens": tokens // 2, "output_tokens": tokens // 4, "cache_read_input_tokens": tokens - tokens // 2 - tokens // 4}}
                  if tokens else {})}})
    ev.append({"type": "result", "subtype": end, "session_id": sid, "duration_ms": 1000 + 100 * len(calls)})
    return "\n".join(json.dumps(e) for e in ev) + "\n"


with tempfile.TemporaryDirectory() as tmp:
    t = Path(tmp)
    prev = t / "prev"; prev.mkdir()
    suite = [
        {"id": "g1", "tier": "golden", "intent": "must_do", "source": "fixture", "checks": [
            {"type": "contains", "value": "broken link", "ignore_case": True},
            {"type": "count", "value": r"^- ", "min": 2, "max": 3}]},
        {"id": "g2", "tier": "golden", "intent": "must_not", "source": "invented", "checks": [
            {"type": "json", "path": "items.0.url", "equals": "https://a.test"}]},
    ] + [
        {"id": f"r{i}", "tier": "real", "intent": "keep_working" if i > 6 else "must_do", "source": f"session s{i}",
         "checks": [{"type": "skill_used", "value": "seo-crawl"}, {"type": "order", "value": ["Skill", "Bash", "Write"]},
                    {"type": "tool_not_called", "value": "Bash:rm -rf"}, {"type": "max_tool_errors", "value": 0},
                    {"type": "finished"}, {"type": "regex", "value": "(?i)report"}]}
        for i in range(1, 9)
    ] + [
        {"id": "au1", "tier": "author", "intent": "must_not", "source": "rejected PR #12",
         "checks": [{"type": "judge", "rubric": "Would the reviewer's objection still apply?"}]},
        {"id": "au2", "tier": "author", "intent": "must_do", "source": "edited PR #15",
         "checks": [{"type": "judge", "rubric": "Is the commit message accurate?"}]},
    ]
    sf = t / "suite.jsonl"
    jsonl(sf, suite)

    code, out, _ = run("score.py", sf, "--validate")
    expect("validate prints mix and intents", code == 0 and "golden 2" in out and "real 8" in out
           and "must_do, must_not, keep_working" in out, out)
    jsonl(t / "nointent.jsonl", [dict(c, intent="must_do") for c in suite])
    code, out, _ = run("score.py", t / "nointent.jsonl", "--validate")
    expect("validate flags missing must_not and keep_working", "no must_not, keep_working case" in out, out)

    def fill(d, broken=(), fix_au2=False, tokens=900):
        d.mkdir(exist_ok=True)
        (d / "g1.md").write_text("Report\n- Broken link on /a\n- slow page /b\n", encoding="utf-8")
        (d / "g2.json").write_text(json.dumps({"items": [{"url": "https://a.test"}]}), encoding="utf-8")
        for i in range(1, 9):
            tools = ["Bash", "Write"] if f"r{i}" not in broken else ["Write"]
            (d / f"r{i}.trace.jsonl").write_text(session(f"s{i}", "seo-crawl", tools, final="Report: 2 issues", tokens=tokens))
        for k in ("au1", "au2"):
            (d / f"{k}.md").write_text("a change\n", encoding="utf-8")
        (d / "judgments.json").write_text(json.dumps({
            "au1#0": {"pass": True, "by": "author"}, "au2#0": {"pass": fix_au2, "by": "author"}}))
        return d

    def trials(name, k, **kw):
        ds = [fill(t / f"{name}{j}", **kw) for j in range(k)]
        return [ds[0]] + [x for d in ds[1:] for x in ("--repeat", d)]

    # Pending judge verdicts: exit 2.
    p0 = fill(t / "p0"); (p0 / "judgments.json").unlink()
    code, out, _ = run("score.py", sf, p0, "--out", t / "p0")
    expect("judge checks pending -> exit 2", code == 2 and json.loads((t / "p0.json").read_text())["pending"], out)

    # Agent verdict on an author case stays pending.
    (p0 / "judgments.json").write_text(json.dumps({"au1#0": {"pass": True, "by": "agent"}, "au2#0": {"pass": False, "by": "author"}}))
    run("score.py", sf, p0, "--out", t / "p0b")
    st = {r["id"]: r["state"] for r in json.loads((t / "p0b.json").read_text())["cases"]}
    expect("author tier needs the author's verdict", st["au1"] == "pending" and st["au2"] != "pending", st)

    # New cases need 3 trials.
    code, out, _ = run("score.py", sf, *trials("two", 2), "--out", t / "two")
    expect("new cases with 2 trials need more -> exit 2", code == 2 and len(json.loads((t / "two.json").read_text())["needs_trials"]) == 12, out)

    base = t / "baseline.json"
    code, out, err = run("score.py", sf, *trials("base", 3), "--baseline", base, "--save-baseline", "--out", t / "base")
    sb = json.loads((t / "base.json").read_text())
    expect("3 trials: scored, baseline saved per case", code == 0 and base.exists()
           and json.loads(base.read_text())["cases"]["r1"]["rate"] == 1.0 and abs(sb["pass_rate"] - 11 / 12) < 0.01, out + err)
    expect("resolution note: one case moves the rate", "one case moves the rate 8.3 points" in out, out)

    # A split case is flaky, counted in the noise band, kept.
    f = trials("flaky", 3); fill(t / "flaky2", broken=("r1",))
    code, out, _ = run("score.py", sf, *f, "--baseline", base, "--out", t / "fl")
    sf_ = json.loads((t / "fl.json").read_text())
    r1 = next(r for r in sf_["cases"] if r["id"] == "r1")
    expect("split trials -> flaky 2/3, noise band 1/12", r1["state"] == "flaky" and r1["passes"] == 2
           and abs(sf_["noise_band"] - 1 / 12) < 0.01, r1)
    expect("flaky case is not a flip", "r1" not in sf_["broke"], sf_["broke"])

    # Trade-off: fixed one, broke one.
    code, out, _ = run("score.py", sf, *trials("trade", 3, broken=("r2",), fix_au2=True), "--baseline", base, "--out", t / "tr")
    st = json.loads((t / "tr.json").read_text())
    expect("fixed and broke reported as a trade-off", st["fixed"] == ["au2"] and st["broke"] == ["r2"]
           and "a trade-off, not a win" in out and code == 0, out)

    # Clear loss once: reported, not blocked. Twice in a row: blocked.
    (t / "ab-log.jsonl").unlink()
    worse = dict(broken=("r2", "r3", "r4", "r5"))
    code1, out1, _ = run("score.py", sf, *trials("loss1", 3, **worse), "--baseline", base)
    code2, out2, _ = run("score.py", sf, *trials("loss2", 3, **worse), "--baseline", base)
    expect("first clear loss warns, exit 0", code1 == 0 and "blocks if the next comparison" in out1, out1)
    expect("second clear loss in a row blocks", code2 == 1 and "repeated clear loss" in out2, out2)

    # Golden case that passed in the baseline fails in one trial: blocked at once.
    (t / "ab-log.jsonl").unlink()
    g = trials("gold", 3); (t / "gold1" / "g2.json").write_text("{}")
    code, out, _ = run("score.py", sf, *g, "--baseline", base, "--out", t / "gold")
    expect("golden broken in one trial -> exit 1", code == 1 and json.loads((t / "gold.json").read_text())["golden_broke"] == ["g2"], out)

    # Critical cases need 5 trials, and one failing trial blocks.
    crit = t / "crit.jsonl"
    jsonl(crit, [{"id": "g1", "tier": "golden", "intent": "must_not", "critical": True, "source": "x",
                  "checks": [{"type": "contains", "value": "Broken"}]}])
    code, out, _ = run("score.py", crit, *trials("c3", 3))
    expect("critical with 3 trials needs 5", code == 2 and "Need more trials" in out, out)
    c5 = trials("c5", 5)
    code, _, _ = run("score.py", crit, *c5)
    (t / "c54" / "g1.md").write_text("nothing")
    code_b, out_b, _ = run("score.py", crit, *c5)
    expect("critical: 5 clean trials pass, one bad trial blocks", code == 0 and code_b == 1, out_b)

    # Token budget fails a correct run; the bill is printed.
    tb = trials("tok", 3, tokens=5000)
    code, out, _ = run("score.py", sf, *tb, "--baseline", base, "--token-budget", "4000", "--out", t / "tok")
    tk = json.loads((t / "tok.json").read_text())
    expect("over budget fails even when correct", len(tk["tokens"]["over_budget"]) == 8
           and "Token bill" in out and "over token budget" in out.lower(), out)
    code, out, _ = run("score.py", sf, *tb, "--token-budget", "6000", "--out", t / "tok2")
    expect("within budget passes", not json.loads((t / "tok2.json").read_text())["tokens"]["over_budget"])
    jsonl(t / "mt.jsonl", [{"id": "r1", "tier": "real", "intent": "must_do", "source": "x",
                            "checks": [{"type": "max_tokens", "value": 1000, "field": "output"}]}])
    run("score.py", t / "mt.jsonl", t / "tok0", "--out", t / "mt")
    det = json.loads((t / "mt.json").read_text())["cases"][0]
    expect("max_tokens check on the output field", det["passes"] == 0 and "1,250 tokens" in str(det["failing"]), det)

    # Free path: a different route is advice, not a failure.
    jsonl(t / "free.jsonl", [{"id": "r1", "tier": "real", "intent": "must_do", "source": "x", "path": "free",
                              "checks": [{"type": "order", "value": ["Skill", "Fetch"]}, {"type": "regex", "value": "Report"}]}])
    code, out, _ = run("score.py", t / "free.jsonl", *trials("fr", 3), "--out", t / "free")
    fr = json.loads((t / "free.json").read_text())["cases"][0]
    expect("free path: wrong route is advice, end state gates", fr["state"] == "pass" and any("order" in x for x in fr["failing"]), fr)

    # Hidden holdout: aggregates only; overfit flagged against the tuned score.
    code, out, _ = run("score.py", sf, *trials("ho", 3, broken=("r1", "r2", "r3", "r4", "r5")), "--hidden", "--tuned", t / "base.json")
    h = json.loads(out)
    expect("hidden view has no case ids", "r1" not in out and "au1" not in out and "pass_rate" in h, out)
    expect("tuned high, holdout low -> overfitted, exit 1", h["overfitted"] and code == 1, h)

    # Known-bad set: every entry must fail, else the check is not trusted.
    kb = t / "known-bad"; kb.mkdir()
    (kb / "kb-health-repeat.md").write_text("REGRESSION  dangling handoff: ai-team-blueprint -> claude-api\nNEW SKILL   choose-effort\n")
    kprev = t / "kb-prev"; kprev.mkdir()
    (kprev / "kb-health-repeat.md").write_text("REGRESSION  dangling handoff: ai-team-blueprint -> claude-api\nNEW SKILL   choose-effort\n")
    (kb / "kb-weak.md").write_text("Everything looks fine.\n")
    kbs = t / "kb.jsonl"
    jsonl(kbs, [{"id": "kb-health-repeat", "source": "skills-site#24", "why": "nightly report repeats yesterday's items",
                 "checks": [{"type": "not_in_previous", "value": "^(REGRESSION|NEW SKILL)"}]},
                {"id": "kb-weak", "source": "invented", "why": "no findings, no evidence",
                 "checks": [{"type": "max_lines", "value": 5}]}])
    code, out, err = run("score.py", kbs, kb, "--expect-fail", "--previous", kprev)
    v = json.loads(out)
    expect("known-bad: dedup check catches #24's repeat", any(r["id"] == "kb-health-repeat" and r["status"] == "caught" for r in v["rows"]), v)
    expect("known-bad: a check that lets a bad output pass is untrusted, exit 1", code == 1 and v["missed"] == ["kb-weak"]
           and "caught 1 of 2" in err, err)
    jsonl(t / "kbj.jsonl", [{"id": "kb-weak", "source": "x", "why": "w", "checks": [{"type": "judge", "rubric": "Any finding?"}]}])
    code, _, _ = run("score.py", t / "kbj.jsonl", kb, "--expect-fail")
    expect("known-bad: an ungraded judge is pending, exit 2", code == 2)

    # Pipeline gates: duplicate PR work, untrusted issue source, diff outside the spec.
    gd = t / "gates"; (gd / "ctx").mkdir(parents=True); gb = t / "gate-bad"; gb.mkdir(); gg = t / "gate-good"; gg.mkdir()
    (gd / "ctx" / "prs.json").write_text(json.dumps([{"number": 24, "state": "open", "files": ["evals/triggers.json"], "covers": ["skill-a", "skill-b"]},
                                                     {"number": 20, "state": "merged", "files": ["README.md"], "covers": []}]))
    (gd / "ctx" / "issues.json").write_text(json.dumps([{"number": 31, "author": {"login": "owner"}, "labels": []},
                                                        {"number": 32, "author": {"login": "stranger"}, "labels": [{"name": "bug"}]},
                                                        {"number": 33, "author": {"login": "friend"}, "labels": [{"name": "pipeline-ok"}]}]))
    (gd / "ctx" / "spec.md").write_text("# Spec\n\n## Files\n- `evals/triggers.json`\n- evals/routing/*.json\n\n## Notes\nnone\n")
    jsonl(gd / "gates.jsonl", [
        {"id": "dup", "tier": "golden", "intent": "must_not", "source": "x", "checks": [{"type": "triage_skips_open_pr", "open_prs": "ctx/prs.json"}]},
        {"id": "src", "tier": "golden", "intent": "must_not", "source": "x", "checks": [{"type": "triage_trusted_source", "issues": "ctx/issues.json", "owners": ["owner"]}]},
        {"id": "spec", "tier": "golden", "intent": "must_not", "source": "x", "checks": [{"type": "diff_within_spec", "spec": "ctx/spec.md"}]}])
    (gb / "dup.json").write_text(json.dumps({"selected": [{"title": "cases for a and b", "covers": ["skill-b"], "files": []}]}))
    (gg / "dup.json").write_text(json.dumps({"selected": [{"title": "readme", "files": ["README.md"]}], "dropped": [{"title": "cases for a and b"}]}))
    (gb / "src.json").write_text(json.dumps({"selected": [{"issue": 31}, {"issue": 32}]}))
    (gg / "src.json").write_text(json.dumps({"selected": [{"issue": 31}, {"issue": 33}]}))
    diff = ("diff --git a/evals/triggers.json b/evals/triggers.json\n--- a/evals/triggers.json\n+++ b/evals/triggers.json\n@@ -1 +1 @@\n-x\n+y\n"
            "diff --git a/evals/routing/r.json b/evals/routing/r.json\n--- a/evals/routing/r.json\n+++ b/evals/routing/r.json\n")
    (gg / "spec.diff").write_text(diff)
    (gb / "spec.diff").write_text(diff + "diff --git a/scripts/build.py b/scripts/build.py\n--- a/scripts/build.py\n+++ b/scripts/build.py\n")
    code, out, err = run("score.py", gd / "gates.jsonl", gb, "--expect-fail")
    v = json.loads(out)
    ev = {r["id"]: " ".join(r["evidence"]) for r in v["rows"]}
    expect("gates: all three bad outputs caught", code == 0 and v["caught"] == 3, v)
    expect("gates: evidence names the open PR, the stranger and the off-spec file",
           "open PR #24 on skill-b" in ev["dup"] and "#32 by stranger" in ev["src"] and "scripts/build.py" in ev["spec"], ev)
    code, out, _ = run("score.py", gd / "gates.jsonl", gg, "--repeat", gg, "--repeat", gg, "--out", t / "gg")
    expect("gates: the good outputs pass (merged PRs and labelled issues are fine)", code == 0
           and all(r["state"] == "pass" for r in json.loads((t / "gg.json").read_text())["cases"]), out)
    code, out, _ = run("score.py", gd / "gates.jsonl", gg, "--expect-fail")
    expect("gates: a check that passes good outputs cannot be trusted on them", code == 1 and len(json.loads(out)["missed"]) == 3)
    (gb / "dup.json").write_text("not json")
    run("score.py", gd / "gates.jsonl", gb, "--out", t / "gbad")
    det = next(r for r in json.loads((t / "gbad.json").read_text())["cases"] if r["id"] == "dup")["failing"]
    expect("gates: unreadable output fails with a reason, no crash", any("unreadable" in f for f in det), det)

    # Forbidden tool, error matching, max_calls.
    jsonl(t / "traj.jsonl", [{"id": "x", "tier": "real", "source": "s", "checks": [
        {"type": "tool_not_called", "value": "Bash:rm -rf"}, {"type": "no_error_matching", "value": "403"},
        {"type": "max_calls", "value": 2}]}])
    xd = t / "x"; xd.mkdir()
    (xd / "x.trace.jsonl").write_text(session("sx", "seo-crawl", ["Fetch", "Bash"], errors=("Fetch",)).replace('"command": "bash"', '"command": "rm -rf out"'))
    run("score.py", t / "traj.jsonl", xd, "--out", t / "x")
    fl = json.loads((t / "x.json").read_text())["cases"][0]["failing"]
    expect("forbidden call, matching error and too many calls all fail", len(fl) == 3, fl)

    # Slash-command skill use.
    jsonl(t / "slash.jsonl", [{"id": "s", "tier": "real", "source": "x", "checks": [{"type": "skill_used", "value": "seo-crawl"}]}])
    sd = t / "slash"; sd.mkdir()
    (sd / "s.trace.jsonl").write_text(session("ss", None, ["Bash"], prompt="<command-name>/seo-crawl</command-name> acme.com"))
    run("score.py", t / "slash.jsonl", sd, "--out", t / "slash")
    expect("skill_used accepts a slash command", json.loads((t / "slash.json").read_text())["cases"][0]["passes"] == 1)

    # Invariants with match "*" and dedup against the previous run.
    jsonl(t / "inv.jsonl", [{"id": "dedup", "tier": "real", "source": "loop-schedule", "match": "*",
                             "checks": [{"type": "not_in_previous", "value": r"^- "}]}])
    rep = t / "reports"; rep.mkdir()
    (prev / "acme.md").write_text("- old A\n- old B\n"); (prev / "beta.md").write_text("- beta\n")
    (rep / "acme.md").write_text("- new C\n- old A\n"); (rep / "beta.md").write_text("- beta new\n")
    run("score.py", t / "inv.jsonl", rep, "--previous", prev, "--out", t / "inv")
    st = {r["id"]: r["passes"] for r in json.loads((t / "inv.json").read_text())["cases"]}
    expect("dedup flags the repeated item per file", st == {"dedup:acme.md": 0, "dedup:beta.md": 1}, st)

    # Unusable suites.
    (t / "bad.jsonl").write_text('{"id": "x", "checks": []}\n{"id": "y", "tier": "gold", "intent": "maybe", "source": "s", "checks": [{"type": "nope"}]}\nnot json\n')
    code, _, err = run("score.py", t / "bad.jsonl", "--validate")
    expect("bad suite exits 2 naming each problem", code == 2 and all(x in err for x in ("missing 'source'", "unknown tier", "unknown intent", "unknown type", "not JSON")), err)
    code, _, _ = run("score.py", sf, t / "nope")
    expect("missing trial folder exits 2", code == 2)

    # ---------- intake ----------
    sess = t / "sessions" / "-home-user-proj"; sess.mkdir(parents=True)
    (sess / "s1.jsonl").write_text(session("s1", "seo-crawl", ["Bash", "Write"], prompt="crawl acme.com, key sk-abcdefghijklmnopqrstuv"))
    (sess / "s2.jsonl").write_text(session("s2", None, ["Bash"], prompt="/seo-crawl acme.com"))
    (sess / "s3.jsonl").write_text(session("s3", "other-skill", ["Bash"]))
    code, out, err = run("intake.py", "sessions", t / "sessions", "--skill", "seo-crawl")
    rows = [json.loads(l) for l in out.splitlines()]
    expect("sessions: Skill call and slash command both found, other skill skipped", len(rows) == 2, rows)
    s1 = next(r for r in rows if "[masked]" in r["prompt"])
    expect("sessions: real tier with draft order and masked prompt",
           s1["tier"] == "real" and any(c["type"] == "order" for c in s1["checks"]) and "sk-abc" not in out, s1)

    prs = [
        {"number": 12, "url": "u12", "state": "CLOSED", "mergedAt": None, "author": {"login": "claude-bot"},
         "headRefName": "claude/x", "title": "Fix", "reviews": [{"state": "COMMENTED", "body": "Wrong approach, use the cache"}],
         "comments": [], "commits": []},
        {"number": 15, "url": "u15", "state": "MERGED", "mergedAt": "2026-11-01", "author": {"login": "claude-bot"},
         "headRefName": "claude/y", "title": "Add", "reviews": [], "comments": [],
         "commits": [{"messageHeadline": "fix typo", "authors": [{"login": "alice"}]}]},
        {"number": 16, "url": "u16", "state": "MERGED", "mergedAt": "2026-11-02", "author": {"login": "claude-bot"},
         "headRefName": "claude/z", "title": "Clean", "reviews": [{"state": "APPROVED", "body": ""}], "comments": [],
         "commits": [{"messageHeadline": "x", "authors": [{"login": "claude-bot"}]}]},
        {"number": 17, "url": "u17", "state": "CLOSED", "mergedAt": None, "author": {"login": "alice"},
         "headRefName": "feature", "title": "Human PR", "reviews": [], "comments": [], "commits": []},
    ]
    (t / "prs.json").write_text(json.dumps(prs))
    code, out, _ = run("intake.py", "prs", t / "prs.json", "--agent", "claude-bot")
    rows = {json.loads(l)["id"]: json.loads(l) for l in out.splitlines()}
    expect("prs: rejected and edited agent PRs only", set(rows) == {"pr-12", "pr-15"}, list(rows))
    expect("prs: author tier, reviewer's words in the rubric",
           rows["pr-12"]["tier"] == "author" and "use the cache" in rows["pr-12"]["checks"][0]["rubric"]
           and rows["pr-15"]["human_signal"] == "edited", rows.get("pr-12"))
    code, _, err = run("intake.py", "prs", t / "prs.json")
    expect("prs: refuses without saying which PRs are the agent's", code == 2)

    issues = [{"number": 3, "url": "i3", "state": "OPEN", "body": "x\n```json\n" + json.dumps(
        {"fingerprint": "aaaabbbbcccc", "skill": "seo-crawl", "tool": "fetch", "happened": "403",
         "fix": "send UA", "error_pattern": "403", "count": 3}) + "\n```"},
              {"number": 4, "url": "i4", "state": "OPEN", "body": "no json here"}]
    (t / "issues.json").write_text(json.dumps(issues))
    (t / "queue.jsonl").write_text(json.dumps({"fingerprint": "aaaabbbbcccc", "skill": "seo-crawl", "tool": "fetch",
                                               "happened": "403", "fix": "send UA", "count": 2, "reproducible": True}) + "\n")
    code, out, _ = run("intake.py", "papercuts", t / "issues.json", "--skill", "seo-crawl")
    r = json.loads(out.splitlines()[0])
    expect("papercuts from gh issues: grouped, error pattern becomes a check",
           len(out.splitlines()) == 1 and "x3" in r["source"] and {"type": "no_error_matching", "value": "403"} in r["checks"], r)
    code, out, _ = run("intake.py", "papercuts", t / "queue.jsonl")
    expect("papercuts from queue: reproducible becomes golden", json.loads(out)["tier"] == "golden", out)

    cand = t / "cand.jsonl"
    cand.write_text("".join(l + "\n" for l in run("intake.py", "prs", t / "prs.json", "--agent", "claude-bot")[1].splitlines()))
    code, out, _ = run("intake.py", "show", cand)
    expect("show prints a table and tier counts", "| pr-12 | author | to set |" in out and "author 2" in out, out)

    # ---------- ablation ----------
    wa, wb, wa2 = t / "with", t / "without", t / "with2"
    for d in (wa, wb, wa2):
        d.mkdir()
    for i in range(12):
        (wa / f"c{i}.trace.jsonl").write_text(session(f"w{i}", "seo-crawl", ["Bash"], final=f"GOOD answer {i}"))
        (wa2 / f"c{i}.trace.jsonl").write_text(session(f"v{i}", "seo-crawl", ["Bash"], final=f"GOOD answer {i}"))
        (wb / f"c{i}.trace.jsonl").write_text(session(f"n{i}", None, ["Bash", "Bash", "Bash"], errors=("Bash",), final=f"weak answer {i}"))
    code, out, _ = run("ablation.py", "pair", wa, wb, "--out", t / "pairs", "--seed", 7)
    files = sorted((t / "pairs").glob("c*.md"))
    blind = all("with" not in f.read_text().lower().replace("without", "") and "Answer 1" in f.read_text() for f in files)
    expect("pair: 12 blind files, key kept outside the folder",
           code == 0 and len(files) == 12 and blind and (t / "pairs.key.json").exists()
           and not list((t / "pairs").glob("*key*")), out)
    key = json.loads((t / "pairs.key.json").read_text())
    flips = {k["1"] for k in key.values()}
    expect("pair: order is randomised", flips == {"A", "B"}, flips)
    # A judge that always picks the GOOD answer, reading only the pair files.
    verdicts = {}
    for f in files:
        txt = f.read_text()
        verdicts[f.stem] = "1" if txt.index("GOOD") < txt.index("weak") else "2"
    (t / "pairs" / "verdicts.json").write_text(json.dumps(verdicts))
    run("ablation.py", "pair", wa, wa2, "--out", t / "noise", "--seed", 3)
    nkey = json.loads((t / "noise.key.json").read_text())
    (t / "noise" / "verdicts.json").write_text(json.dumps({k: ("1" if i % 2 else "2") for i, k in enumerate(nkey)}))
    code, out, err = run("ablation.py", "score", t / "pairs", "--noise", t / "noise", "--arm-a", wa, "--arm-b", wb)
    res = json.loads(out)
    expect("score: skill wins every blind comparison -> helps", res["a_share"] == 1.0 and res["verdict"] == "helps", res)
    expect("score: noise band from identical arms", res["noise_band"] is not None and res["noise_band"] <= 0.1, res["noise_band"])
    expect("score: trace stats per arm", res["arm_b"]["tool_calls"] > res["arm_a"]["tool_calls"]
           and res["arm_b"]["tool_errors"] > res["arm_a"]["tool_errors"], (res["arm_a"], res["arm_b"]))
    (t / "pairs" / "verdicts.json").write_text(json.dumps({k: "tie" for k in verdicts}))
    code, out, _ = run("ablation.py", "score", t / "pairs")
    expect("score: all ties -> no clear difference", json.loads(out)["verdict"] == "no clear difference")

# ---------- token windows ----------
def usage(i, o, cr=0, cw=0):
    return {"input_tokens": i, "output_tokens": o, "cache_read_input_tokens": cr, "cache_creation_input_tokens": cw}


tw = [
    {"type": "user", "message": {"role": "user", "content": "<command-name>/seo-crawl</command-name> acme.com"}},
    # m1 is logged twice (two content blocks); the last usage is the final one and counts once.
    {"type": "assistant", "message": {"role": "assistant", "id": "m1", "usage": usage(100, 5), "content": [{"type": "text", "text": "Crawling."}]}},
    {"type": "assistant", "message": {"role": "assistant", "id": "m1", "usage": usage(100, 20), "content": [
        {"type": "tool_use", "id": "t1", "name": "Skill", "input": {"skill": "seo-check"}}]}},
    {"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "t1", "content": "loaded"}]}},
    {"type": "assistant", "message": {"role": "assistant", "id": "m2", "usage": usage(300, 50, cr=1000), "content": [{"type": "text", "text": "Checked."}]}},
    {"type": "assistant", "isSidechain": True, "message": {"role": "assistant", "id": "m3", "usage": usage(40, 10), "content": [{"type": "text", "text": "sub"}]}},
    {"type": "assistant", "message": {"role": "assistant", "id": "m4", "usage": usage(200, 30), "content": [
        {"type": "tool_use", "id": "t2", "name": "Skill", "input": {"skill": "seo-check"}}]}},
    {"type": "assistant", "message": {"role": "assistant", "id": "m5", "usage": usage(500, 100, cw=2000), "content": [{"type": "text", "text": "Done."}]}},
]
with tempfile.TemporaryDirectory() as tmp:
    f = Path(tmp) / "w.trace.jsonl"
    f.write_text("\n".join(json.dumps(e) for e in tw) + "\n")
    code, out, _ = run("traces.py", f)
    d = json.loads(out)
    by = d["tokens_by_skill"]
    expect("tokens: repeated message id counted once, last value kept", d["tokens"]["output"] == 20 + 50 + 10 + 30 + 100, d["tokens"])
    expect("tokens: slash command opens a window; Skill call switches it from the next message",
           by["seo-crawl"]["tokens"]["total"] == 120 and by["seo-crawl"]["invocations"] == 1
           and by["seo-check"]["invocations"] == 2 and by["seo-check"]["tokens"]["total"] == 1350 + 50 + 230 + 2600, by)
    expect("tokens: windows add up to the total", sum(v["tokens"]["total"] for v in by.values()) == d["tokens"]["total"], by)
    expect("tokens: subagent messages split out", d["tokens_subagents"]["total"] == 50, d["tokens_subagents"])
    expect("tokens: peak context is the largest input side", d["peak_context"] == 2500, d["peak_context"])
    jsonl(Path(tmp) / "c.jsonl", [{"id": "w", "tier": "real", "intent": "must_do", "source": "x", "checks": [
        {"type": "skill_tokens", "skill": "seo-check", "value": 2000},
        {"type": "skill_tokens", "skill": "seo-crawl", "value": 2000},
        {"type": "max_context", "value": 2000},
        {"type": "skill_tokens", "skill": "never-ran", "value": 10}]}])
    run("score.py", Path(tmp) / "c.jsonl", tmp, "--out", Path(tmp) / "c")
    fl = json.loads((Path(tmp) / "c.json").read_text())["cases"][0]["failing"]
    expect("skill_tokens per invocation, max_context, missing skill",
           any("2,115 tokens per invocation of seo-check" in x for x in fl) and not any("seo-crawl" in x for x in fl)
           and any("peak context 2,500" in x for x in fl) and any("never-ran" in x for x in fl), fl)

# ---------- traces ----------
code, out, _ = run("traces.py", FIX / "session.jsonl")
tr = json.loads(out)
expect("trace: two calls in order", [c["name"] for c in tr["calls"]] == ["WebFetch", "Bash"], tr["calls"])
expect("trace: errors and denial counted", tr["tool_errors"] == 2 and tr["permission_denials"] == 1, tr)
expect("trace: end from result line", tr["end"] == "error_max_turns" and "ended_error_max_turns" in tr["flags"], tr["flags"])
expect("trace: secrets and emails masked", "abcd1234efgh5678" not in out and "ops@acme.com" not in out, out)
with tempfile.TemporaryDirectory() as tmp:
    log = Path(tmp) / "run.log"
    log.write_text("start\nERROR: upstream timed out\n", encoding="utf-8")
    code, out, _ = run("traces.py", log)
    expect("plain log: error lines found", json.loads(out)["error_line_count"] == 1)
    code, out, _ = run("traces.py", Path(tmp) / "missing")
    expect("missing trace exits 2", code == 2)

print(f"\n{'FAILED: ' + ', '.join(failures) if failures else 'all passed'}")
sys.exit(1 if failures else 0)

#!/usr/bin/env python3
"""Score one run of a loop against a golden set or invariants file.

Usage:
  python score.py CASES.jsonl RUN_DIR [--baseline baseline.json] [--previous PREV_RUN_DIR]
                  [--out PREFIX] [--save-baseline]

CASES.jsonl  one case per line: {"id", "kind", "source", "checks": [...], optional "match", "critical"}
RUN_DIR      one output file per case (<id>.txt|.md|.json), plus optional judgments.json

Exit codes: 0 pass, 1 regression or failed critical case, 2 judge checks pending or unusable input.
Writes PREFIX.json and PREFIX.md when --out is given. Standard library only.
"""
import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path

OUTPUT_EXTS = (".txt", ".md", ".json", ".out", ".html")
KINDS = {"positive", "negative", "edge", "regression"}


def load_cases(path):
    cases, errors = [], []
    for n, line in enumerate(Path(path).read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("//"):
            continue
        try:
            case = json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(f"line {n}: not JSON ({e.msg})")
            continue
        for key in ("id", "checks"):
            if key not in case:
                errors.append(f"line {n}: missing '{key}'")
        if not case.get("checks"):
            errors.append(f"line {n}: needs at least one check")
        if case.get("kind") and case["kind"] not in KINDS:
            errors.append(f"line {n}: unknown kind '{case['kind']}'")
        cases.append(case)
    ids = [c.get("id") for c in cases]
    for dup in sorted({i for i in ids if ids.count(i) > 1 and i is not None}):
        errors.append(f"duplicate id '{dup}'")
    return cases, errors


def outputs_for(case, run_dir):
    files = sorted(p for p in Path(run_dir).iterdir()
                   if p.is_file() and p.suffix in OUTPUT_EXTS and p.name != "judgments.json")
    pattern = case.get("match")
    if pattern:
        return [p for p in files if fnmatch.fnmatch(p.name, pattern)]
    return [p for p in files if p.stem == case["id"]]


def json_path(data, path):
    cur = data
    for part in path.split(".") if path else []:
        if isinstance(cur, list) and part.isdigit() and int(part) < len(cur):
            cur = cur[int(part)]
        elif isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            raise KeyError(path)
    return cur


def item_lines(text, pattern):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if pattern:
        rx = re.compile(pattern)
        lines = [l for l in lines if rx.search(l)]
    return lines


def run_check(check, text, out_file, previous_dir, judgments, key):
    """Return (status, detail): status is pass, fail or pending."""
    t = check.get("type")
    v = check.get("value")
    flags = re.I if check.get("ignore_case") else 0
    try:
        if t in ("contains", "not_contains"):
            hay, needle = (text.lower(), str(v).lower()) if check.get("ignore_case") else (text, str(v))
            found = needle in hay
            ok = found if t == "contains" else not found
            return ("pass" if ok else "fail"), f"{'found' if found else 'not found'}: {v!r}"
        if t in ("regex", "not_regex"):
            m = re.search(v, text, flags | re.M)
            ok = bool(m) if t == "regex" else not m
            return ("pass" if ok else "fail"), (f"matched {m.group(0)[:60]!r}" if m else "no match")
        if t == "count":
            n = len(re.findall(v, text, flags | re.M))
            lo, hi = check.get("min"), check.get("max")
            ok = (lo is None or n >= lo) and (hi is None or n <= hi)
            return ("pass" if ok else "fail"), f"{n} matches (min {lo}, max {hi})"
        if t == "min_len":
            return ("pass" if len(text) >= v else "fail"), f"{len(text)} chars"
        if t == "max_len":
            return ("pass" if len(text) <= v else "fail"), f"{len(text)} chars"
        if t == "max_lines":
            n = len([l for l in text.splitlines() if l.strip()])
            return ("pass" if n <= v else "fail"), f"{n} lines"
        if t == "json":
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                return "fail", "output is not JSON"
            try:
                got = json_path(data, check.get("path", ""))
            except KeyError:
                return "fail", f"path {check.get('path')!r} missing"
            if "equals" in check:
                ok = got == check["equals"]
                return ("pass" if ok else "fail"), f"{check.get('path')} = {json.dumps(got)[:60]}"
            return "pass", f"{check.get('path')} exists"
        if t == "not_in_previous":
            if previous_dir is None:
                return "pending", "needs --previous"
            prev_file = Path(previous_dir) / out_file.name
            if not prev_file.exists():
                return "pass", "no previous output for this file"
            prev = set(item_lines(prev_file.read_text(encoding="utf-8", errors="replace"), v))
            repeats = [l for l in item_lines(text, v) if l in prev]
            return ("fail" if repeats else "pass"), (
                f"{len(repeats)} repeated, first: {repeats[0][:60]!r}" if repeats else "no repeats")
        if t == "judge":
            verdict = judgments.get(key)
            if not isinstance(verdict, dict) or "pass" not in verdict:
                return "pending", check.get("rubric", "")
            return ("pass" if verdict["pass"] else "fail"), str(verdict.get("why", ""))[:120]
    except re.error as e:
        return "fail", f"bad regex: {e}"
    except TypeError as e:
        return "fail", f"bad check fields: {e}"
    return "fail", f"unknown check type {t!r}"


def score(cases, run_dir, previous_dir=None):
    jpath = Path(run_dir) / "judgments.json"
    judgments = json.loads(jpath.read_text(encoding="utf-8")) if jpath.exists() else {}
    results, pending = [], []
    for case in cases:
        files = outputs_for(case, run_dir)
        if not files:
            results.append({"id": case["id"], "file": None, "kind": case.get("kind"),
                            "critical": bool(case.get("critical")), "status": "fail",
                            "checks": [{"index": 0, "type": "output", "status": "fail",
                                        "detail": "no output file"}]})
            continue
        for f in files:
            text = f.read_text(encoding="utf-8", errors="replace")
            rid = case["id"] if not case.get("match") else f"{case['id']}:{f.name}"
            checks = []
            for i, check in enumerate(case["checks"]):
                key = f"{rid}#{i}"
                status, detail = run_check(check, text, f, previous_dir, judgments, key)
                checks.append({"index": i, "type": check.get("type"), "status": status, "detail": detail})
                if status == "pending":
                    pending.append({"key": key, "file": f.name, "type": check.get("type"), "detail": detail})
            statuses = {c["status"] for c in checks}
            status = "fail" if "fail" in statuses else "pending" if "pending" in statuses else "pass"
            results.append({"id": rid, "file": f.name, "kind": case.get("kind"),
                            "critical": bool(case.get("critical")), "status": status, "checks": checks})
    return results, pending


def summarize(results, pending, baseline):
    passed = [r["id"] for r in results if r["status"] == "pass"]
    failed = [r["id"] for r in results if r["status"] == "fail"]
    base_pass = set(baseline.get("passed", [])) if baseline else set()
    base_fail = set(baseline.get("failed", [])) if baseline else set()
    regressions = sorted(i for i in failed if i in base_pass)
    fixed = sorted(i for i in passed if i in base_fail)
    new_failing = sorted(i for i in failed if i not in base_pass and i not in base_fail)
    critical = sorted(r["id"] for r in results if r["critical"] and r["status"] == "fail")
    scored = len(passed) + len(failed)
    rate = round(len(passed) / scored, 4) if scored else 0.0
    if regressions or critical or (baseline and new_failing):
        verdict, code = "fail", 1
    elif pending:
        verdict, code = "pending", 2
    elif not baseline and failed:
        verdict, code = "fail", 1
    else:
        verdict, code = "pass", 0
    return {"verdict": verdict, "exit": code, "pass_rate": rate,
            "baseline_pass_rate": baseline.get("pass_rate") if baseline else None,
            "counts": {"pass": len(passed), "fail": len(failed),
                       "pending": len([r for r in results if r["status"] == "pending"])},
            "passed": passed, "failed": failed, "regressions": regressions, "fixed": fixed,
            "new_failing": new_failing, "critical_failed": critical, "pending": pending,
            "results": results}


def to_markdown(s, cases_path, run_dir):
    lines = [f"# Scorecard — {Path(run_dir).name}", "",
             f"Cases: `{cases_path}` · Verdict: **{s['verdict']}** · Pass rate: {s['pass_rate']:.0%}"
             + (f" (baseline {s['baseline_pass_rate']:.0%})" if s["baseline_pass_rate"] is not None else ""),
             ""]
    for label, key in (("Regressions", "regressions"), ("Critical failures", "critical_failed"),
                       ("New failing", "new_failing"), ("Fixed since baseline", "fixed")):
        if s[key]:
            lines.append(f"**{label}:** {', '.join(s[key])}")
    lines += ["", "| Case | Kind | Status | Failing or pending checks |", "| --- | --- | --- | --- |"]
    for r in s["results"]:
        bad = "; ".join(f"#{c['index']} {c['type']}: {c['detail']}"
                        for c in r["checks"] if c["status"] != "pass")
        lines.append(f"| {r['id']} | {r['kind'] or ''} | {r['status']} | {bad.replace('|', '/')} |")
    if s["pending"]:
        lines += ["", "## Pending judge checks", "",
                  "Grade each and write `judgments.json` in the run folder as "
                  '`{"<key>": {"pass": true, "why": "..."}}`.', ""]
        lines += [f"- `{p['key']}` ({p['file']}): {p['detail']}" for p in s["pending"]]
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("cases")
    ap.add_argument("run_dir")
    ap.add_argument("--baseline")
    ap.add_argument("--previous")
    ap.add_argument("--out")
    ap.add_argument("--save-baseline", action="store_true")
    a = ap.parse_args(argv)

    if not Path(a.cases).is_file() or not Path(a.run_dir).is_dir():
        print(f"error: need a cases file and a run folder ({a.cases}, {a.run_dir})", file=sys.stderr)
        return 2
    cases, errors = load_cases(a.cases)
    if errors:
        print("error: cases file is not usable:\n  " + "\n  ".join(errors), file=sys.stderr)
        return 2
    if a.previous and not Path(a.previous).is_dir():
        print(f"error: --previous {a.previous} is not a folder", file=sys.stderr)
        return 2
    baseline = {}
    if a.baseline and Path(a.baseline).exists():
        baseline = json.loads(Path(a.baseline).read_text(encoding="utf-8"))

    results, pending = score(cases, a.run_dir, a.previous)
    s = summarize(results, pending, baseline)
    md = to_markdown(s, a.cases, a.run_dir)
    if a.out:
        Path(a.out + ".json").write_text(json.dumps(s, indent=2), encoding="utf-8")
        Path(a.out + ".md").write_text(md, encoding="utf-8")
    print(md, end="")

    if a.save_baseline:
        if not a.baseline:
            print("error: --save-baseline needs --baseline PATH", file=sys.stderr)
            return 2
        if s["verdict"] != "pass":
            print("refused: baseline not saved because the verdict is not pass", file=sys.stderr)
        else:
            Path(a.baseline).write_text(json.dumps(
                {"pass_rate": s["pass_rate"], "passed": s["passed"], "failed": s["failed"]},
                indent=2), encoding="utf-8")
            print(f"baseline saved: {a.baseline}")
    return s["exit"]


if __name__ == "__main__":
    sys.exit(main())

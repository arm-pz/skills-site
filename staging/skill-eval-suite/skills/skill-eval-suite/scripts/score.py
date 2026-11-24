#!/usr/bin/env python3
"""Score a loop's trials against its eval suite: how often each case passes, flips against the
baseline, noise, token budget, plus holdout and known-bad modes.

Usage:
  python score.py SUITE.jsonl --validate
  python score.py SUITE.jsonl TRIAL_1 [--repeat TRIAL_2 --repeat TRIAL_3 ...]
                  [--baseline baseline.json [--save-baseline]] [--token-budget N] [--previous PREV]
                  [--out PREFIX]
  python score.py HOLDOUT.jsonl TRIAL_1 --repeat ... --hidden [--tuned scorecard.json]
  python score.py KNOWN_BAD.jsonl KNOWN_BAD_DIR --expect-fail

SUITE.jsonl   one case per line: {"id", "tier", "intent", "source", "checks": [...]}
              tier:   golden ~5% (fixed input, mocks) · real ~80% (real prompt, trajectory) · author ~15%
              intent: must_do · must_not · keep_working (every skill needs all three)
              path:   required (default: trajectory checks gate) · free (only the end state gates)
TRIAL_n       per case <id>.txt|.md|.json (output) and/or <id>.trace.jsonl (session), judgments.json.

How it decides (an EDD reading of evals):
- A case is scored as how often it passes across trials. A new case (not in the baseline) needs 3
  trials, a critical one 5, before it counts; split results mean flaky, and flaky cases are kept.
- Against the baseline it reports the same cases' flips: fixed, broke, net. Fixed and broke together
  is a trade-off, not a win. Only a repeated clear loss blocks (net worse >= max(2, 7% of cases) and
  above the noise, on this run and the one before, from ab-log.jsonl next to the baseline).
- A golden case that passed in the baseline, or a critical case, failing in any trial blocks at once.
- --token-budget fails a trial over budget even when its answer is right.
- --hidden prints only aggregates (for a holdout set the tuning agent must never read);
  --tuned compares it with the tuned suite's score and flags overfitting.
- --expect-fail inverts the verdict: every known-bad output must fail, or the checks are not trusted.

Exit codes: 0 pass, 1 blocked, 2 pending verdicts, too few trials, or unusable input. Stdlib only.
"""
import argparse
import fnmatch
import importlib.util
import json
import math
import re
import statistics
import sys
from pathlib import Path

OUTPUT_EXTS = (".txt", ".md", ".json", ".out", ".html", ".diff", ".patch")
KINDS = {"positive", "negative", "edge", "regression"}
TIERS = {"golden": 0.05, "real": 0.80, "author": 0.15}
INTENTS = ("must_do", "must_not", "keep_working")
TARGET = (0.70, 0.90)
NEW_TRIALS, CRITICAL_TRIALS = 3, 5
OUTPUT_CHECKS = {"contains", "not_contains", "regex", "not_regex", "count", "min_len", "max_len",
                 "max_lines", "json", "not_in_previous", "judge"}
# Gates a pipeline's own stages must hold; each reads a context file named relative to the suite.
GATE_CHECKS = {"triage_skips_open_pr", "triage_trusted_source", "diff_within_spec"}
TRACE_CHECKS = {"tool_called", "tool_not_called", "order", "skill_used", "max_tool_errors",
                "max_calls", "no_error_matching", "finished", "max_tokens", "skill_tokens", "max_context"}

_spec = importlib.util.spec_from_file_location("traces", Path(__file__).resolve().parent / "traces.py")
traces = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(traces)


# ---------- suite ----------

def load_suite(path):
    cases, errors = [], []
    for n, line in enumerate(Path(path).read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("//"):
            continue
        try:
            case = json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(f"line {n}: not JSON ({e.msg})")
            continue
        if not isinstance(case, dict):
            errors.append(f"line {n}: not an object")
            continue
        for key in ("id", "checks", "source"):
            if not case.get(key):
                errors.append(f"line {n}: missing '{key}'")
        case.setdefault("tier", "golden")
        if case["tier"] not in TIERS:
            errors.append(f"line {n}: unknown tier '{case['tier']}'")
        if case.get("intent") and case["intent"] not in INTENTS:
            errors.append(f"line {n}: unknown intent '{case['intent']}' (use {', '.join(INTENTS)})")
        if case.get("path", "required") not in ("required", "free"):
            errors.append(f"line {n}: path must be 'required' or 'free'")
        if case.get("kind") and case["kind"] not in KINDS:
            errors.append(f"line {n}: unknown kind '{case['kind']}'")
        for i, c in enumerate(case.get("checks") or []):
            t = c.get("type") if isinstance(c, dict) else None
            if t not in OUTPUT_CHECKS | TRACE_CHECKS | GATE_CHECKS:
                errors.append(f"line {n}: check {i} has unknown type {t!r}")
        case["_base"] = str(Path(path).resolve().parent)
        cases.append(case)
    ids = [c.get("id") for c in cases]
    for dup in sorted({i for i in ids if i and ids.count(i) > 1}):
        errors.append(f"duplicate id '{dup}'")
    return cases, errors


def mix(cases):
    """Tier shares and intent coverage, with notes where the suite drifts from the method."""
    n = len(cases) or 1
    counts = {t: sum(1 for c in cases if c["tier"] == t) for t in TIERS}
    notes = []
    if counts["golden"] == 0:
        notes.append("no golden case: add at least one fixed-input case with tool mocks")
    if counts["author"] == 0:
        notes.append("no author-judged case")
    if counts["real"] / n < 0.6:
        notes.append(f"real prompts are {counts['real'] / n:.0%} of the suite; aim for ~80%")
    if counts["golden"] / n > 0.25:
        notes.append(f"golden cases are {counts['golden'] / n:.0%}; they test a fixed path, not real use")
    no_traj = [c["id"] for c in cases if c["tier"] == "real" and c.get("path", "required") == "required"
               and not any(ch.get("type") in TRACE_CHECKS for ch in c["checks"])]
    if no_traj:
        notes.append(f"required-path real cases without a trajectory check: {', '.join(no_traj[:8])}")
    coverage = {}
    for c in cases:
        coverage.setdefault(c.get("skill", "(suite)"), set()).add(c.get("intent"))
    for skill, got in sorted(coverage.items()):
        missing = [i for i in INTENTS if i not in got]
        if missing:
            notes.append(f"{skill}: no {', '.join(missing)} case")
    no_intent = [c["id"] for c in cases if not c.get("intent")]
    if no_intent:
        notes.append(f"cases without an intent: {', '.join(no_intent[:8])}")
    return {"counts": counts, "shares": {t: round(counts[t] / n, 3) for t in TIERS},
            "intents": {s: [i for i in INTENTS if i in got] for s, got in coverage.items()}, "notes": notes}


# ---------- checks ----------

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


def call_matches(call, spec):
    """spec is 'ToolRegex' or 'ToolRegex:InputRegex'."""
    name_rx, _, input_rx = spec.partition(":")
    return bool(re.fullmatch(name_rx, call["name"] or "")) and (
        not input_rx or re.search(input_rx, call.get("input") or ""))


def tokens_of(tr, field):
    tok = (tr or {}).get("tokens") or {}
    if field == "input+output":
        return (tok.get("input") or 0) + (tok.get("output") or 0) if tok else None
    return tok.get(field)


def output_check(check, text, out_name, previous_dir):
    t, v = check["type"], check.get("value")
    flags = re.I if check.get("ignore_case") else 0
    if t in ("contains", "not_contains"):
        hay, needle = (text.lower(), str(v).lower()) if check.get("ignore_case") else (text, str(v))
        found = needle in hay
        return (found if t == "contains" else not found), f"{'found' if found else 'not found'}: {v!r}"
    if t in ("regex", "not_regex"):
        m = re.search(v, text, flags | re.M)
        return (bool(m) if t == "regex" else not m), (f"matched {m.group(0)[:60]!r}" if m else "no match")
    if t == "count":
        n = len(re.findall(v, text, flags | re.M))
        lo, hi = check.get("min"), check.get("max")
        return (lo is None or n >= lo) and (hi is None or n <= hi), f"{n} matches (min {lo}, max {hi})"
    if t == "min_len":
        return len(text) >= v, f"{len(text)} chars"
    if t == "max_len":
        return len(text) <= v, f"{len(text)} chars"
    if t == "max_lines":
        n = len([l for l in text.splitlines() if l.strip()])
        return n <= v, f"{n} lines"
    if t == "json":
        try:
            got = json_path(json.loads(text), check.get("path", ""))
        except json.JSONDecodeError:
            return False, "output is not JSON"
        except KeyError:
            return False, f"path {check.get('path')!r} missing"
        if "equals" in check:
            return got == check["equals"], f"{check.get('path')} = {json.dumps(got)[:60]}"
        return True, f"{check.get('path')} exists"
    if t == "not_in_previous":
        if previous_dir is None:
            return None, "needs --previous"
        prev_file = Path(previous_dir) / out_name
        if not prev_file.exists():
            return True, "no previous output for this file"
        prev = set(item_lines(prev_file.read_text(encoding="utf-8", errors="replace"), v))
        repeats = [l for l in item_lines(text, v) if l in prev]
        return not repeats, (f"{len(repeats)} repeated, first: {repeats[0][:60]!r}" if repeats else "no repeats")
    raise ValueError(t)


def trace_check(check, tr, token_field):
    t, v = check["type"], check.get("value")
    calls = tr.get("calls", [])
    if t in ("tool_called", "tool_not_called"):
        n = sum(1 for c in calls if call_matches(c, v))
        if t == "tool_not_called":
            return n == 0, f"{n} matching calls to {v!r}"
        return n >= check.get("min", 1), f"{n} matching calls to {v!r}"
    if t == "skill_used":
        n = sum(1 for c in calls if c["name"] == "Skill" and re.search(rf"\b{re.escape(v)}\b", c.get("input") or ""))
        # A skill started with a slash command arrives in the prompt, with no Skill call.
        typed = re.search(rf"(^|<command-name>)/{re.escape(v)}\b", (tr.get("prompt") or "").strip())
        how = "loaded" if n else "typed as /command" if typed else "not loaded"
        return bool(n or typed), f"skill {v!r} {how}"
    if t == "order":
        i = 0
        for c in calls:
            if i < len(v) and call_matches(c, v[i]):
                i += 1
        return i == len(v), f"{i}/{len(v)} steps in order" + ("" if i == len(v) else f"; missing {v[i]!r}")
    if t == "max_tool_errors":
        return tr.get("tool_errors", 0) <= v, f"{tr.get('tool_errors', 0)} tool errors"
    if t == "max_calls":
        return len(calls) <= v, f"{len(calls)} tool calls"
    if t == "no_error_matching":
        hits = [c for c in calls if c.get("error") and re.search(v, c.get("result") or "", re.I)]
        return not hits, (f"{len(hits)} errors match, first in {hits[0]['name']}" if hits else "none match")
    if t == "finished":
        ok = tr.get("end") in ("success", "unknown") and bool(tr.get("final_text"))
        return ok, f"end={tr.get('end')}, final text {'present' if tr.get('final_text') else 'missing'}"
    if t == "skill_tokens":
        entry = (tr.get("tokens_by_skill") or {}).get(check["skill"])
        if not entry or not entry.get("tokens"):
            return False, f"no tokens recorded for skill {check['skill']!r}"
        tok = entry["tokens"]
        field = check.get("field", token_field)
        n = (tok["input"] + tok["output"]) if field == "input+output" else tok[field]
        per = n / max(1, entry["invocations"])
        return per <= v, f"{per:,.0f} tokens per invocation of {check['skill']} (max {v:,})"
    if t == "max_context":
        n = tr.get("peak_context")
        if n is None:
            return False, "trace has no token usage"
        return n <= v, f"peak context {n:,} tokens (max {v:,})"
    if t == "max_tokens":
        n = tokens_of(tr, check.get("field", token_field))
        if n is None:
            return False, "trace has no token usage"
        return n <= v, f"{n:,} tokens (max {v:,})"
    raise ValueError(t)


# ---------- pipeline gates ----------
# Triage output is JSON: {"selected": [{"issue": 23, "title": "...", "files": [...], "covers": [...]}], "dropped": [...]}

def _context(base, rel):
    return json.loads((Path(base) / rel).read_text(encoding="utf-8"))


def _selected(text):
    data = json.loads(text)
    items = data.get("selected", []) if isinstance(data, dict) else []
    return [i for i in items if isinstance(i, dict)]


def spec_files(spec_text):
    """Paths or globs listed under a 'Files' heading of a spec (bullets, backticks optional)."""
    m = re.search(r"^#{1,4}\s*Files\b[^\n]*\n(.*?)(?=^#{1,4}\s|\Z)", spec_text, re.M | re.S)
    if not m:
        return None
    out = []
    for line in m.group(1).splitlines():
        b = re.match(r"\s*[-*]\s+`?([^`\s]+)`?", line)
        if b:
            out.append(b.group(1))
    return out


def diff_paths(text):
    paths = set()
    for line in text.splitlines():
        m = re.match(r"diff --git a/(\S+) b/(\S+)", line)
        if m:
            paths.update(p for p in m.groups() if p != "dev/null")
            continue
        m = re.match(r"(?:\+\+\+|---) (?:[ab]/)?(\S+)", line)
        if m and m.group(1) != "/dev/null":
            paths.add(m.group(1))
    return sorted(paths)


def gate_check(check, text, base):
    t = check["type"]
    if t == "triage_skips_open_pr":
        prs = _context(base, check["open_prs"])
        hits = []
        for item in _selected(text):
            mine = set(item.get("files", [])) | set(item.get("covers", []))
            for pr in prs:
                theirs = set(pr.get("files", [])) | set(pr.get("covers", []))
                shared = sorted(mine & theirs)
                if shared and (pr.get("state", "open").lower() == "open"):
                    hits.append(f"{item.get('title') or item.get('issue')} overlaps open PR #{pr.get('number')} on {', '.join(shared[:4])}")
        return not hits, ("; ".join(hits) if hits else "no selected task overlaps an open PR")
    if t == "triage_trusted_source":
        issues = {int(i["number"]): i for i in _context(base, check["issues"])}
        owners = {o.lower() for o in check.get("owners", [])}
        label = check.get("label", "pipeline-ok")
        bad = []
        for item in _selected(text):
            n = item.get("issue")
            issue = issues.get(int(n)) if n is not None else None
            if issue is None:
                bad.append(f"#{n} not in the issue list")
                continue
            author = ((issue.get("author") or {}).get("login") or "").lower()
            labels = {(l.get("name") if isinstance(l, dict) else l) for l in issue.get("labels", [])}
            if author not in owners and label not in labels:
                bad.append(f"#{n} by {author or 'unknown'} has no {label} label")
        return not bad, ("; ".join(bad) if bad else "every selected issue is from an owner or labelled")
    if t == "diff_within_spec":
        files = spec_files((Path(base) / check["spec"]).read_text(encoding="utf-8"))
        if files is None:
            return False, "spec has no Files list"
        touched = diff_paths(text)
        if not touched:
            return False, "output has no diff"
        outside = [p for p in touched if not any(fnmatch.fnmatch(p, f) for f in files)]
        return not outside, (f"outside the spec's Files: {', '.join(outside)}" if outside
                             else f"{len(touched)} files, all in the spec")
    raise ValueError(t)


def judge_check(case, key, judgments):
    verdict = judgments.get(key)
    if not isinstance(verdict, dict) or "pass" not in verdict:
        idx = int(key.rsplit("#", 1)[1])
        return None, case["checks"][idx].get("rubric", "")
    if case["tier"] == "author" and verdict.get("by") != "author":
        return None, "author-tier verdict needs \"by\": \"author\""
    return bool(verdict["pass"]), f"{verdict.get('by', 'agent')}: {str(verdict.get('why', ''))[:100]}"


# ---------- one trial ----------

def files_for(case, run_dir):
    files = [p for p in Path(run_dir).iterdir() if p.is_file()]
    outs = sorted(p for p in files if p.suffix in OUTPUT_EXTS and p.name != "judgments.json")
    if case.get("match"):
        return [(p.name, p, None) for p in outs if fnmatch.fnmatch(p.name, case["match"])]
    out = next((p for p in outs if p.stem == case["id"]), None)
    trace = next((p for p in files if p.name in (f"{case['id']}.trace.jsonl", f"{case['id']}.jsonl")), None)
    return [(case["id"], out, trace)] if (out or trace) else []


def score_trial(cases, run_dir, previous_dir, budget, token_field):
    jpath = Path(run_dir) / "judgments.json"
    judgments = json.loads(jpath.read_text(encoding="utf-8")) if jpath.exists() else {}
    results = []
    for case in cases:
        entries = files_for(case, run_dir)
        if not entries:
            results.append({"id": case["id"], "case": case, "status": "fail", "tokens": None,
                            "checks": [{"index": -1, "type": "output", "status": "fail",
                                        "detail": "no output or trace file"}]})
            continue
        for label, out_file, trace_file in entries:
            rid = case["id"] if not case.get("match") else f"{case['id']}:{label}"
            tr = traces.load(trace_file, raw=True) if trace_file else None
            text = out_file.read_text(encoding="utf-8", errors="replace") if out_file else ((tr or {}).get("final_text") or "")
            free = case.get("path") == "free"
            checks = []
            for i, check in enumerate(case["checks"]):
                t, key = check.get("type"), f"{rid}#{i}"
                try:
                    if t == "judge":
                        ok, detail = judge_check(case, key, judgments)
                    elif t in GATE_CHECKS:
                        ok, detail = gate_check(check, text, case["_base"])
                    elif t in TRACE_CHECKS:
                        ok, detail = (False, "no trace file") if tr is None else trace_check(check, tr, token_field)
                    else:
                        ok, detail = output_check(check, text, out_file.name if out_file else f"{rid}.txt", previous_dir)
                except re.error as e:
                    ok, detail = False, f"bad regex: {e}"
                except (TypeError, KeyError, AttributeError) as e:
                    ok, detail = False, f"bad check fields: {e}"
                except (OSError, json.JSONDecodeError, ValueError) as e:
                    ok, detail = False, f"unreadable output or context: {str(e)[:120]}"
                status = "pending" if ok is None else "pass" if ok else "fail"
                # On a free path any safe route passes: steps are reported, only the end state gates.
                if free and t in TRACE_CHECKS and t != "max_tokens" and status == "fail":
                    status = "advice"
                checks.append({"index": i, "type": t, "status": status, "detail": detail})
            n_tok = tokens_of(tr, token_field) if tr else None
            if budget is not None:
                if n_tok is None:
                    checks.append({"index": -2, "type": "token_budget", "status": "fail",
                                   "detail": "no token usage in trace"})
                elif n_tok > budget:
                    checks.append({"index": -2, "type": "token_budget", "status": "fail",
                                   "detail": f"{n_tok:,} tokens over budget {budget:,}"})
            st = {c["status"] for c in checks}
            status = "fail" if "fail" in st else "pending" if "pending" in st else "pass"
            results.append({"id": rid, "case": case, "status": status, "checks": checks, "tokens": n_tok})
    return results


# ---------- across trials ----------

def combine(trials, baseline):
    """Per case: passes of trials, flaky or not, enough trials or not."""
    base_cases = (baseline or {}).get("cases", {})
    by_id = {}
    for trial in trials:
        for r in trial:
            by_id.setdefault(r["id"], []).append(r)
    rows, pending = [], []
    for rid, rs in by_id.items():
        case = rs[0]["case"]
        done = [r for r in rs if r["status"] in ("pass", "fail")]
        for r in rs:
            for c in r["checks"]:
                if c["status"] == "pending":
                    pending.append({"key": f"{rid}#{c['index']}", "tier": case["tier"], "detail": c["detail"]})
        passes = sum(r["status"] == "pass" for r in done)
        need = CRITICAL_TRIALS if case.get("critical") else NEW_TRIALS if rid not in base_cases else 1
        if len(done) < len(rs):
            state = "pending"
        elif len(done) < need:
            state = "needs_trials"
        elif passes == len(done):
            state = "pass"
        elif passes == 0:
            state = "fail"
        else:
            state = "flaky"
        toks = [r["tokens"] for r in rs if r["tokens"] is not None]
        rows.append({"id": rid, "tier": case["tier"], "intent": case.get("intent"),
                     "critical": bool(case.get("critical")), "state": state, "passes": passes,
                     "trials": len(done), "need": need, "rate": round(passes / len(done), 4) if done else None,
                     "tokens": round(statistics.median(toks)) if toks else None,
                     "failing": sorted({f"#{c['index']} {c['type']}: {c['detail']}" for r in rs
                                        for c in r["checks"] if c["status"] in ("fail", "advice", "pending")})})
    return rows, pending


def flips(rows, baseline):
    """Same-case comparison with the baseline: which cases moved, not how the average moved."""
    base = (baseline or {}).get("cases", {})
    fixed, broke = [], []
    for r in rows:
        b = base.get(r["id"])
        if b is None or r["rate"] is None or r["state"] in ("needs_trials", "pending"):
            continue
        was, now = b.get("rate", 0) >= 0.5, r["rate"] >= 0.5
        if b.get("rate") == 0.5 or r["rate"] == 0.5:
            continue  # a coin flip on either side is noise, not a move
        if not was and now:
            fixed.append(r["id"])
        elif was and not now:
            broke.append(r["id"])
    return fixed, broke


def summarize(cases, trials, baseline, budget, ab_log_path, token_field):
    rows, pending = combine(trials, baseline)
    scored = [r for r in rows if r["state"] in ("pass", "fail", "flaky")]
    n = len(scored)
    pass_rate = round(sum(r["rate"] for r in scored) / n, 4) if n else 0.0
    noise = round(sum(r["state"] == "flaky" for r in scored) / n, 4) if n and len(trials) > 1 else None
    fixed, broke = flips(rows, baseline)
    net = len(broke) - len(fixed)
    threshold = max(2, math.ceil(0.07 * max(n, 1)))
    noise_cases = (noise or 0) * n
    clear_loss = bool(baseline) and net >= threshold and net > noise_cases
    history = []
    if ab_log_path and Path(ab_log_path).exists():
        history = [json.loads(l) for l in Path(ab_log_path).read_text(encoding="utf-8").splitlines() if l.strip()]
    repeated_loss = clear_loss and bool(history) and history[-1].get("clear_loss")

    base_cases = (baseline or {}).get("cases", {})
    golden_broke = sorted(r["id"] for r in rows if r["tier"] == "golden" and base_cases.get(r["id"], {}).get("rate") == 1
                          and r["passes"] < r["trials"])
    critical = sorted(r["id"] for r in rows if r["critical"] and r["trials"] and r["passes"] < r["trials"])
    needs = sorted(r["id"] for r in rows if r["state"] == "needs_trials")
    toks = [r["tokens"] for r in rows if r["tokens"] is not None]
    over = sorted(r["id"] for r in rows if budget is not None and any("over budget" in f for f in r["failing"]))
    bill = {"median": round(statistics.median(toks)) if toks else None, "max": max(toks) if toks else None,
            "total": sum(toks) if toks else None, "budget": budget, "over_budget": over, "field": token_field}

    band = "below" if pass_rate < TARGET[0] else "above" if pass_rate > TARGET[1] else "in"
    notes = []
    if n:
        notes.append(f"{n} scored cases: one case moves the rate {100 / n:.1f} points; "
                     "do not call a smaller change a win")
    if band == "above":
        notes.append("pass rate above 90%: the suite may be too easy to notice a real change")
    if band == "below":
        notes.append("pass rate below 70%: fix the loop or the cases before trusting a trend")
    if len(trials) < NEW_TRIALS:
        notes.append(f"{len(trials)} trial(s): new cases need {NEW_TRIALS}, critical cases {CRITICAL_TRIALS}")
    if fixed and broke:
        notes.append(f"fixed {len(fixed)}, broke {len(broke)}: a trade-off, not a win")
    if clear_loss and not repeated_loss:
        notes.append(f"clear loss (net {net} worse): blocks if the next comparison is a clear loss too")
    if not toks:
        notes.append("no token usage found: save traces to print the token bill")

    if critical or golden_broke or repeated_loss:
        verdict, code = "blocked", 1
    elif pending or needs:
        verdict, code = "pending", 2
    else:
        verdict, code = "pass", 0
    return {"verdict": verdict, "exit": code, "trials": len(trials), "pass_rate": pass_rate,
            "noise_band": noise, "band": band, "target": TARGET,
            "baseline_pass_rate": (baseline or {}).get("pass_rate"),
            "fixed": fixed, "broke": broke, "net_worse": net, "clear_loss": clear_loss,
            "clear_loss_threshold": threshold, "repeated_loss": repeated_loss,
            "critical_failed": critical, "golden_broke": golden_broke, "needs_trials": needs,
            "tokens": bill, "mix": mix(cases), "notes": notes, "pending": pending, "cases": rows}


# ---------- output ----------

def pct(x):
    return "–" if x is None else f"{x:.0%}"


def to_markdown(s, suite, run_dir):
    lines = [f"# Scorecard — {Path(run_dir).name}", "",
             f"Suite: `{suite}` · Verdict: **{s['verdict']}** · {s['trials']} trial(s) · "
             f"Pass rate {pct(s['pass_rate'])} (target {pct(TARGET[0])}–{pct(TARGET[1])}, {s['band']})"
             + (f" · Noise {pct(s['noise_band'])}" if s["noise_band"] is not None else ""), ""]
    if s["baseline_pass_rate"] is not None:
        lines.append(f"**Against the baseline (same cases):** fixed {len(s['fixed'])}, broke {len(s['broke'])}, "
                     f"net {s['net_worse']:+d} worse"
                     + (" — **repeated clear loss: blocked**" if s["repeated_loss"] else "")
                     + (f". Fixed: {', '.join(s['fixed'])}." if s["fixed"] else "")
                     + (f" Broke: {', '.join(s['broke'])}." if s["broke"] else ""))
    t = s["tokens"]
    if t["median"] is not None:
        lines.append(f"**Token bill ({t['field']}):** median {t['median']:,} per case, max {t['max']:,}, total {t['total']:,}"
                     + (f"; budget {t['budget']:,}, {len(t['over_budget'])} over" if t["budget"] else ""))
    for label, key in (("Critical failures", "critical_failed"), ("Golden cases broken", "golden_broke"),
                       ("Need more trials", "needs_trials"), ("Over token budget", None)):
        items = s[key] if key else t["over_budget"]
        if items:
            lines.append(f"**{label}:** {', '.join(items)}")
    lines.append("")
    lines += [f"- {x}" for x in s["notes"] + s["mix"]["notes"]]
    lines += ["", "| Case | Tier | Intent | State | Passes | Tokens | Failing |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for r in s["cases"]:
        lines.append(f"| {r['id']} | {r['tier']} | {r['intent'] or ''} | {r['state']} | {r['passes']}/{r['trials']} | "
                     f"{'' if r['tokens'] is None else format(r['tokens'], ',')} | "
                     f"{'; '.join(r['failing'])[:300].replace('|', '/')} |")
    if s["pending"]:
        lines += ["", "## Pending judge checks", "",
                  'Write verdicts to each trial\'s `judgments.json`: `{"<key>": {"pass": true, "why": "...", "by": "agent"}}`. '
                  'Author-tier keys need `"by": "author"`.', ""]
        lines += [f"- `{p['key']}` ({p['tier']}): {p['detail']}" for p in s["pending"][:60]]
    return "\n".join(lines) + "\n"


def hidden_view(s, tuned_path):
    """Aggregates only: no case ids, prompts, checks or outputs reach the tuning agent."""
    out = {"verdict": s["verdict"], "trials": s["trials"], "cases_scored": sum(r["state"] in ("pass", "fail", "flaky") for r in s["cases"]),
           "pass_rate": s["pass_rate"], "noise_band": s["noise_band"], "pending": len(s["pending"]),
           "needs_trials": len(s["needs_trials"]), "token_median": s["tokens"]["median"]}
    if tuned_path:
        tuned = json.loads(Path(tuned_path).read_text(encoding="utf-8"))
        gap = round(tuned["pass_rate"] - s["pass_rate"], 4)
        limit = max(0.15, 2 * (tuned.get("noise_band") or 0))
        out.update({"tuned_pass_rate": tuned["pass_rate"], "gap": gap, "overfit_limit": limit,
                    "overfitted": gap > limit})
        if gap > limit:
            out["verdict"], out["exit"] = "overfitted", 1
    out.setdefault("exit", s["exit"])
    return out


def expect_fail_view(cases, trial):
    """Known-bad set: every entry must fail. A pass means the check or judge cannot be trusted yet."""
    rows = []
    for r in trial:
        caught = r["status"] == "fail"
        rows.append({"id": r["id"], "status": "caught" if caught else "pending" if r["status"] == "pending" else "MISSED",
                     "why_bad": r["case"].get("why", ""),
                     "evidence": [f"{c['type']}: {c['detail']}" for c in r["checks"] if c["status"] == "fail"][:3]})
    missed = [r["id"] for r in rows if r["status"] == "MISSED"]
    pending = [r["id"] for r in rows if r["status"] == "pending"]
    code = 1 if missed else 2 if pending else 0
    return {"verdict": "untrusted" if missed else "pending" if pending else "trusted",
            "exit": code, "caught": sum(r["status"] == "caught" for r in rows), "total": len(rows),
            "missed": missed, "pending": pending, "rows": rows}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("suite")
    ap.add_argument("run_dir", nargs="?")
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--repeat", action="append", default=[])
    ap.add_argument("--baseline")
    ap.add_argument("--save-baseline", action="store_true")
    ap.add_argument("--previous")
    ap.add_argument("--token-budget", type=int)
    ap.add_argument("--token-field", default="total", choices=("total", "output", "input", "input+output"))
    ap.add_argument("--hidden", action="store_true")
    ap.add_argument("--tuned")
    ap.add_argument("--expect-fail", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args(argv)

    if not Path(a.suite).is_file():
        print(f"error: no suite file at {a.suite}", file=sys.stderr)
        return 2
    cases, errors = load_suite(a.suite)
    if errors:
        print("error: suite is not usable:\n  " + "\n  ".join(errors), file=sys.stderr)
        return 2
    if a.validate:
        m = mix(cases)
        print(f"{len(cases)} cases: " + ", ".join(f"{t} {m['counts'][t]} ({m['shares'][t]:.0%}, target {TIERS[t]:.0%})" for t in TIERS))
        for skill, got in sorted(m["intents"].items()):
            print(f"{skill}: intents {', '.join(got) or 'none'}")
        for note in m["notes"]:
            print(f"- {note}")
        return 0
    if a.run_dir is None:
        print("error: give a trial folder, or --validate", file=sys.stderr)
        return 2
    for d in [a.run_dir, *a.repeat, a.previous]:
        if d is not None and not Path(d).is_dir():
            print(f"error: {d} is not a folder", file=sys.stderr)
            return 2

    if a.expect_fail:
        v = expect_fail_view(cases, score_trial(cases, a.run_dir, a.previous, a.token_budget, a.token_field))
        print(json.dumps(v, indent=2))
        print(f"\nknown-bad caught {v['caught']} of {v['total']}: {v['verdict']}"
              + (f"; missed {', '.join(v['missed'])}" if v["missed"] else ""), file=sys.stderr)
        if a.out:
            Path(a.out + ".json").write_text(json.dumps(v, indent=2), encoding="utf-8")
        return v["exit"]

    baseline = {}
    if a.baseline and Path(a.baseline).exists():
        baseline = json.loads(Path(a.baseline).read_text(encoding="utf-8"))
    ab_log = str(Path(a.baseline).with_name("ab-log.jsonl")) if a.baseline else None
    trials = [score_trial(cases, d, a.previous, a.token_budget, a.token_field) for d in [a.run_dir, *a.repeat]]
    s = summarize(cases, trials, baseline, a.token_budget, ab_log, a.token_field)

    if a.hidden:
        h = hidden_view(s, a.tuned)
        print(json.dumps(h, indent=2))
        if a.out:
            Path(a.out + ".json").write_text(json.dumps(h, indent=2), encoding="utf-8")
        return h["exit"]

    md = to_markdown(s, a.suite, a.run_dir)
    if a.out:
        Path(a.out + ".json").write_text(json.dumps(s, indent=2, default=str), encoding="utf-8")
        Path(a.out + ".md").write_text(md, encoding="utf-8")
    print(md, end="")
    if baseline and ab_log:
        with open(ab_log, "a", encoding="utf-8") as f:
            f.write(json.dumps({"run": str(a.run_dir), "fixed": len(s["fixed"]), "broke": len(s["broke"]),
                                "net_worse": s["net_worse"], "clear_loss": s["clear_loss"],
                                "pass_rate": s["pass_rate"], "token_median": s["tokens"]["median"]}) + "\n")
    if a.save_baseline:
        if not a.baseline:
            print("error: --save-baseline needs --baseline PATH", file=sys.stderr)
            return 2
        if s["verdict"] != "pass":
            print("refused: baseline not saved because the verdict is not pass", file=sys.stderr)
        else:
            Path(a.baseline).write_text(json.dumps(
                {"pass_rate": s["pass_rate"], "noise_band": s["noise_band"], "trials": s["trials"],
                 "token_median": s["tokens"]["median"],
                 "cases": {r["id"]: {"rate": r["rate"], "trials": r["trials"]} for r in s["cases"]}},
                indent=2), encoding="utf-8")
            print(f"baseline saved: {a.baseline}")
    return s["exit"]


if __name__ == "__main__":
    sys.exit(main())

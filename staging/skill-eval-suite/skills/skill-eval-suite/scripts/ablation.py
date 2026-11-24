#!/usr/bin/env python3
"""Ablation: does the skill (or a part of it) earn its tokens? Blind pairwise comparison.

Usage:
  python ablation.py pair ARM_A ARM_B --out PAIRS_DIR [--prompts prompts.jsonl] [--seed N]
  python ablation.py score PAIRS_DIR [--noise NOISE_PAIRS_DIR] [--arm-a ARM_A --arm-b ARM_B]

ARM_A / ARM_B  one output per case (<id>.txt|.md|.json, or <id>.trace.jsonl whose final text is used):
               A is the run with the skill, B without it (or with part of it removed).
pair           writes PAIRS_DIR/<id>.md with "Answer 1" and "Answer 2" in random order and nothing
               that names an arm. The unblinding key goes to PAIRS_DIR.key.json, outside the folder,
               so a judge given only PAIRS_DIR cannot read it. The judge writes PAIRS_DIR/verdicts.json
               as {"<id>": "1" | "2" | "tie"}.
score          unblinds, gives A's win share with a 95% Wilson interval and, with --noise (the same
               procedure run on two identical arms, A vs A), the noise band: how far two identical
               runs differ from 50%. With --arm-a/--arm-b it also compares tool calls, tool errors and
               duration from the traces.

Standard library only.
"""
import argparse
import importlib.util
import json
import math
import random
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location("traces", Path(__file__).resolve().parent / "traces.py")
traces = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(traces)

OUTPUT_EXTS = (".txt", ".md", ".json", ".out", ".html", ".diff", ".patch")


def outputs(arm):
    found = {}
    for p in sorted(Path(arm).iterdir()):
        if p.name.endswith(".trace.jsonl"):
            cid = p.name[: -len(".trace.jsonl")]
            if cid not in found:
                found[cid] = (traces.load(p, raw=True).get("final_text") or "")
        elif p.suffix in OUTPUT_EXTS and p.name != "judgments.json":
            found[p.stem] = p.read_text(encoding="utf-8", errors="replace")
    return found


def pair(a, b, out, prompts_path, seed):
    A, B = outputs(a), outputs(b)
    ids = sorted(set(A) & set(B))
    if not ids:
        print("error: the two arms share no case ids", file=sys.stderr)
        return 2
    prompts = {}
    if prompts_path:
        for line in Path(prompts_path).read_text(encoding="utf-8").splitlines():
            if line.strip():
                c = json.loads(line)
                prompts[c["id"]] = c.get("prompt", "")
    rng = random.Random(seed)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    key = {}
    for cid in ids:
        flip = rng.random() < 0.5
        first, second = (B[cid], A[cid]) if flip else (A[cid], B[cid])
        key[cid] = {"1": "B" if flip else "A", "2": "A" if flip else "B"}
        body = [f"# Case {cid}", ""]
        if cid in prompts:
            body += ["## Request", "", prompts[cid], ""]
        body += ["## Answer 1", "", first.strip(), "", "## Answer 2", "", second.strip(), ""]
        (out / f"{cid}.md").write_text("\n".join(body), encoding="utf-8")
    Path(str(out).rstrip("/") + ".key.json").write_text(json.dumps(key, indent=2), encoding="utf-8")
    (out / "JUDGE.md").write_text(
        "Judge each case file blind. For each, decide which answer better does what the request asks:\n"
        "correct, complete, no invented facts, then concise. Write verdicts.json in this folder as\n"
        '{"<case id>": "1" | "2" | "tie"}. Do not look for or open any key file.\n', encoding="utf-8")
    missing = sorted((set(A) | set(B)) - set(ids))
    print(f"{len(ids)} pairs written to {out}" + (f"; {len(missing)} cases in only one arm skipped" if missing else ""))
    return 0


def wilson(wins, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = wins / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(max(0.0, c - h), 4), round(min(1.0, c + h), 4))


def tally(pairs_dir):
    pairs_dir = Path(pairs_dir)
    key = json.loads(Path(str(pairs_dir).rstrip("/") + ".key.json").read_text(encoding="utf-8"))
    verdicts = json.loads((pairs_dir / "verdicts.json").read_text(encoding="utf-8"))
    a = b = tie = 0
    unjudged = []
    for cid, k in key.items():
        v = str(verdicts.get(cid, "")).strip().lower()
        if v == "tie":
            tie += 1
        elif v in ("1", "2"):
            if k[v] == "A":
                a += 1
            else:
                b += 1
        else:
            unjudged.append(cid)
    n = a + b + tie
    share = round((a + 0.5 * tie) / n, 4) if n else None
    return {"a_wins": a, "b_wins": b, "ties": tie, "n": n, "a_share": share,
            "ci95": wilson(a + 0.5 * tie, n), "unjudged": unjudged}


def trace_stats(arm):
    rows = []
    for p in Path(arm).glob("*.trace.jsonl"):
        tr = traces.load(p, raw=True)
        rows.append((len(tr.get("calls", [])), tr.get("tool_errors", 0), tr.get("duration_ms")))
    if not rows:
        return None
    mean = lambda xs: round(sum(xs) / len(xs), 2) if xs else None
    return {"runs": len(rows), "tool_calls": mean([r[0] for r in rows]),
            "tool_errors": mean([r[1] for r in rows]),
            "duration_ms": mean([r[2] for r in rows if r[2] is not None])}


def score(pairs_dir, noise_dir, arm_a, arm_b):
    t = tally(pairs_dir)
    if t["n"] == 0:
        print("error: no verdicts yet; the judge writes verdicts.json in the pairs folder", file=sys.stderr)
        return 2
    noise = None
    if noise_dir:
        nt = tally(noise_dir)
        noise = round(abs(nt["a_share"] - 0.5), 4) if nt["a_share"] is not None else None
    lo, hi = t["ci95"]
    band = noise or 0.0
    if lo > 0.5 and t["a_share"] > 0.5 + band:
        verdict = "helps"
    elif hi < 0.5 and t["a_share"] < 0.5 - band:
        verdict = "hurts"
    else:
        verdict = "no clear difference"
    result = {**t, "noise_band": noise, "verdict": verdict,
              "arm_a": trace_stats(arm_a) if arm_a else None, "arm_b": trace_stats(arm_b) if arm_b else None}
    print(json.dumps(result, indent=2))
    print(f"\nA (with) won {t['a_share']:.0%} of {t['n']} blind comparisons, 95% CI {lo:.0%}–{hi:.0%}"
          + (f", noise band ±{noise:.0%}" if noise is not None else ", no noise band (run --noise)")
          + f": {verdict}.", file=sys.stderr)
    if t["unjudged"]:
        print(f"unjudged: {', '.join(t['unjudged'])}", file=sys.stderr)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pair"); p.add_argument("arm_a"); p.add_argument("arm_b")
    p.add_argument("--out", required=True); p.add_argument("--prompts"); p.add_argument("--seed", type=int)
    s = sub.add_parser("score"); s.add_argument("pairs"); s.add_argument("--noise")
    s.add_argument("--arm-a"); s.add_argument("--arm-b")
    a = ap.parse_args(argv)
    if a.cmd == "pair":
        for d in (a.arm_a, a.arm_b):
            if not Path(d).is_dir():
                print(f"error: {d} is not a folder", file=sys.stderr)
                return 2
        return pair(a.arm_a, a.arm_b, a.out, a.prompts, a.seed)
    if not Path(str(a.pairs).rstrip("/") + ".key.json").exists() or not (Path(a.pairs) / "verdicts.json").exists():
        print("error: need the pairs folder's key file and verdicts.json", file=sys.stderr)
        return 2
    return score(a.pairs, a.noise, a.arm_a, a.arm_b)


if __name__ == "__main__":
    sys.exit(main())

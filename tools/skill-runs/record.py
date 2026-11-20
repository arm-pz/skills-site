"""Record real-world runs on the site and list what each skill needs fixed.

    python tools/skill-runs/record.py            # write run evidence into site/skills.json + SUMMARY.md
    python tools/skill-runs/record.py --dry-run  # show what would change

Record the latest verdict and the latest passing example independently. The summary
lists the latest verdict for each skill and the defects attributed to the skill.
Regenerate the pages afterwards with gen_page.py --write.
"""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "reports" / "runs"
EVIDENCE = "https://github.com/arm-pz/skills-site/blob/main/"


def latest():
    runs, passes = {}, {}
    for f in sorted(RUNS.glob("*/*/verdict.json")):
        v = json.loads(f.read_text(encoding="utf-8"))
        # The report date survives a fresh checkout, unlike the transcript's mtime.
        v["ran"] = v["date"]
        v["dir"] = f.parent.relative_to(ROOT).as_posix()
        name = v["skill"]
        if name not in runs or v["ran"] >= runs[name]["ran"]:
            runs[name] = v
        if v["verdict"] == "PASS" and (name not in passes or v["ran"] >= passes[name]["ran"]):
            passes[name] = v
    return runs, passes


def rejected_evidence():
    """Evidence URLs of every run whose current verdict is not PASS, newest or not."""
    out = set()
    for f in RUNS.glob("*/*/verdict.json"):
        v = json.loads(f.read_text(encoding="utf-8"))
        if v["verdict"] != "PASS":
            out.add(EVIDENCE + f.parent.relative_to(ROOT).as_posix() + "/README.md")
    return out


def result_line(summary, limit=230):
    s = " ".join(summary.split())
    return s if len(s) <= limit else s[: s.rfind(" ", 0, limit)].rstrip(",;") + "…"


def evidence_for(run):
    return {"date": run["ran"], "target": run["target"], "result": result_line(run["summary"]),
            "evidence": EVIDENCE + run["dir"] + "/README.md"}


def record_entry(entry, run, passing, rejected=frozenset()):
    changed = False
    if run:
        latest_run = dict(evidence_for(run), verdict=run["verdict"])
        if entry.get("latestRun") != latest_run:
            entry["latestRun"] = latest_run
            changed = True
    old_pass = entry.get("tested")
    # A recorded pass whose report was later re-judged is no longer a passing example,
    # whether or not that report is still the newest run.
    if old_pass and (old_pass["evidence"] in rejected or (
            run and run["verdict"] != "PASS" and old_pass["evidence"] == latest_run["evidence"])):
        del entry["tested"]
        old_pass = None
        changed = True
    if passing and (not old_pass or passing["ran"] >= old_pass["date"]):
        new_pass = evidence_for(passing)
        if old_pass != new_pass:
            entry["tested"] = new_pass
            changed = True
    if changed and "tested" not in entry:
        entry.pop("featured", None)
    return changed


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    runs, passes = latest()
    rejected = rejected_evidence()
    path = ROOT / "site" / "skills.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    changed = []
    for s in manifest["skills"]:
        if record_entry(s, runs.get(s["name"]), passes.get(s["name"]), rejected):
            changed.append(s["name"])
    order = {"PASS": 0, "PARTIAL": 1, "FAIL": 2}
    rows = sorted(runs.values(), key=lambda v: (order.get(v["verdict"], 3), v["skill"]))
    counts = {k: sum(v["verdict"] == k for v in rows) for k in order}
    lines = ["# Real-world runs: summary", "",
             f"{len(rows)} skills and mods run: {counts['PASS']} PASS, {counts['PARTIAL']} PARTIAL, {counts['FAIL']} FAIL. "
             "Each row links to the full evidence.", "",
             "| Verdict | Skill | Report date | Result |", "|---|---|---|---|"]
    for v in rows:
        lines.append(f"| {v['verdict']} | [{v['skill']}]({Path(v['dir']).relative_to('reports/runs').as_posix()}/README.md) "
                     f"| {v['ran']} | {result_line(v['summary'], 300).replace('|', '/')} |")
    lines += ["", "## Fix list for tune-skill and the polish skills", "",
              "Defects the judge attributed to the skill itself (not to the run's environment), newest run per skill.", ""]
    for v in rows:
        if v["verdict"] != "PASS" and v.get("skill_defects"):
            lines.append(f"### {v['skill']} ({v['verdict']})")
            lines += [f"- {d}" for d in v["skill_defects"]] + [""]
    summary = "\n".join(lines) + "\n"
    if a.dry_run:
        print("would record:", ", ".join(changed) or "nothing")
        print(summary)
        return 0
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (RUNS / "SUMMARY.md").write_text(summary, encoding="utf-8")
    print("recorded:", ", ".join(changed) or "nothing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Record real-world runs on the site and list what each skill needs fixed.

    python tools/skill-runs/record.py            # write PASS runs into site/skills.json + SUMMARY.md
    python tools/skill-runs/record.py --dry-run  # show what would change

For each skill, the newest verdict under reports/runs/*/<skill>/ counts. A PASS becomes the page's
"Last real-world run" (the tested field), linked to that run's evidence; an existing tested entry is
replaced only by a newer PASS. PARTIAL and FAIL runs are never shown as working: they go into
reports/runs/SUMMARY.md with the defects the judge attributed to the skill, as the fix list for
tune-skill and the polish skills. Regenerate the pages afterwards with gen_page.py --write.
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "reports" / "runs"
EVIDENCE = "https://github.com/arm-pz/skills-site/blob/main/"


def latest():
    out = {}
    for f in sorted(RUNS.glob("*/*/verdict.json")):
        v = json.loads(f.read_text())
        # The day the run actually happened (a folder can hold runs that crossed midnight).
        v["ran"] = datetime.fromtimestamp((f.parent / "transcript.jsonl").stat().st_mtime, timezone.utc).date().isoformat()
        v["dir"] = f.parent.relative_to(ROOT).as_posix()
        if v["skill"] not in out or v["ran"] >= out[v["skill"]]["ran"]:
            out[v["skill"]] = v
    return out


def result_line(summary, limit=230):
    s = " ".join(summary.split())
    return s if len(s) <= limit else s[: s.rfind(" ", 0, limit)].rstrip(",;") + "…"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    runs = latest()
    path = ROOT / "site" / "skills.json"
    manifest = json.loads(path.read_text())
    changed = []
    for s in manifest["skills"]:
        v = runs.get(s["name"])
        if not v or v["verdict"] != "PASS":
            continue
        old = s.get("tested")
        if old and old["date"] > v["ran"]:
            continue
        s["tested"] = {"date": v["ran"], "target": v["target"], "result": result_line(v["summary"]),
                       "evidence": EVIDENCE + v["dir"] + "/README.md"}
        changed.append(s["name"])
    order = {"PASS": 0, "PARTIAL": 1, "FAIL": 2}
    rows = sorted(runs.values(), key=lambda v: (order.get(v["verdict"], 3), v["skill"]))
    counts = {k: sum(v["verdict"] == k for v in rows) for k in order}
    lines = ["# Real-world runs: summary", "",
             f"{len(rows)} skills and mods run: {counts['PASS']} PASS, {counts['PARTIAL']} PARTIAL, {counts['FAIL']} FAIL. "
             "Only PASS runs are shown on the site. Each row links to the full evidence.", "",
             "| Verdict | Skill | Ran | Result |", "|---|---|---|---|"]
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
    (RUNS / "SUMMARY.md").write_text(summary)
    print("recorded:", ", ".join(changed) or "nothing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

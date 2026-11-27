"""Compare the catalog router against the same Claude Code tasks without it."""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import run


ROUTER = "workflow-router"
BASE_SKILLS = ("draft-skill", "findable", "wordsmith")
CASES = {
    "publish-and-discover": {
        "prompt": ("I have an idea for a skill that drafts changelog entries. I want to make it installable "
                   "and help people find the published repo and docs. Which workflows should I follow?"),
        "workflows": ["build-a-skill", "get-found"],
        "skills": ["draft-skill", "tune-skill", "prompts-to-skill-release", "findable", "publish-pipeline"],
        "approvals": ["prompts-to-skill-release", "get-indexed"],
    },
    "publish-and-discover-paraphrase": {
        "prompt": ("I'd like to turn my weekly release-note checklist into a reusable agent skill. "
                   "Other developers should be able to install it and find it through search. Map the work in order."),
        "workflows": ["build-a-skill", "get-found"],
        "skills": ["draft-skill", "tune-skill", "prompts-to-skill-release", "findable", "publish-pipeline"],
        "approvals": ["prompts-to-skill-release", "get-indexed"],
    },
    "single-skill-near-miss": {
        "prompt": "Which single catalog skill should I use to tighten the wording of an existing README introduction?",
        "workflows": [],
        "skills": ["wordsmith"],
        "approvals": [],
    },
    "mixed-inventory": {
        "prompt": ("My skill and its GitHub repo already exist. I want people to find the repo by what it does, "
                   "get its associated site pages indexed, and check that its listings agree. Which workflow fits, "
                   "and which of its skills do I actually have in this project?"),
        "workflows": ["get-found"],
        "skills": ["findable", "publish-pipeline", "upstream-check", "get-indexed"],
        "approvals": ["get-indexed"],
    },
}
SCHEMA = {
    "type": "object",
    "properties": {
        "workflows": {"type": "array", "items": {"type": "string"}},
        "inventory": {"type": "array", "items": {
            "type": "object", "properties": {
                "skill": {"type": "string"},
                "status": {"type": "string", "enum": ["installed", "missing"]},
            },
            "required": ["skill", "status"], "additionalProperties": False,
        }},
        "approval_points": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["workflows", "inventory", "approval_points"],
    "additionalProperties": False,
}
OUTPUT_INSTRUCTIONS = (
    "Plan only. Do not perform any workflow steps or send anything. catalog.json is the local directory "
    "of available workflow and skill names. In the structured answer, put workflow slugs in execution order. "
    "For a task owned by a single skill, leave workflows empty. Report the recommended skills by name as "
    "installed or missing based on the project. List skills with steps that need explicit approval before "
    "public changes or submissions under approval_points."
)
TOOLS = ("Read", "Glob", "Grep", "Skill", "Bash")
ALLOW = (*TOOLS[:-1], "Bash(python .claude/skills/workflow-router/scripts/route_check.py *)",
         "Bash(python3 .claude/skills/workflow-router/scripts/route_check.py *)")


def score(case, answer, installed, activated, arm, known_skills):
    inventory = {item["skill"]: item["status"] for item in answer["inventory"]}
    expected_inventory = {name: "installed" if name in installed else "missing" for name in case["skills"]}
    return {
        "activation": activated == (arm == "router" and bool(case["workflows"])),
        "route": answer["workflows"] == case["workflows"],
        "inventory": (len(inventory) == len(answer["inventory"])
                      and inventory.keys() <= known_skills
                      and expected_inventory.items() <= inventory.items()
                      and all(status == ("installed" if name in installed else "missing")
                              for name, status in inventory.items())),
        "approvals": (set(case["approvals"]) <= set(answer["approval_points"])
                      and set(answer["approval_points"]) <= known_skills
                      and (bool(case["approvals"]) or not answer["approval_points"])),
    }


def router_activated(events):
    calls, completed = set(), set()
    for event in events:
        content = event.get("message", {}).get("content")
        if not isinstance(content, list):
            continue
        for item in content:
            if (item.get("type") == "tool_use" and item.get("name") == "Skill"
                    and item["input"].get("skill") in {ROUTER, f"caffeinity:{ROUTER}"}):
                calls.add(item["id"])
            if item.get("type") == "tool_result" and not item.get("is_error"):
                completed.add(item["tool_use_id"])
    return bool(calls & completed)


def trial_order(cases, repeats):
    for repeat in range(1, repeats + 1):
        for case in cases:
            arms = ("control", "router") if repeat % 2 else ("router", "control")
            yield from ((case, arm, repeat) for arm in arms)


def prepare_sources(names):
    manifest = run.manifest()
    sources = {name: run.source(name, manifest) for name in names}
    revisions = {name: subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
    ).strip() for name, path in sources.items()}
    return sources, revisions


def catalog():
    manifest = json.loads((run.ROOT / "site" / "skills.json").read_text(encoding="utf-8"))
    return {
        "workflows": [{"slug": flow["slug"], "title": flow["title"], "steps": [
            step["skills"] for step in flow["steps"]]} for flow in manifest["workflows"]],
        "skills": {entry["name"]: entry["blurb"] for entry in manifest["skills"] if entry["page"] != "none"},
    }


def trial(case_name, arm, repeat, model, budget, sources, directory, isolated_config):
    case = CASES[case_name]
    installed = set(BASE_SKILLS) | ({ROUTER} if arm == "router" else set())
    row = {"case": case_name, "arm": arm, "repeat": repeat, "installed": sorted(installed)}
    with tempfile.TemporaryDirectory(prefix="routing-eval-") as tmp:
        home = Path(tmp) / "home"
        home.mkdir()
        project = Path(tmp) / "project"
        project.mkdir()
        (project / "catalog.json").write_text(json.dumps(directory, ensure_ascii=False), encoding="utf-8")
        for name in sorted(installed):
            shutil.copytree(sources[name], project / ".claude" / "skills" / name,
                            ignore=shutil.ignore_patterns(".git"))
        env = run.child_env(home)
        for key in ("SystemRoot", "ComSpec", "TEMP", "TMP"):
            if key in os.environ:
                env[key] = os.environ[key]
        if not (isolated_config / ".credentials.json").is_file():
            for key in ("CLAUDE_CODE_OAUTH_TOKEN", "ANTHROPIC_API_KEY"):
                if os.environ.get(key):
                    env[key] = os.environ[key]
                    break
        env["USERPROFILE"] = str(home)
        env["CLAUDE_CONFIG_DIR"] = str(isolated_config)
        args = ["-p", case["prompt"] + "\n\n" + OUTPUT_INSTRUCTIONS, "--model", model,
                "--output-format", "stream-json", "--verbose", "--json-schema", json.dumps(SCHEMA),
                "--setting-sources", "project", "--strict-mcp-config", "--no-session-persistence",
                "--permission-mode", "dontAsk", "--tools", *TOOLS, "--allowedTools", *ALLOW,
                "--max-turns", "12", "--max-budget-usd", str(budget)]
        try:
            events, _, seconds = run.claude(args, project, env, timeout=180)
        except subprocess.TimeoutExpired:
            return dict(row, error="session timed out")
    result = run.final(events)
    if not result:
        return dict(row, error="Claude Code returned no result")
    row.update(cost_usd=result.get("total_cost_usd"), seconds=round(seconds, 2))
    answer = result.get("structured_output")
    message = result.get("result", "")
    if run.LIMIT.search(message):
        return dict(row, error="Claude Code usage limit")
    if "expired" in message.lower():
        return dict(row, error="Claude Code reported expired credentials")
    if result.get("is_error"):
        subtype = result.get("subtype", "")
        return dict(row, error=subtype if subtype.startswith("error_") else "Claude Code returned an error")
    if not isinstance(answer, dict) or not set(SCHEMA["required"]) <= answer.keys():
        return dict(row, error="Claude Code returned no structured answer")
    row["resolved_model"] = next((e.get("model") for e in events if e.get("subtype") == "init"), None)
    activated = router_activated(events)
    scores = score(case, answer, installed, activated, arm, directory["skills"].keys())
    return dict(row, activated=activated, answer=answer, scores=scores)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", action="append", choices=CASES, help="defaults to all four cases")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--model", default="sonnet")
    parser.add_argument("--budget-per-run", type=float, default=0.25)
    parser.add_argument("--list", action="store_true", help="print the matrix without calling Claude Code")
    parser.add_argument("--output", type=Path, help="new JSONL result file")
    args = parser.parse_args(argv)
    if args.repeats < 1 or not 0 < args.budget_per_run < float("inf"):
        parser.error("use positive repeats and a finite positive per-run budget")
    jobs = list(trial_order(dict.fromkeys(args.case or CASES), args.repeats))
    if args.list:
        for case, arm, repeat in jobs:
            print(f"{case} {arm} {repeat}")
        return 0
    if args.output is None or args.output.exists():
        parser.error("provide a path to a new --output file")
    config = Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude"))
    if not ((config / ".credentials.json").is_file()
            or os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")):
        parser.error("Claude Code credentials are unavailable for an isolated session")
    sources, revisions = prepare_sources((*BASE_SKILLS, ROUTER))
    directory = catalog()
    with (tempfile.TemporaryDirectory(prefix="routing-eval-auth-") as auth,
          args.output.open("x", encoding="utf-8") as output):
        isolated_config = Path(auth)
        credentials = config / ".credentials.json"
        if credentials.is_file():
            shutil.copyfile(credentials, isolated_config / credentials.name)
        metadata = {"type": "design", "model": args.model, "budget_per_run_usd": args.budget_per_run,
                    "planned_trials": len(jobs), "skill_revisions": revisions,
                    "claude_version": subprocess.check_output(["claude", "--version"], text=True).strip()}
        print(json.dumps(metadata), file=output, flush=True)
        for case, arm, repeat in jobs:
            row = trial(case, arm, repeat, args.model, args.budget_per_run, sources, directory, isolated_config)
            print(json.dumps(row), file=output, flush=True)
            print(f"{case} {arm} {repeat}: {row.get('error', row.get('scores'))}", flush=True)
            if "error" in row:
                print("Stopped after an incomplete trial. The result file contains the completed prefix.",
                      file=sys.stderr)
                return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

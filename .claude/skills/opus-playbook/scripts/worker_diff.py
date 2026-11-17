#!/usr/bin/env python3
"""Inventory what a delegated worker changed, for steps 2, 3 and 5 of the opus-playbook ladder.

    python scripts/worker_diff.py --base <ref> [--report report.md] [--repo <dir>]

--base    the commit the worker started from (default HEAD, which shows uncommitted work only)
--report  the worker's report saved as text; changed files it never names are listed
--repo    the repository to inspect (default: current directory)

Prints evidence, never a verdict. Exit 0 when the inventory ran, 2 when git could not be read.
It reads the repository and runs nothing from it.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

TEST_PATH = re.compile(
    r"(^|/)(tests?|__tests__|spec|specs|e2e|__snapshots__)/|(^|/)(test_[^/]*|conftest)\.py$"
    r"|[._-](test|spec)\.[a-z]+$|_test\.[a-z]+$|\.snap$", re.I)
CHECK_CONFIG = re.compile(
    r"(^|/)(\.github/workflows/|\.gitlab-ci\.yml$|\.circleci/|pytest\.ini$|tox\.ini$|setup\.cfg$"
    r"|jest\.config\.[a-z]+$|vitest\.config\.[a-z]+$|\.eslintrc[^/]*$|eslint\.config\.[a-z]+$"
    r"|\.pre-commit-config\.yaml$|\.coveragerc$)", re.I)

# (label, pattern, where it applies: "any", "test" or "code")
ADDED = [
    ("test skipped or narrowed", re.compile(
        r"@pytest\.mark\.(skip|skipif|xfail)|pytest\.skip\(|unittest\.skip|\b(it|test|describe)\.(skip|only|todo)\("
        r"|\bx(it|describe|test)\(|@Ignore\b|@Disabled\b|\bt\.Skip\("), "any"),
    ("check silenced", re.compile(
        r"#\s*noqa|#\s*type:\s*ignore|eslint-disable|@ts-ignore|@ts-expect-error|@ts-nocheck|#\s*pragma:\s*no cover"
        r"|\|\|\s*true\b|continue-on-error:\s*true"), "any"),
    ("unfinished marker", re.compile(r"\b(TODO|FIXME|HACK|XXX)\b|NotImplementedError|not implemented", re.I), "any"),
    ("failure swallowed", re.compile(
        r"except\s*:|except\s+(Exception|BaseException)\b[^:]*:\s*(pass)?\s*$|catch\s*(\([^)]*\))?\s*\{\s*\}"), "code"),
    ("stand-in outside tests", re.compile(r"\b(mock|stub|fake|dummy|placeholder|hardcoded?)\b", re.I), "code"),
]
ASSERTION = re.compile(r"\bassert\b|\bexpect\(|\bshould\b|\.assert[A-Z_a-z]*\(")


def git(repo, *args):
    done = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if done.returncode != 0:
        print(f"worker_diff: git {' '.join(args)} failed: {done.stderr.strip()}", file=sys.stderr)
        sys.exit(2)
    return done.stdout


def kind(path):
    if TEST_PATH.search(path):
        return "test"
    if CHECK_CONFIG.search(path):
        return "config"
    return "code"


def collect(repo, base):
    """Return {path: {"status", "added": [(lineno, text)], "removed": [text]}} against base."""
    files = {}
    for line in git(repo, "diff", "--name-status", "--no-renames", base).splitlines():
        status, _, path = line.partition("\t")
        files[path] = {"status": status, "added": [], "removed": []}
    current, lineno = None, 0
    for line in git(repo, "diff", "-U0", "--no-renames", "--no-color", base).splitlines():
        if line.startswith("diff --git"):
            current = None
        elif line.startswith("--- "):
            current = line[6:] if line.startswith("--- a/") else None
        elif line.startswith("+++ "):
            if line.startswith("+++ b/"):
                current = line[6:]
        elif line.startswith("@@"):
            found = re.search(r"\+(\d+)", line)
            lineno = int(found.group(1)) if found else 0
        elif current in files and line.startswith("+"):
            files[current]["added"].append((lineno, line[1:]))
            lineno += 1
        elif current in files and line.startswith("-"):
            files[current]["removed"].append(line[1:])
    for path in git(repo, "ls-files", "--others", "--exclude-standard").splitlines():
        try:
            text = (Path(repo) / path).read_text(encoding="utf-8", errors="replace")
        except OSError:
            text = ""
        files[path] = {"status": "new, untracked",
                       "added": list(enumerate(text.splitlines(), 1)), "removed": []}
    return files


def main():
    parser = argparse.ArgumentParser(description="Inventory a delegated worker's changes.")
    parser.add_argument("--base", default="HEAD")
    parser.add_argument("--report")
    parser.add_argument("--repo", default=".")
    args = parser.parse_args()

    files = collect(args.repo, args.base)
    names = {"A": "added", "M": "modified", "D": "deleted", "T": "type changed"}
    print(f"CHANGED against {args.base}: {len(files)} file(s)")
    for path in sorted(files):
        entry = files[path]
        status = names.get(entry["status"], entry["status"])
        print(f"  {status:<14} {path}  (+{len(entry['added'])} -{len(entry['removed'])})  [{kind(path)}]")

    if args.report:
        try:
            report = Path(args.report).read_text(encoding="utf-8", errors="replace")
        except OSError as err:
            print(f"worker_diff: cannot read report: {err}", file=sys.stderr)
            sys.exit(2)
        unmentioned = [p for p in sorted(files) if p not in report and Path(p).name not in report]
        print(f"\nUNMENTIONED in the report: {len(unmentioned)}")
        for path in unmentioned:
            print(f"  {path}")
    else:
        print("\nUNMENTIONED in the report: not checked (no --report given)")

    guarded = [p for p in sorted(files) if kind(p) != "code"]
    print(f"\nTESTS AND CHECK CONFIG touched: {len(guarded)}")
    for path in guarded:
        entry = files[path]
        if entry["status"] == "D":
            print(f"  {path}: deleted")
            continue
        gone = sum(1 for text in entry["removed"] if ASSERTION.search(text))
        new = sum(1 for _, text in entry["added"] if ASSERTION.search(text))
        note = "  <- fewer assertions than before" if gone > new else ""
        print(f"  {path}: assertion lines removed {gone}, added {new}{note}")

    hits = []
    for path in sorted(files):
        where = kind(path)
        for lineno, text in files[path]["added"]:
            for label, pattern, scope in ADDED:
                if scope == "code" and where != "code":
                    continue
                if pattern.search(text):
                    hits.append((path, lineno, label, text.strip()[:100]))
    print(f"\nADDED LINES to read first: {len(hits)}")
    for path, lineno, label, text in hits:
        print(f"  {path}:{lineno}  {label}: {text}")

    print("\nThis is an inventory. Read the diff, then run the checks yourself.")


if __name__ == "__main__":
    main()

"""Install the PR graph into a target checkout. Existing, differing files are never overwritten."""
import argparse
import shutil
import subprocess
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[2]
FILES = (
    ".claude/skills/pr-graph/SKILL.md",
    ".claude/skills/address-findings/SKILL.md",
    ".claude/agents/pr-reviewer.md",
    ".claude/agents/pr-fixer.md",
    "tools/pr-graph/merge_gate.py",
    "tools/pr-graph/schemas/review-report.schema.json",
    "tools/pr-graph/schemas/fix-report.schema.json",
    "tools/agent-skills/tests/test_merge_gate.py",
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path)
    args = parser.parse_args()
    target = Path(subprocess.check_output(
        ["git", "-C", str(args.checkout), "rev-parse", "--show-toplevel"], text=True).strip()).resolve()
    pending = []
    for name in FILES:
        dest = target / name
        if dest.resolve() != dest:
            parser.error(f"linked destination: {dest}")
        if dest.exists():
            if dest.read_text(encoding="utf-8") != (SOURCE / name).read_text(encoding="utf-8"):
                parser.error(f"existing file differs: {dest}")
        else:
            pending.append(name)
    for name in pending:
        dest = target / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOURCE / name, dest)
    print(f"Installed {len(pending)} files in {target}")


if __name__ == "__main__":
    main()

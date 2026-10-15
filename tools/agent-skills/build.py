"""Build the agent-skills discovery artifacts from the GitHub repos.

Downloads each repo's default-branch tarball, extracts the skill directory, and
writes a deterministic .tar.gz per skill plus the v0.2.0 discovery index.
"""

import gzip
import hashlib
import os
import io
import json
import subprocess
import tarfile

GH = os.environ.get("GH", "gh")  # Windows: point GH at the real gh.exe, not the npm shim
REPOS = {
    "wordsmith": "skills/wordsmith",
    "recruiter-lens": "skills/recruiter-lens",
    "job-lens": "skills/job-lens",
    "deep-tutor": "skills/deep-tutor",
    "do-better": "skills/do-better",
    "findable": "skills/findable",
    "keyword-guard": ".",
    "web-preflight": ".",
}
# Repo scaffolding that is not part of the skill itself; only applies to repos
# whose skill sits at the repository root.
REPO_META = {"README.md", "LICENSE", "LICENSE.md", "CHANGELOG.md", "CONTRIBUTING.md"}
REPO_META_DIRS = {".claude-plugin", ".github", ".git", "tests"}
OUT = os.environ.get("OUT", "out")
SITE = "https://skills.caffeinity.com"


def gh(*args):
    out = subprocess.run([GH, "api", *args], capture_output=True, check=True)
    return out.stdout


def skill_files(repo, base):
    tarball = gh(f"repos/arm-pz/{repo}/tarball")
    files = {}
    with tarfile.open(fileobj=io.BytesIO(tarball), mode="r:gz") as tf:
        root = next(iter({m.name.split("/")[0] for m in tf.getmembers()}))
        for m in tf.getmembers():
            if not m.isfile():
                continue
            rel = m.name[len(root) + 1:]
            if base == ".":
                top = rel.split("/")[0]
                if top in REPO_META or top in REPO_META_DIRS:
                    continue
            elif not rel.startswith(base + "/"):
                continue
            else:
                rel = rel[len(base) + 1:]
            files[rel] = tf.extractfile(m).read()
    return files


def pack(files):
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w") as tf:
        for name in sorted(files):
            info = tarfile.TarInfo(name)
            info.size = len(files[name])
            info.mode = 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mtime = 0
            tf.addfile(info, io.BytesIO(files[name]))
    gz = io.BytesIO()
    with gzip.GzipFile(fileobj=gz, mode="wb", mtime=0, compresslevel=9) as g:
        g.write(raw.getvalue())
    return gz.getvalue()


def main():
    os.makedirs(OUT, exist_ok=True)
    entries = []
    for name, base in REPOS.items():
        files = skill_files(name, base)
        if "SKILL.md" not in files:
            raise SystemExit(f"{name}: no SKILL.md found under {base!r}")
        blob = pack(files)
        digest = "sha256:" + hashlib.sha256(blob).hexdigest()
        with open(os.path.join(OUT, f"{name}.tar.gz"), "wb") as fh:
            fh.write(blob)
        description = json.loads(
            gh(f"repos/arm-pz/{name}").decode("utf-8")
        )["description"]
        entries.append(
            {
                "name": name,
                "description": description,
                "type": "archive",
                "url": f"{SITE}/agent-skills/{name}.tar.gz",
                "digest": digest,
            }
        )
        print(f"{name:<15} files={len(files):<3} tar={len(blob):>6}B  {digest[7:19]}…")
        for f in sorted(files):
            print(f"                  {f} ({len(files[f])}B)")

    index = {"$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
             "skills": sorted(entries, key=lambda e: e["name"])}
    with open(os.path.join(OUT, "index.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(index, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"\nindex.json: {len(index['skills'])} skills, "
          f"{len(json.dumps(index))} bytes")


if __name__ == "__main__":
    main()

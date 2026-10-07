"""Prepare a local gh-pages commit with a separate index; does not push or configure hosting."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts/github-pages"
OUTPUT = ARTIFACTS / "preview/imbolg_harmony_new"
BRANCH = "refs/heads/gh-pages"


def main():
    manifest = json.loads((ARTIFACTS / "build-manifest.json").read_text(encoding="utf-8"))
    verified = json.loads((ARTIFACTS / "local-verification.json").read_text(encoding="utf-8"))
    if verified.get("result") != "PASS" or verified.get("identity") != manifest["identity"]:
        raise ValueError("Build has no matching successful verification")
    expected = {item["path"]: item for item in manifest["files"]}
    actual = {p.relative_to(OUTPUT).as_posix() for p in OUTPUT.rglob("*") if p.is_file()}
    if set(expected) != actual:
        raise ValueError("The public file list changed since verification")
    env = dict(os.environ)
    env["GIT_INDEX_FILE"] = str(ARTIFACTS / ("deploy-index-" + uuid4().hex))
    command = ["git", "-c", "core.autocrlf=false", "--git-dir=" + str(ROOT / ".git"), "--work-tree=" + str(OUTPUT)]

    def git(*arguments, optional=False):
        result = subprocess.run(command + list(arguments), cwd=OUTPUT, env=env, capture_output=True)
        if result.returncode and not optional:
            raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
        return result.stdout.decode("utf-8").strip() if result.returncode == 0 else None

    object_format = git("rev-parse", "--show-object-format")
    objects = {}
    for name, item in expected.items():
        path = OUTPUT / name
        if path.is_symlink() or path.resolve() != path.absolute():
            raise ValueError("Linked public file")
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != item["sha256"] or len(data) != item["bytes"]:
            raise ValueError("Public file changed: " + name)
        objects[name] = hashlib.new(object_format, b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    source_commit = git("rev-parse", "HEAD")
    parent = git("rev-parse", "--verify", BRANCH, optional=True)
    git("read-tree", "--empty")
    git("add", "--all")
    staged = {}
    for record in git("ls-files", "--stage", "-z").rstrip("\0").split("\0"):
        metadata, name = record.split("\t", 1)
        mode, object_id, stage = metadata.split()
        if stage != "0" or mode != "100644":
            raise ValueError("Unexpected public Git file mode")
        staged[name] = object_id
    if staged != objects:
        raise ValueError("Staged Git bytes differ from the verified public bundle")
    tree = git("write-tree")
    arguments = ["commit-tree", tree, "-m", "Publish complete approved Imbolg Harmony site with inactive contact form"]
    if parent:
        arguments += ["-p", parent]
    commit = git(*arguments)
    git("update-ref", BRANCH, commit, parent or "0" * len(commit))
    receipt = {"prepared_utc": datetime.now(timezone.utc).isoformat(), "branch": "gh-pages", "commit": commit, "tree": tree, "parent": parent, "source_commit": source_commit, "identity": manifest["identity"], "files": len(objects), "bytes": manifest["bytes"], "pushed": False}
    (ARTIFACTS / "prepared-deployment.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt))


if __name__ == "__main__":
    main()

from __future__ import annotations

import hashlib
from pathlib import Path

from tech_agents.utils import has_path_traversal, is_within_repo_root


class FileOpsError(Exception):
    pass


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def assert_allowlisted_path(repo_root: Path, relative_path: str) -> None:
    if has_path_traversal(relative_path):
        raise FileOpsError(f"Disallowed path traversal: {relative_path}")
    candidate = (repo_root / relative_path)
    if not is_within_repo_root(repo_root, candidate):
        raise FileOpsError(f"Path escapes repo root: {relative_path}")


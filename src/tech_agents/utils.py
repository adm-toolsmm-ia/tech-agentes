from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any


def now_iso() -> str:
    # Avoid adding heavy deps; ISO-ish is enough for logs.
    import datetime as _dt

    return _dt.datetime.utcnow().replace(tzinfo=_dt.timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def write_bytes_if_missing(path: Path, content: bytes) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return True


def write_json_if_missing(path: Path, data: Any) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def sha256_text(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def is_within_repo_root(repo_root: Path, candidate: Path) -> bool:
    repo_root = repo_root.resolve()
    try:
        candidate.resolve().relative_to(repo_root)
        return True
    except Exception:
        return False


def has_path_traversal(path: str) -> bool:
    # Conservative check for file ops: disallow absolute paths and traversal.
    if os.path.isabs(path):
        return True
    norm = Path(path)
    return any(part in ("..",) for part in norm.parts)


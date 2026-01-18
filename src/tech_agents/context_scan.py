from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RepoScan:
    repo_root: Path
    project_type: str  # frontend|backend|ai_ml|devops|containers|unknown
    phase: str  # speed|balanced|quality
    is_multiagent: bool
    has_project_configs: bool
    has_project_standards: bool


def detect_project_type(repo_root: Path) -> str:
    if (repo_root / "package.json").exists():
        if (repo_root / "components").exists():
            return "frontend"
        if (repo_root / "routes").exists() or (repo_root / "api").exists():
            return "backend"
        return "unknown"
    if (repo_root / "requirements.txt").exists() or (repo_root / "pyproject.toml").exists():
        if (repo_root / "models").exists():
            return "ai_ml"
        return "unknown"
    if (repo_root / "terraform").exists() or (repo_root / "k8s").exists():
        return "devops"
    if (repo_root / "docker-compose.yml").exists():
        return "containers"
    return "unknown"


def detect_phase(repo_root: Path) -> str:
    # Minimal heuristic: folder names and common production branches if git exists.
    if (repo_root / "poc").exists():
        return "speed"
    # Avoid hard dependency on git; treat as balanced by default.
    return "balanced"


def scan_repo(repo_root: Path) -> RepoScan:
    repo_root = repo_root.resolve()
    is_multiagent = (repo_root / "agents").exists() and (repo_root / "workflows").exists()
    has_project_configs = (repo_root / "configs" / "projeto.json").exists()
    has_project_standards = (repo_root / "docs" / "padrões" / "padroes_projeto.md").exists()
    return RepoScan(
        repo_root=repo_root,
        project_type=detect_project_type(repo_root),
        phase=detect_phase(repo_root),
        is_multiagent=is_multiagent,
        has_project_configs=has_project_configs,
        has_project_standards=has_project_standards,
    )


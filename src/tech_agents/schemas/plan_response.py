from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

from tech_agents.schemas.common import ProjectRef, SLO


class AgentRosterItem(BaseModel):
    name: str
    type: Literal["base", "specialist"]
    mandate: str
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    handoff_to: list[str] = Field(default_factory=list)


class Recommendation(BaseModel):
    agent_name: str
    reason: str
    priority: Literal["high", "medium", "low"]
    expected_impact: str = ""
    dependencies: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)


class TaskItem(BaseModel):
    id: str
    assigned_to: str
    goal: str
    inputs: str = ""
    acceptance_criteria: list[str] = Field(default_factory=list)
    deliverable_format: str = ""
    deadline: str = ""


class FileOp(BaseModel):
    action: Literal["create", "update", "append"]
    path: str
    format: Literal["md", "json", "jsonl", "yaml"]
    content: str
    allowlisted: bool = True
    checksum: str = ""
    reason: str = ""


class PlanResponse(BaseModel):
    project: ProjectRef
    slo: SLO
    agent_roster: list[AgentRosterItem] = Field(default_factory=list)
    recommendations: list[Recommendation] = Field(default_factory=list)
    tasks: list[TaskItem] = Field(default_factory=list)
    security_findings: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    file_ops: list[FileOp] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)

    extra: dict[str, Any] = Field(default_factory=dict)


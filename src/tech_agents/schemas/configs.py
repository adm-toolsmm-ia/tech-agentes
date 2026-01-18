from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

from tech_agents.schemas.common import Environment, Instrumentation, SLO


class Budgets(BaseModel):
    run_usd: float = Field(default=0, ge=0)
    daily_usd: float = Field(default=0, ge=0)
    project_usd: float = Field(default=0, ge=0)


class ProjectConfig(BaseModel):
    name: str = Field(min_length=1)
    version: str = Field(default="0.1.0", min_length=1)
    owners: list[str] = Field(default_factory=list)
    environment: Environment = "dev"
    tenant_id: str = ""
    deadlines: dict[str, str] = Field(default_factory=dict)
    kpis: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    budgets: Budgets = Field(default_factory=Budgets)
    slo: SLO = Field(default_factory=SLO)
    instrumentation: Instrumentation = Field(default_factory=Instrumentation)


ModelClass = Literal["frontier", "intermediate", "light"]


class ModelRoutingRule(BaseModel):
    task_class: str
    preferred: list[str] = Field(default_factory=list)
    fallback: list[str] = Field(default_factory=list)
    max_temperature: float = Field(default=0.3, ge=0, le=2)


class ModelPolicy(BaseModel):
    version: str = Field(default="0.1.0", min_length=1)
    pricing_version: str = Field(default="unknown")
    thresholds: dict[str, Any] = Field(default_factory=dict)
    routing: list[ModelRoutingRule] = Field(default_factory=list)
    defaults: dict[str, Any] = Field(default_factory=dict)


class EnvSecretsRef(BaseModel):
    # Store only references (names/keys), never secrets.
    refs: dict[str, str] = Field(default_factory=dict)


class EnvironmentsConfig(BaseModel):
    version: str = Field(default="0.1.0", min_length=1)
    dev: EnvSecretsRef = Field(default_factory=EnvSecretsRef)
    stage: EnvSecretsRef = Field(default_factory=EnvSecretsRef)
    prod: EnvSecretsRef = Field(default_factory=EnvSecretsRef)


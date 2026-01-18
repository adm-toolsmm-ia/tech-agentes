from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


Environment = Literal["dev", "stage", "prod"]


class ProjectRef(BaseModel):
    name: str = Field(min_length=1)
    version: str = Field(default="0.1.0", min_length=1)
    context_hash: str = Field(default="")
    repo_root: str = Field(default="")
    environment: Environment = Field(default="dev")
    tenant_id: str = Field(default="")


class SLO(BaseModel):
    latency_s: int = Field(default=8, ge=1)
    critical_error_rate_max: float = Field(default=0.01, ge=0, le=1)
    daily_budget_usd: float = Field(default=0, ge=0)


class Instrumentation(BaseModel):
    provider: Literal["none", "langfuse", "helicone", "sdk"] = "none"
    enabled: bool = False
    notes: Optional[str] = None


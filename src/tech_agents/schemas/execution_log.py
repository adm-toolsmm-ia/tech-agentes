from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, model_validator

from tech_agents.schemas.common import Environment, Instrumentation


class ExecutionLog(BaseModel):
    timestamp: str
    run_id: str
    tenant_id: str
    agent: str
    reason_trigger: str
    input_summary: str
    operations: list[str] = Field(default_factory=list)

    instrumentation: Instrumentation = Field(default_factory=Instrumentation)

    model_used: Optional[str] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None

    context_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    latency_ms: Optional[int] = None
    cost_estimate_usd: Optional[float] = None
    pricing_version: Optional[str] = None

    errors: list[str] = Field(default_factory=list)
    outputs_checksum: str = ""
    next_handoff: str = ""
    environment: Environment = "dev"

    extra: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def enforce_no_uninstrumented_estimates(self) -> "ExecutionLog":
        if self.instrumentation.provider == "none" or self.instrumentation.enabled is False:
            # Forbidden to fill token/latency/cost fields as estimates.
            forbidden = {
                "context_tokens": self.context_tokens,
                "output_tokens": self.output_tokens,
                "latency_ms": self.latency_ms,
                "cost_estimate_usd": self.cost_estimate_usd,
            }
            filled = [k for k, v in forbidden.items() if v not in (None,)]
            if filled:
                raise ValueError(
                    f"Uninstrumented run cannot include estimates: {', '.join(filled)}"
                )
        return self


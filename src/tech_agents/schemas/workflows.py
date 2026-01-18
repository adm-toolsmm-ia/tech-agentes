from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


# --- Task-level components ---


class TaskTrigger(BaseModel):
    """Defines when/how a task is triggered."""

    type: Literal["manual", "event", "schedule"] = "manual"
    condition: str = ""
    inputs_required: list[str] = Field(default_factory=list)


class RetryConfig(BaseModel):
    """Retry configuration for error handling."""

    enabled: bool = True
    max_attempts: int = 3
    backoff: Literal["linear", "exponential"] = "linear"
    initial_delay_seconds: int = 30


class ErrorHandling(BaseModel):
    """Error handling configuration for a task."""

    on_failure: Literal["notify_and_pause", "notify_and_continue", "block_pipeline"] = (
        "notify_and_pause"
    )
    retry: RetryConfig = Field(default_factory=RetryConfig)
    fallback: str = ""


class Rollback(BaseModel):
    """Rollback configuration for a task."""

    enabled: bool = False
    procedure: str = ""
    auto: bool = False
    requires_approval: bool = False
    reason: str = ""


class Gate(BaseModel):
    """A gate/checkpoint that must pass before proceeding."""

    name: str
    condition: str
    blocking: bool = True
    message: str = ""


# --- Main task model ---


class WorkflowTask(BaseModel):
    """A task in the execution plan or backlog."""

    id: str
    assigned_to: str
    goal: str
    acceptance_criteria: list[str] = Field(default_factory=list)
    deliverable_format: str = ""
    deadline: str = ""

    # Extended fields for full workflow support
    trigger: Optional[TaskTrigger] = None
    error_handling: Optional[ErrorHandling] = None
    rollback: Optional[Rollback] = None
    gates: list[Gate] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)


# --- Plan-level components ---


class PlanMetadata(BaseModel):
    """Metadata for an execution plan."""

    created_at: str = ""
    updated_at: str = ""
    owner: str = ""
    description: str = ""


class GlobalConfig(BaseModel):
    """Global configuration for the execution plan."""

    max_retries: int = 3
    retry_delay_seconds: int = 30
    timeout_seconds: int = 300
    notification_channel: str = ""
    require_cto_approval_for: list[str] = Field(default_factory=list)


class PromotionRule(BaseModel):
    """Rules for promoting between environments."""

    required_gates: list[str] = Field(default_factory=list)
    approval_required: bool = False
    approvers: list[str] = Field(default_factory=list)
    evidence_required: list[str] = Field(default_factory=list)
    auto_promote: bool = False


class PromotionRules(BaseModel):
    """Promotion rules for different environment transitions."""

    dev_to_stage: PromotionRule = Field(default_factory=PromotionRule)
    stage_to_prod: PromotionRule = Field(default_factory=PromotionRule)


class Notifications(BaseModel):
    """Notification configuration for workflow events."""

    on_task_start: list[str] = Field(default_factory=list)
    on_task_complete: list[str] = Field(default_factory=list)
    on_task_failure: list[str] = Field(default_factory=list)
    on_gate_blocked: list[str] = Field(default_factory=list)
    on_promotion: list[str] = Field(default_factory=list)


# --- Main execution plan model ---


class ExecutionPlan(BaseModel):
    """Complete execution plan with tasks, gates, and promotion rules."""

    version: str = Field(default="0.1.0")
    environment: Literal["dev", "stage", "prod"] = "dev"

    # Extended metadata and configuration
    metadata: Optional[PlanMetadata] = None
    global_config: Optional[GlobalConfig] = None

    # Tasks and recommendations
    tasks: list[WorkflowTask] = Field(default_factory=list)
    recommendations: list[dict[str, Any]] = Field(default_factory=list)

    # Promotion and notification rules
    promotion_rules: Optional[PromotionRules] = None
    notifications: Optional[Notifications] = None


class Backlog(BaseModel):
    """Backlog of prioritized tasks."""

    version: str = Field(default="0.1.0")
    items: list[WorkflowTask] = Field(default_factory=list)

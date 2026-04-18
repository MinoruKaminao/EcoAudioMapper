from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ObservationSummary(BaseModel):
    id: UUID
    status: str
    visibility_level: str
    recorded_at_utc: datetime | None = None


class ObservationListResponse(BaseModel):
    items: list[ObservationSummary] = Field(default_factory=list)
    total: int = 0
    limit: int = 20
    offset: int = 0

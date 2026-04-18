from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid

from app.db.base import Base


class Observation(Base):
    __tablename__ = "observations"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    media_file_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    location_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    observation_datetime_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    source_type: Mapped[str] = mapped_column(String(length=50), nullable=False)
    quality_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 4), nullable=True)
    visibility_level: Mapped[str] = mapped_column(String(length=30), nullable=False)
    status: Mapped[str] = mapped_column(String(length=30), nullable=False)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    place_name: Mapped[str | None] = mapped_column(String(length=255), nullable=True)
    current_top_detection_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

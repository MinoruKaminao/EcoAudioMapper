from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models.observation import Observation
from app.db.session import get_db
from app.schemas.observation import ObservationListResponse, ObservationSummary


router = APIRouter(prefix="/observations", tags=["observations"])


@router.get(
    "",
    response_model=ObservationListResponse,
    status_code=status.HTTP_200_OK,
    summary="List observations (bootstrap skeleton)",
)
def list_observations(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> ObservationListResponse:
    total = db.scalar(
        select(func.count()).select_from(Observation).where(Observation.deleted_at.is_(None))
    )
    rows = db.scalars(
        select(Observation)
        .where(Observation.deleted_at.is_(None))
        .order_by(Observation.created_at.desc(), Observation.id.desc())
        .offset(offset)
        .limit(limit)
    ).all()

    items = [
        ObservationSummary(
            id=row.id,
            status=row.status,
            visibility_level=row.visibility_level,
            recorded_at_utc=None,
        )
        for row in rows
    ]

    return ObservationListResponse(
        items=items,
        total=total or 0,
        limit=limit,
        offset=offset,
    )

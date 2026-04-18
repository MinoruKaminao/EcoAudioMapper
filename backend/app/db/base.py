from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Shared declarative base for future ORM models."""


from app.db.models.observation import Observation  # noqa: E402,F401

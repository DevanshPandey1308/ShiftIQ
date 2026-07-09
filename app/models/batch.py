from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.database.database import Base
from sqlalchemy.orm import relationship


class Batch(Base):
    __tablename__ = "batches"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    dataset_id = Column(
        Integer,
        ForeignKey("datasets.id"),
        nullable=False
    )

    status = Column(
        String,
        default="Pending"
    )

    processing_started_at = Column(
        DateTime,
        nullable=True
    )

    processing_completed_at = Column(
        DateTime,
        nullable=True
    )

    health_score = Column(
        Float,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    dataset = relationship(
        "Dataset",
        back_populates="batches"
    )

    drift_report = relationship(
        "DriftReport",
        back_populates="batch",
        uselist=False
    )

    alerts = relationship(
        "Alert",
        back_populates="batch"
    )

    ai_insights = relationship(
        "AIInsight",
        back_populates="batch"
    )
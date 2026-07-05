from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    JSON
)

from sqlalchemy.orm import relationship

from app.database.database import Base


class DriftReport(Base):
    __tablename__ = "drift_reports"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    batch_id = Column(
        Integer,
        ForeignKey("batches.id"),
        nullable=False,
        unique=True
    )

    psi_results = Column(
        JSON,
        nullable=True
    )

    ks_results = Column(
        JSON,
        nullable=True
    )

    chi_square_results = Column(
        JSON,
        nullable=True
    )

    js_results = Column(
        JSON,
        nullable=True
    )

    health_score = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    batch = relationship(
        "Batch",
        back_populates="drift_report"
    )
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database.database import Base


class AIInsight(Base):
    __tablename__ = "ai_insights"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    batch_id = Column(
        Integer,
        ForeignKey("batches.id"),
        nullable=False
    )

    insight = Column(
        String,
        nullable=False
    )

    recommendation = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    batch = relationship(
        "Batch",
        back_populates="ai_insights"
    )
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


class MLModel(Base):
    __tablename__ = "ml_models"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    description = Column(
        String,
        nullable=True
    )

    problem_type = Column(
        String,
        nullable=False
    )

    target_column = Column(
        String,
        nullable=False
    )

    model_type = Column(
        String,
        nullable=False
    )

    version = Column(
        String,
        default="1.0.0"
    )

    environment = Column(
        String,
        default="Production"
    )

    status = Column(
        String,
        default="ACTIVE"
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    owner = relationship(
        "User",
        back_populates="ml_models"
    )

    datasets = relationship(
        "Dataset",
        back_populates="model",
        cascade="all, delete-orphan"
    )
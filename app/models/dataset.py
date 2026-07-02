from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship

from app.database.database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    file_path = Column(
        String,
        nullable=False
    )

    # Owner of the dataset
    # (Will later come from JWT authentication)
    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    # ML Model this dataset belongs to
    model_id = Column(
        Integer,
        ForeignKey("ml_models.id"),
        nullable=True
    )

    # BASELINE or BATCH
    dataset_type = Column(
        String,
        nullable=True
    )

    # Metadata generated after processing
    row_count = Column(
        Integer,
        nullable=True
    )

    column_count = Column(
        Integer,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    owner = relationship(
        "User",
        back_populates="datasets"
    )

    model = relationship(
        "MLModel",
        back_populates="datasets"
    )
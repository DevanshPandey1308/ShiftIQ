from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database.database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    file_path = Column(String, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"))

    # Metadata
    row_count = Column(Integer, nullable=True)
    column_count = Column(Integer, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    owner = relationship("User", backref="datasets")
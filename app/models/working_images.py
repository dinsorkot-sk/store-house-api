from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class WorkingImages(Base):
    __tablename__ = "working_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    working_id = Column(Integer, ForeignKey("working.id"), nullable=False, index=True)
    working_image_data = Column(Text, nullable=False)
    created_at = Column(
        DateTime, server_default=func.current_timestamp(), nullable=False
    )
    updated_at = Column(
        DateTime,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )
    deleted_at = Column(DateTime, index=True, nullable=True)

    __table_args__ = (
        Index("images_working_index", "working_id"),
        Index("working_index", "deleted_at"),
    )

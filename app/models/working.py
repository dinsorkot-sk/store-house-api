from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Working(Base):
    __tablename__ = "working"

    id = Column(Integer, primary_key=True, autoincrement=True)
    working_name = Column(Text, nullable=False)
    detail = Column(Text, nullable=True)
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

    __table_args__ = (Index("working_index", "deleted_at"),)

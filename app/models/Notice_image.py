from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class NoticeImage(Base):
    __tablename__ = "notice_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    notice_id = Column(Integer, ForeignKey('notices.id', ondelete='CASCADE'), nullable=False, index=True)
    image_path = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    uploaded_at = Column(DateTime, server_default=func.current_timestamp())
    deleted_at = Column(DateTime, index=True, nullable=True)

    # Relationship with notice
    # notice = relationship("Notice", back_populates="images")
    
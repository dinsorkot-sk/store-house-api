from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False, index=True)
    email = Column(String(255), index=True)
    location = Column(Text, nullable=False, index=True)
    size = Column(String(50))
    office_size = Column(String(50))
    details = Column(Text)
    preferred_contact_phone = Column(Boolean, default=False)
    preferred_contact_email = Column(Boolean, default=False)
    poster_type = Column(String(50))
    price = Column(DECIMAL)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(DateTime, index=True, nullable=True)

    # Relationship with notice_images
    images = relationship("NoticeImage", back_populates="notice", cascade="all, delete-orphan")

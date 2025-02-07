from sqlalchemy import Column, Integer, String, Text, DateTime, TIMESTAMP, text
from sqlalchemy.sql import func
from app.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    url = Column(Text, nullable=False)
    created_at = Column(
        DateTime, server_default=func.current_timestamp(), nullable=True
    )
    updated_at = Column(
        DateTime,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=True,
    )
    deleted_at = Column(DateTime, nullable=True)

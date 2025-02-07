from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Admin_User(Base):
    __tablename__ = "admin_users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(
        DateTime, server_default=func.current_timestamp(), nullable=True
    )
    updated_at = Column(
        DateTime,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=True,
    )
    deleted_at = Column(DateTime, nullable=True, index=True)

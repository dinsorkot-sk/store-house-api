from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP, text, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class ContactImage(Base):
    __tablename__ = "contact_images"

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(
        Integer,
        ForeignKey("contacts.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    image_path = Column(String(255), nullable=False)
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

    # contact = relationship("Contact", back_populates="images")

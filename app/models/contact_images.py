from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP, text, ForeignKey
from app.database import Base

class ContactImage(Base):
    __tablename__ = "contact_images"
    
    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id", ondelete="CASCADE"), nullable=False)
    image_path = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    uploaded_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    # contact = relationship("Contact", back_populates="images")
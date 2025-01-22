from sqlalchemy import Column, Integer, String, Text, DateTime, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    url = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    uploaded_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    deleted_at = Column(DateTime, nullable=True)

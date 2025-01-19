from sqlalchemy import Column, Integer, String, TIMESTAMP, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Inquirer(Base):
    __tablename__ = 'inquirers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    notice_id = Column(Integer, ForeignKey('notices.id', ondelete='CASCADE'), nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    detail = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')
    uploaded_at = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')
    deleted_at = Column(DateTime, nullable=True)

    notice = relationship('Notice', back_populates='inquirers')  # Assuming a 'Notice' model exists.

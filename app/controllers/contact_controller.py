from sqlalchemy.orm import Session

from datetime import datetime
from app.models.contacts import Contact
from app.schemas.contacts import ContactCreate , ContactUpdate ,  ContactResponse
from app.schemas.contact_images import ContactImageCreate , ContactImageUpdate
from fastapi import HTTPException, Request

def create_contact(db:Session , contact_create:ContactCreate):
    contact = Contact(**contact_create.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    
    # Add images if provided
    if contact_create.images:
        for image in contact_create.images:
            notice_image = ContactImageCreate(
                notice_id=contact.id,
                image_path=image.image_path,
            )
            db.add(notice_image)
        db.commit()
        
    return contact

def get_contact(db:Session , contact_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    return ContactResponse.from_orm(db_contact)

def get_contacts():
    return

def update_contact(db: Session, contact_id: int, contact_update: ContactUpdate):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    # Update the fields only if provided in the request
    for key, value in contact_update.dict(exclude_unset=True).items():
        setattr(contact, key, value)

    db.commit()
    db.refresh(contact)
    return ContactResponse.from_orm(contact)


def delete_contact(db: Session, contact_id: int):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    if contact:
        contact.deleted_at = datetime.utcnow()
        db.commit()
        db.refresh(contact)
        return contact
    return ContactResponse.from_orm(contact)
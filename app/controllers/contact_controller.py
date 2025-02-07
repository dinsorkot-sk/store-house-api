from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
from datetime import datetime
from app.models.contacts import Contact
from app.models.contact_images import ContactImage
from app.schemas.contacts import ContactCreate, ContactUpdate, ContactResponse , ContactInResponse
from app.schemas.contact_images import ContactImageCreate, ContactImageUpdate
from fastapi import HTTPException, Request

import base64


def decode_base64(data):
    # เพิ่ม padding หากขาด
    missing_padding = len(data) % 4
    if missing_padding:
        data += "=" * (4 - missing_padding)

    return base64.b64decode(data)


def create_contact(db: Session, contact_create: ContactCreate):
    contact_data = contact_create.dict(exclude={"images"})
    contact = Contact(**contact_data)

    db.add(contact)
    db.commit()
    db.refresh(contact)

    # Add images if provided
    if contact_create.images:
        for image in contact_create.images:

            file_image = decode_base64(image.image_path)

            contact_image = ContactImage(
                contact_id=contact.id,
                image_path=file_image,
            )
            db.add(contact_image)
        db.commit()

    return ContactInResponse.from_orm(contact)


def get_contact(db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    return ContactInResponse.from_orm(db_contact)


def get_contacts(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    keyword: str = None,
    order_contacts: str = "desc",
)-> ContactResponse:
    # Query สำหรับค้นหา Contact
    query = db.query(Contact)
    
     # เพิ่มเงื่อนไขการค้นหา หากมี keyword
    if keyword:
        query = query.filter(
            or_(
                Contact.title.ilike(f"%{keyword}%"),
            )
        )
    
    # จัดเรียงตามราคา (asc หรือ desc)
    if order_contacts == "asc":
        query = query.order_by(asc(Contact.updated_at))
    elif order_contacts == "desc":
        query = query.order_by(desc(Contact.updated_at))
        
    query = query.filter(Contact.deleted_at.is_(None))
    
    # ค้นหา Notice ทั้งหมดจากฐานข้อมูล
    contacts = query.offset(skip).limit(limit).all()
    
    # คำนวณจำนวนข้อมูลทั้งหมดในฐานข้อมูล
    total = query.count()

    # คำนวณจำนวนหน้า (total pages)
    total_pages = (total // limit) + (1 if total % limit > 0 else 0)

    # คำนวณหมายเลขหน้าปัจจุบัน
    current_page = (skip // limit) + 1

    # คำนวณ next และ prev page
    next_page = current_page + 1 if current_page < total_pages else None
    prev_page = current_page - 1 if current_page > 1 else None

    # สร้าง next_page_url และ prev_page_url โดยใช้ url_for และค่าพารามิเตอร์ที่เหมาะสม
    next_page_url = (
        f"api/notices/?skip={(next_page - 1) * limit}&limit={limit}"
        if next_page
        else None
    )
    prev_page_url = (
        f"api/notices/?skip={(prev_page - 1) * limit}&limit={limit}"
        if prev_page
        else None
    )

    if not contacts:
        raise HTTPException(status_code=404, detail="Contacts not found")

    # สร้าง response ที่มีข้อมูลต่างๆ
    return ContactResponse(
        total=total,
        total_pages=total_pages,
        current_page=current_page,
        next_page_url=next_page_url,
        prev_page_url=prev_page_url,
        contacts=[ContactInResponse.from_orm(contact) for contact in contacts],
    )
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
    return ContactInResponse.from_orm(contact)


def delete_contact(db: Session, contact_id: int):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    if contact:
        contact.deleted_at = datetime.utcnow()
        db.commit()
        db.refresh(contact)
        return contact
    return ContactInResponse.from_orm(contact)

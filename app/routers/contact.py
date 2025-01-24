from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.contacts import ContactCreate, ContactUpdate, ContactResponse
from app.database import SessionLocal
from app.controllers.contact_controller import (
    create_contact,
    update_contact,
    delete_contact,
    get_contact,
    get_contacts
)


def get_session_local():
    yield SessionLocal()


router = APIRouter(
    prefix="/api",
    tags=["api contacts"],
)


# สร้าง Contacts ใหม่
@router.post("/contacts/", response_model=ContactResponse)
def add_contact(inquirer: ContactCreate, db: Session = Depends(get_session_local)):
    return create_contact(db=db, inquirer=inquirer)


#  ดึงข้อมูล Contacts ทั้งหมด
@router.get("/contacts/", response_model=ContactResponse)
def read_contacts(
    skip: int = 0,
    limit: int = 10,
    keyword: str = None,
    order_contacts: str = None,
    request: Request = None,
    db: Session = Depends(get_session_local),
):
    return get_contacts(
        db=db,
        skip=skip,
        limit=limit,
        keyword=keyword,
        order_contacts=order_contacts,
        request=request,
    )


#  ดึงข้อมูล Contacts ตาม ID
@router.get("/contacts/{inquirer_id}", response_model=ContactResponse)
def read_contact(inquirer_id: int, db: Session = Depends(get_session_local)):
    return get_contact(db=db, inquirer_id=inquirer_id)


# อัพเดท Contacts ตาม ID
@router.put("/contacts/{inquirer_id}", response_model=ContactResponse)
def update_contact(
    inquirer_id: int, inquirer: ContactUpdate, db: Session = Depends(get_session_local)
):
    return update_contact(db=db, inquirer_id=inquirer_id, inquirer_update=inquirer)


# ลบ Contacts ตาม ID
@router.delete("/contacts/{inquirer_id}", response_model=ContactResponse)
def drop_contact(inquirer_id: int, db: Session = Depends(get_session_local)):
    return delete_contact(db=db, inquirer_id=inquirer_id)

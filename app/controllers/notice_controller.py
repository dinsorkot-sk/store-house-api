from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
from datetime import datetime
from app.models.notice import Notice
from app.models.notice_image import NoticeImage
from app.schemas.notice import (
    NoticeCreate,
    NoticeUpdate,
    NoticeInResponse,
    NoticeResponse,
)
from fastapi import HTTPException, Request


# ฟังก์ชันในการสร้าง Notice ใหม่
def create_notice(db: Session, notice_create: NoticeCreate) -> NoticeInResponse:
    # Create Notice instance
    notice_data = notice_create.dict(exclude={"images"})  # Exclude images here
    notice = Notice(**notice_data)

    # Add Notice to database
    db.add(notice)
    db.commit()
    db.refresh(notice)  # Load generated ID and timestamps

    # Add images if provided
    if notice_create.images:
        for image in notice_create.images:
            notice_image = NoticeImage(
                notice_id=notice.id,
                image_path=image.image_path,
            )
            db.add(notice_image)
        db.commit()

    # # Reload notice with images
    # notice = db.query(Notice).filter(Notice.id == notice.id).first()

    return NoticeInResponse.from_orm(notice)


# ฟังก์ชันในการอัปเดต Notice
def update_notice(
    db: Session, notice_id: int, notice_update: NoticeUpdate
) -> NoticeInResponse:
    # Find the Notice to update
    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    # Update fields dynamically
    update_fields = [
        "title",
        "first_name",
        "last_name",
        "phone",
        "email",
        "location",
        "size",
        "office_size",
        "details",
        "preferred_contact_phone",
        "preferred_contact_email",
        "poster_type",
        "price",
    ]
    for field in update_fields:
        if getattr(notice_update, field) is not None:
            setattr(notice, field, getattr(notice_update, field))

    # Update images if provided
    if notice_update.images:
        db.query(NoticeImage).filter(NoticeImage.notice_id == notice.id).delete()
        db.add_all(
            [
                NoticeImage(notice_id=notice.id, image_path=image.image_path)
                for image in notice_update.images
            ]
        )

    # Save changes
    db.commit()
    db.refresh(notice)
    return NoticeInResponse.from_orm(notice)


# ฟังค์ชั่นในการลบ
def delete_notice(db: Session, notice_id: int):
    # ค้นหา Notice
    notice = db.query(Notice).filter(Notice.id == notice_id).first()

    # ตรวจสอบว่า Notice มีอยู่หรือไม่
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    # ค้นหา NoticeImage ทั้งหมดที่เกี่ยวข้องกับ Notice
    notice_images = (
        db.query(NoticeImage).filter(NoticeImage.notice_id == notice.id).all()
    )

    # ตั้งค่า `deleted_at` สำหรับ NoticeImage (ถ้ามี)
    for image in notice_images:
        image.deleted_at = datetime.utcnow()

    # ตั้งค่า `deleted_at` สำหรับ Notice
    notice.deleted_at = datetime.utcnow()

    # บันทึกการเปลี่ยนแปลงในฐานข้อมูล
    db.commit()
    db.refresh(notice)

    return NoticeInResponse.from_orm(notice)


# ฟังก์ชันในการดึงข้อมูล Notice ตาม ID
def get_notice(db: Session, notice_id: int) -> NoticeInResponse:
    # ค้นหาข้อมูล Notice ที่มี id ตรงกับที่ระบุ
    notice = db.query(Notice).filter(Notice.id == notice_id).first()

    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    return NoticeInResponse.from_orm(notice)


# ฟังก์ชันในการดึงข้อมูลทั้งหมดของ Notices
def get_notices(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    keyword: str = None,
    order_price: str = None,
    order_size: str = None,
    order_notices: str = "desc",
) -> NoticeResponse:

    # Query สำหรับค้นหา Notice
    query = db.query(Notice)

    # เพิ่มเงื่อนไขการค้นหา หากมี keyword
    if keyword:
        query = query.filter(
            or_(
                Notice.title.ilike(f"%{keyword}%"),
                Notice.details.ilike(f"%{keyword}%"),
                Notice.location.ilike(f"%{keyword}%"),
            )
        )

    # จัดเรียงตามราคา (asc หรือ desc)
    if order_price == "asc":
        query = query.order_by(asc(Notice.price))
    elif order_price == "desc":
        query = query.order_by(desc(Notice.price))

    # จัดเรียงตามราคา (asc หรือ desc)
    if order_size == "asc":
        query = query.order_by(asc(Notice.size))
    elif order_size == "desc":
        query = query.order_by(desc(Notice.size))

    # จัดเรียงตามราคา (asc หรือ desc)
    if order_notices == "asc":
        query = query.order_by(asc(Notice.created_at))
    elif order_notices == "desc":
        query = query.order_by(desc(Notice.created_at))

    query = query.filter(Notice.deleted_at.is_(None))

    # ค้นหา Notice ทั้งหมดจากฐานข้อมูล
    notices = query.offset(skip).limit(limit).all()

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

    if not notices:
        raise HTTPException(status_code=404, detail="Notices not found")

    # สร้าง response ที่มีข้อมูลต่างๆ
    return NoticeResponse(
        total=total,
        total_pages=total_pages,
        current_page=current_page,
        next_page_url=next_page_url,
        prev_page_url=prev_page_url,
        notices=[NoticeInResponse.from_orm(notice) for notice in notices],
    )

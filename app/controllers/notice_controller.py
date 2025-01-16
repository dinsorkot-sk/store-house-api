from sqlalchemy.orm import Session
from app.models.notice import Notice
from app.schemas.notice import NoticeCreate, NoticeUpdate, NoticeInResponse
from fastapi import HTTPException , Request

# ฟังก์ชันในการสร้าง Notice ใหม่
def create_notice(db: Session, notice_create: NoticeCreate) -> NoticeInResponse:
    # สร้าง instance ของ Notice จากข้อมูลที่ได้รับ
    notice = Notice(
        title=notice_create.title,
        first_name=notice_create.first_name,
        last_name=notice_create.last_name,
        phone=notice_create.phone,
        email=notice_create.email,
        location=notice_create.location,
        size=notice_create.size,
        office_size=notice_create.office_size,
        details=notice_create.details,
        preferred_contact_phone=notice_create.preferred_contact_phone,
        preferred_contact_email=notice_create.preferred_contact_email,
        poster_type=notice_create.poster_type,
        price=notice_create.price,
    )

    # เพิ่มข้อมูลลงในฐานข้อมูล
    db.add(notice)
    db.commit()
    db.refresh(notice)  # โหลดข้อมูลที่เพิ่งเพิ่มเข้ามาใหม่เพื่อให้ได้ค่า id, timestamps

    return NoticeInResponse.from_orm(notice)

# ฟังก์ชันในการอัปเดต Notice
def update_notice(db: Session, notice_id: int, notice_update: NoticeUpdate) -> NoticeInResponse:
    # ค้นหา Notice ที่ต้องการอัปเดตจาก id
    notice = db.query(Notice).filter(Notice.id == notice_id).first()

    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    # อัปเดตข้อมูลของ Notice
    if notice_update.title:
        notice.title = notice_update.title
    if notice_update.first_name:
        notice.first_name = notice_update.first_name
    if notice_update.last_name:
        notice.last_name = notice_update.last_name
    if notice_update.phone:
        notice.phone = notice_update.phone
    if notice_update.email:
        notice.email = notice_update.email
    if notice_update.location:
        notice.location = notice_update.location
    if notice_update.size:
        notice.size = notice_update.size
    if notice_update.office_size:
        notice.office_size = notice_update.office_size
    if notice_update.details:
        notice.details = notice_update.details
    if notice_update.preferred_contact_phone is not None:
        notice.preferred_contact_phone = notice_update.preferred_contact_phone
    if notice_update.preferred_contact_email is not None:
        notice.preferred_contact_email = notice_update.preferred_contact_email
    if notice_update.poster_type:
        notice.poster_type = notice_update.poster_type
    if notice_update.price is not None:
        notice.price = notice_update.price

    # บันทึกการอัปเดตลงในฐานข้อมูล
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
def get_notices(db: Session, skip: int = 0, limit: int = 10 , request: Request = None) -> dict:
    # ค้นหา Notice ทั้งหมดจากฐานข้อมูล
    notices = db.query(Notice).offset(skip).limit(limit).all()
    
    # คำนวณจำนวนข้อมูลทั้งหมดในฐานข้อมูล
    total = db.query(Notice).count()

    # คำนวณจำนวนหน้า (total pages)
    total_pages = (total // limit) + (1 if total % limit > 0 else 0)
    
    # คำนวณหมายเลขหน้าปัจจุบัน
    current_page = (skip // limit) + 1
    
    # คำนวณ next และ prev page
    next_page = current_page + 1 if current_page < total_pages else None
    prev_page = current_page - 1 if current_page > 1 else None
    
    # ตรวจสอบว่า request มีค่า prefix หรือไม่ และสร้าง URL
    base_url = str(request.base_url) if request else "http://localhost:8000/"
    # สร้าง next_page_url และ prev_page_url โดยใช้ url_for และค่าพารามิเตอร์ที่เหมาะสม
    next_page_url = f"{base_url}api/notices/?skip={(next_page - 1) * limit}&limit={limit}" if next_page else None
    prev_page_url = f"{base_url}api/notices/?skip={(prev_page - 1) * limit}&limit={limit}" if prev_page else None
    
    # สร้าง response ที่มีข้อมูลต่างๆ
    return {
        "total": total,
        "total_pages": total_pages,
        "current_page": current_page,
        "next_page_url": next_page_url,
        "prev_page_url": prev_page_url,
        "notices": [NoticeInResponse.from_orm(notice) for notice in notices]
    }


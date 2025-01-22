from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
from app.models.admin_user import Admin_User
from app.schemas.admin_user import AdminUserCreate, AdminUserUpdate , AdminUserResponse
from fastapi import HTTPException,Request
import bcrypt


# ฟังก์ชันในการสร้าง AdminUser ใหม่
def create_admin_user(db: Session, admin_user_create: AdminUserCreate) -> AdminUserResponse:
    # ตรวจสอบว่า username ซ้ำหรือไม่
    existing_user = db.query(Admin_User).filter(Admin_User.username == admin_user_create.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = bcrypt.hashpw(admin_user_create.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    
    # สร้าง instance ของ Admin_User จากข้อมูลที่ได้รับ
    admin_user = Admin_User(
        username=admin_user_create.username,
        password=hashed_password,  
    )

    # เพิ่มข้อมูลลงในฐานข้อมูล
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)  # โหลดข้อมูลที่เพิ่งเพิ่มเข้ามาใหม่เพื่อให้ได้ค่า id, timestamps

    return AdminUserResponse.from_orm(admin_user) 


# ฟังก์ชันในการอัปเดต Admin User
def update_admin_user(
    db: Session, admin_user_id: int, admin_user_update: AdminUserUpdate
) -> AdminUserResponse:
    # ค้นหา adminuser ที่ต้องการอัปเดตจาก id
    admin_user = db.query(Admin_User).filter(Admin_User.id == admin_user_id).first()

    if not admin_user:
        raise HTTPException(status_code=404, detail="Notice not found")

    # อัปเดตข้อมูลของ adminuser
    if admin_user_update.username:
        admin_user.username = admin_user_update.username
    if admin_user_update.password:
        admin_user.password = bcrypt.hashpw(
            admin_user_update.password.encode('utf-8'), bcrypt.gensalt()
        ).decode('utf-8')
    
    # บันทึกการอัปเดตลงในฐานข้อมูล
    db.commit()
    db.refresh(admin_user)

    return AdminUserResponse.from_orm(admin_user)


def soft_delete_admin_user(db: Session, admin_user_id: int):
    # ค้นหา Admin User ที่ต้องการลบ
    admin_user = db.query(Admin_User).filter(Admin_User.id == admin_user_id).first()

    if not admin_user:
        raise HTTPException(status_code=404, detail="Admin user not found")

    if admin_user.deleted_at:
        raise HTTPException(status_code=400, detail="Admin user already deleted")

    # อัปเดต deleted_at ให้เป็นเวลาปัจจุบัน
    admin_user.deleted_at = datetime.now()

    # บันทึกการเปลี่ยนแปลง
    db.commit()
    db.refresh(admin_user)



# ฟังก์ชันในการล็อกอิน AdminUser
def login_admin_user(db: Session, username: str, password: str):
    # ค้นหาผู้ใช้ตาม username
    admin_user = db.query(Admin_User).filter(Admin_User.username == username).first()
    if not admin_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # ตรวจสอบรหัสผ่าน
    if not bcrypt.checkpw(password.encode('utf-8'), admin_user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    # ส่งข้อมูลผู้ใช้งานกลับในกรณีที่ล็อกอินสำเร็จ
    return {
        "id": admin_user.id,
        "username": admin_user.username,
        "created_at": admin_user.created_at,
        "updated_at": admin_user.updated_at
    }




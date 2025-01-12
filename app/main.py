from fastapi import FastAPI
from app.database import Base, engine
from app.routers import user

# สร้างตารางในฐานข้อมูล
Base.metadata.create_all(bind=engine)

app = FastAPI()

# เพิ่ม Router
app.include_router(user.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with MySQL"}

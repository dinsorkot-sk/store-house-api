from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import notice, inquirer , admin_user , contact , working
from app.middleware.login import LoginMiddleware

# สร้างตารางในฐานข้อมูล
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # หรือ "" สำหรับอนุญาตทุกโดเมน
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # กำหนด method ที่อนุญาต
    allow_headers=[""],  # กำหนด headers ที่อนุญาต
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(notice.router)
app.include_router(inquirer.router)
app.include_router(admin_user.router)

app.add_middleware(LoginMiddleware)

app.include_router(contact.router)
app.include_router(working.router)


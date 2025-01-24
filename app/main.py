from fastapi import FastAPI
from app.database import Base, engine
from app.routers import notice, inquirer , admin_user , contact


# สร้างตารางในฐานข้อมูล
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(notice.router)
app.include_router(inquirer.router)
app.include_router(admin_user.router)
app.include_router(contact.router)

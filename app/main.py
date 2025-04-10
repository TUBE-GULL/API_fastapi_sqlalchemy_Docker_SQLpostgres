from fastapi import FastAPI
from app.routers.main_router import root
from app.database import create_db

app = FastAPI()
app.include_router(root)# Подключаем главный роутер (там все маршруты).

@app.on_event("startup")
async def startup():
    await create_db()
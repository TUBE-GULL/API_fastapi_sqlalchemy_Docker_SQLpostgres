from fastapi import FastAPI
from alembic.config import Config
from alembic import command

from app.routers.main_router import root
from app.database import create_db

app = FastAPI()
app.include_router(root)# Подключаем главный роутер (там все маршруты).

@app.on_event("startup")
async def startup():
    await create_db()
    
    


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

# Вызывайте при старте приложения
run_migrations()
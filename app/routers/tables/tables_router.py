from fastapi import APIRouter

from app.routers.tables.get_all import router_get_all_tables
from app.routers.tables.create import router_create_table 
from app.routers.tables.delete import router_delete_table

tables = APIRouter(
    prefix='/tables',
    tags=["Столики"]
)

tables.include_router(router_get_all_tables)
tables.include_router(router_create_table)
tables.include_router(router_delete_table)
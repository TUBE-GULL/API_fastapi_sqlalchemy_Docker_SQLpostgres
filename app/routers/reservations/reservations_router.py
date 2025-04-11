from fastapi import APIRouter
from app.routers.reservations.create import router_create_reservation
from app.routers.reservations.delete import router_delete_reservation
from app.routers.reservations.get_all import router_get_all_reservations

reservations = APIRouter(
    prefix="/reservations",
    tags=["Брони"]
)

reservations.include_router(router_create_reservation)
reservations.include_router(router_delete_reservation)
reservations.include_router(router_get_all_reservations)


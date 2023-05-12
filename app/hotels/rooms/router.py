from datetime import date, datetime

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRoomsRoomLeft


router = APIRouter(
    prefix="/hotels", 
    tags=["Rooms"]
)

# Get all rooms by hotel_id
@router.get("/{hotel_id}/rooms")
@cache(expire=20)
async def get_all_rooms_by_hotel_id(
    hotel_id: str, 
    date_from: date = Query(..., description=f"Date format is: {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Date format is: {datetime.now().date()}"),
) -> list[SRoomsRoomLeft]:
    return await RoomsDAO.get_available_rooms_by_hotel_id(int(hotel_id), date_from, date_to)
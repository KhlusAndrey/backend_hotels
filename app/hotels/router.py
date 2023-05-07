from datetime import date, datetime
from pydantic import parse_obj_as
from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache
from app.hotels.dao import HotelDAO
from app.hotels.rooms.schemas import SRooms

from app.hotels.schemas import SHotels

router = APIRouter(
    prefix="/hotels",
    tags=["hotels"]
)


@router.get("/{location}")
@cache(expire=60)
async def get_hotels_by_location_and_date(
    location: str,
    date_from: date = Query(..., description=f"Date format is: {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Date format is: {datetime.now().date()}")
):
    hotels = await HotelDAO.search_for_hotels(location, date_from, date_to)
    hotels_json = parse_obj_as(list[SHotels], hotels)
    return hotels_json

@router.get("/{hotel_id}/rooms")
async def get_rooms_by_time(
    hotel_id: int,
    date_from: date = Query(..., description=f"Date format is: {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Date format is: {datetime.now().date()}"),
) -> list[SRooms]:
    rooms = await HotelDAO.search_for_rooms(hotel_id, date_from, date_to)

    return rooms

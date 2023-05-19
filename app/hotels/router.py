from datetime import date, datetime

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache
from pydantic import parse_obj_as

from app.hotels.dao import HotelDAO
from app.hotels.rooms.schemas import SRooms
from app.hotels.schemas import SHotels, SHotelsRoomsLeft

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)


@router.get("/all")
@cache(expire=60)
async def get_all_hotels() -> list[SHotels]:
    return await HotelDAO.select_all_filter()


@router.get("/id")
@cache(expire=60)
async def get_hotel_by_id(hotel_id: str) -> SHotels:
    return await HotelDAO.find_one_or_none(id=int(hotel_id))


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

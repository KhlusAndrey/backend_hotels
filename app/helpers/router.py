import csv

from fastapi import APIRouter, Depends

from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.dependencies import get_current_admin_user
from app.users.models import Users

router = APIRouter(
    prefix="/import", 
    tags=["Import hotels and rooms"]
)

# Loading hotels in database 
@router.post("/hotels")
async def import_hotels_to_database(admin_user: Users = Depends(get_current_admin_user),
    ):
    async with async_session_maker() as session:
        with open("app/helpers/hotels.csv", encoding="UTF-8", newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Пропуск заголовков столбцов
            print(reader)
            for row in reader:
                id, name, location, services, room_quantity, image_id = row
                services = services.strip('[]').replace('"', '').split('; ')
                hotel = Hotels(id=int(id), name=name, location=location, services=services, room_quantity=int(room_quantity), image_id=int(image_id))
                session.add(hotel)
        await session.commit()


# Loading rooms in database 
@router.post("/rooms")
async def import_rooms_to_database(admin_user: Users = Depends(get_current_admin_user),
    ):
    async with async_session_maker() as session:
        with open("app/helpers/rooms.csv", encoding="UTF-8", newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Пропуск заголовков столбцов
            for row in reader:
                hotel_id, name, description, price, services, quantity, image_id = row
                services = services.strip('[]').replace('"', '').split('; ')
                room = Rooms(hotel_id=int(hotel_id), name=name, description=description, price=int(price), services=services, quantity=int(quantity), image_id=int(image_id))
                session.add(room)
        await session.commit()



from datetime import date

from sqlalchemy import String, and_, cast, func, label, or_, select
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.database import async_session_maker, engine
from app.hotels.rooms.models import Rooms

"""
Получение списка отелей

Пример эндпоинта: /hotels/Алтай.
HTTP метод: GET.
HTTP код ответа: 200.
Описание: возвращает список отелей по заданным параметрам, 
причем в отеле должен быть минимум 1 свободный номер.
Нужно быть авторизованным: нет.
Параметры: параметр пути location и параметры запроса date_from, date_to.
Ответ пользователю: 
для каждого отеля должно быть указано: 
id, 
name, 
location, 
services, 
rooms_quantity, 
image_id, 
rooms_left (количество оставшихся номеров).
"""

class HotelDAO(BaseDAO):
    model = Hotels

    # @classmethod
    # async def search_for_hotels(
    #     cls,
    #     location: str,
    #     date_from: date,
    #     date_to: date,
    # ):
    #     async with async_session_maker() as session:
    #         # Найдем отели подходящие под поиск
    #         hotels = (
    #             select(Hotels)
    #             .where(Hotels.location.ilike(f'%{location}%'))
    #         ).cte(name="hotels")

    #         # Найдем все забронированные номера в период date_from - date_to
    #         bookings = (
    #             select(Bookings.room_id, func.count(Bookings.id).label("num_bookings"))
    #             .where(or_(
    #                 and_(Bookings.date_from <= date_from, Bookings.date_to >= date_from),
    #                 and_(Bookings.date_from >= date_from, Bookings.date_from <= date_to),
    #             ))
    #             .group_by(Bookings.room_id)
    #         ).cte(name="bookings")

    #         # Сделаем JOIN на Rooms и сгруппируем по отелям
    #         room_counts = (
    #             select(hotels.c.id, func.sum(Rooms.quantity - bookings.c.num_bookings).label("rooms_left"))
    #             .select_from(hotels.join(Rooms, Hotels.id == Rooms.hotel_id).join(bookings, Rooms.id == bookings.c.room_id, isouter=True))
    #             .group_by(hotels.c.id)
    #         ).cte(name="room_counts")

    #         # Сделаем JOIN на результаты предыдущего CTE и превратим их в модель SHotels
    #         query = (
    #             select(room_counts.c.id, Hotels.name, Hotels.location, Hotels.services, Hotels.room_quantity, Hotels.image_id, room_counts.c.rooms_left)
    #             .select_from(room_counts.join(Hotels, Hotels.id == room_counts.c.id))
    #         )
            
    #         print(query.compile(engine, compile_kwargs={"literal_binds": True}))

    #         result = await session.execute(query)
    #         return result.scalars().all()
             
    @classmethod
    async def search_for_hotels(
        cls,
        location: str,
        date_from: date,
        date_to: date,
    ):
        async with async_session_maker() as session:
            bookings_for_selected_dates = (
                select(Bookings)
                .filter(
                    or_(
                        and_(
                            Bookings.date_from < date_from,
                            Bookings.date_to > date_from
                        ),
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from < date_to
                        ),
                    )
                )
                .subquery("filtered_bookings")
            )
            hotels_rooms_left = (
                select(
                (
                    Hotels.room_quantity - func.count(bookings_for_selected_dates.c.room_id)
                ).label("rooms_left"),
                Rooms.hotel_id,
                )
                .select_from(Hotels)
                .outerjoin(Rooms, Rooms.hotel_id == Hotels.id)
                .outerjoin(
                    bookings_for_selected_dates,
                    bookings_for_selected_dates.c.room_id == Rooms.id,
                )
                .where(
                    Hotels.location.contains(location.title()),
                )
                .group_by(Hotels.room_quantity, Rooms.hotel_id)
                .cte("hotels_rooms_left")
            )
            get_hotels_info = (
                select(
                Hotels.__table__.columns,
                hotels_rooms_left.c.rooms_left,
                )
                .select_from(Hotels)
                .join(hotels_rooms_left, hotels_rooms_left.c.hotel_id == Hotels.id)
                .where(hotels_rooms_left.c.rooms_left > 0)
            )
            hotels_info = await session.execute(get_hotels_info)
            return hotels_info.all()


    @classmethod
    async def search_for_rooms(
        cls,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        async with async_session_maker() as session:
            bookings_for_selected_dates = (
                select(Bookings)
                .filter(
                or_(
                        and_(
                            Bookings.date_from < date_from,
                            Bookings.date_to > date_from
                        ),
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from < date_to
                        ),
                    )
                )
                .subquery("filtered_bookings"),
            )
            rooms_left = (
                    select(
                        (
                          Rooms.quantity - func.count(bookings_for_selected_dates.c.room_id)
                        ).label("rooms_left"),
                        Rooms.id.label("room_id"),
                    )
                    .select_from(Rooms)
                    .outerjoin(
                        bookings_for_selected_dates,
                        bookings_for_selected_dates.c.room_id == Rooms.id
                    )
                    .where(Rooms.hotel_id == hotel_id)
                    .group_by(
                        Rooms.quantity, bookings_for_selected_dates.c.room_id, Rooms.id
                    )
                    .cte()
                )
            

class HotelRepository:
   
    @classmethod
    async def find_all():
        pass

class HotelService:

    @classmethod
    async def find_all():
        pass



from datetime import date
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from sqlalchemy import delete, select, insert, func, and_, or_
from app.bookings.schemas import SBookings
from app.hotels.rooms.models import Rooms
from app.database import engine, async_session_maker

class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add_booking(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date, 
    ):
        """
        WITH booked_rooms AS (
        SELECT * FROM bookings
        WHERE room_id = 1 AND 
        (date_from >= "2023-05-15" AND date_from <= "2023-06-20") OR
        (date_from <= "2023-05-15" AND date_to > "2023-05-15")
        )
        """
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_to <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        )
                    )
                )

            ).cte("booked_rooms")

            """
            SELECT room.quantity - COUNT(booked_rooms.room_id) FROM rooms
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            WHERE rooms.id = 1
            GROUP BY rooms.quantity, booked_rooms.room_id
            """
            get_rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
            ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(Rooms.id == room_id).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )

            print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))
            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking_to_db = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ).returning(Bookings)

                new_booking = await session.execute(add_booking_to_db)
                await session.commit()
                return new_booking.scalar()
            else:
                return None
        
    # @classmethod
    # async def booking_delete(cls, booking_id):
    #     async with async_session_maker() as session:
    #         await session.delete(booking_id)
    #         await session.commit()
            """
        Пример эндпоинта: /bookings.
        HTTP метод: GET.
        HTTP код ответа: 200.
        Описание: возвращает список всех бронирований пользователя.
        Нужно быть авторизованным: да.
        Параметры: отсутствуют.
        
        Ответ пользователю: для каждого бронирования должно быть указано: 
        room_id, 
        user_id, 
        date_from, 
        date_to, price, 
        total_cost, 
        total_days, 
        image_id(для номера), 
        name(для номера), 
        description, 
        services(для номера).
id = Column(Integer, primary_key=True)
room_id = Column(ForeignKey("rooms.id"))
user_id = Column(ForeignKey("users.id") )
date_from = Column(Date, nullable=False)
date_to = Column(Date, nullable=False)
price = Column(Integer, nullable=False)
total_cost = Column(Integer, Computed("(date_to - date_from) * price"))
total_days = Column(Integer, Computed("date_to - date_from"))

        """
            
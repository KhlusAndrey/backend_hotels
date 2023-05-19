from datetime import date

from sqlalchemy import and_, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.bookings.schemas import SBookings, SBookingWithRoomInfo
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import BookingsNotExistException, RoomCanNotBeBookedException
from app.helpers.helpers import validation_bookings_dates
from app.hotels.rooms.models import Rooms
from app.logger import logger
from app.users.models import Users


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add_booking(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ) -> None:
        """Add booking for current user"""

        await validation_bookings_dates(date_from, date_to)

        """
        WITH booked_rooms AS (
        SELECT * FROM bookings
        WHERE room_id = 1 AND 
        (date_from >= "2023-05-15" AND date_from <= "2023-06-20") OR
        (date_from <= "2023-05-15" AND date_to > "2023-05-15")
        )
        """
        async with async_session_maker() as session:
            booked_rooms = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == room_id,
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_to <= date_to,
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_from,
                            ),
                        ),
                    )
                )
                .cte("booked_rooms")
            )

            """
            SELECT room.quantity - COUNT(booked_rooms.room_id) FROM rooms
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            WHERE rooms.id = 1
            GROUP BY rooms.quantity, booked_rooms.room_id
            """
            get_rooms_left = (
                select(
                    (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                        "rooms_left"
                    )
                )
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )

            # print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True})) # Show raw SQL query from ORM
            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price: int = await session.execute(get_price)
                price: int = price.scalar()
                add_booking_to_db = (
                    insert(Bookings)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(Bookings)
                )

                new_booking = await session.execute(add_booking_to_db)
                await session.commit()
                return new_booking.scalar()
            else:
                return None

    @classmethod
    async def get_booked_rooms(
        cls, room_id: int, date_from: date, date_to: date
    ) -> int:
        """Get available rooms by room_id for period date_from - date_to"""

        await validation_bookings_dates(date_from, date_to)

        return await cls.select_all_filter(
            and_(
                Bookings.room_id == room_id,
                and_(Bookings.date_to >= date_from, Bookings.date_from <= date_to),
            )
        )

    @classmethod
    async def get_booking_for_user(cls, user: Users) -> list[SBookingWithRoomInfo]:
        """Get all bookings for current user"""
        async with async_session_maker() as session:
            query = (
                select(
                    Bookings.id,
                    Bookings.room_id,
                    Bookings.user_id,
                    Bookings.date_from,
                    Bookings.date_to,
                    Bookings.price,
                    Bookings.total_cost,
                    Bookings.total_days,
                    Rooms.image_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.services,
                )
                .select_from(Bookings)
                .join(Rooms, Bookings.room_id == Rooms.id, isouter=True)
                .where(Bookings.user_id == user.id)
            )

            result = await session.execute(query)
            return result.all()

    @classmethod
    async def add_booking_for_user(
        cls, user_id: int, room_id: int, date_from: date, date_to: date
    ) -> SBookings:
        """Add booking for current user"""
        try:
            # Cheek correct booking dates
            await validation_bookings_dates(date_from, date_to)
            booked_rooms: int = len(
                await cls.get_booked_rooms(room_id, date_from, date_to)
            )
            async with async_session_maker() as session:
                total_rooms = (
                    await session.execute(select(Rooms.quantity).filter_by(id=room_id))
                ).scalar()
                # If not available rooms for booking
                if not total_rooms - booked_rooms:
                    raise RoomCanNotBeBookedException
                # Get price for room per night
                price: int = (
                    await session.execute(select(Rooms.price).filter_by(id=room_id))
                ).scalar()
                # Add booking
                return (
                    await cls.add_rows(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                ).scalar()
        # Add logging
        except (SQLAlchemyError, Exception) as err:
            if isinstance(err, SQLAlchemyError):
                msg: str = "DB"
            elif isinstance(err, Exception):
                msg: str = "Unknown"
            msg += "Exception: Cannot add booking"
            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }
            logger.error(msg, extra=extra, exc_info=True)

    @classmethod
    async def delete_booking_for_user(cls, booking_id: int, user_id: int) -> None:
        """Delete booking for current user by booking_id"""
        # Cheek booking is exist
        if not await cls.find_one_or_none(id=booking_id, user_id=user_id):
            raise BookingsNotExistException
        # Delete booking
        await cls.delete_rows_filer_by(id=booking_id, user_id=user_id)

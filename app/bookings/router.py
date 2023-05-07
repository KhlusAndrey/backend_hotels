from datetime import date
from fastapi import APIRouter, Depends


from app.bookings.dao import BookingDAO
from app.bookings.models import Bookings
from app.bookings.schemas import SBookings
from app.exceptions import BookingsNotExistException, RoomCanNotBeBookedException
from app.tasks.tasks import send_email_booking_confirmation
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix="/bookings",
    tags=["Booking"]
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookings]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("")
async def add_booking(
    room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add_booking(user.id, room_id, date_from, date_to)
    # send_email_booking_confirmation.delay(booking, user.email) # For send need tune email
    if not booking:
        raise RoomCanNotBeBookedException


# @router.delete("/{id}")
# async def all_bookings(
#     booking_id = id,
#     user: Users = Depends(get_current_user)
# ):
#     get_booking = await BookingDAO.find_one_or_none(booking_id)
#     if not get_booking:
#         raise BookingsNotExistException
#     await BookingDAO.delete_booking(get_booking)

from datetime import date, datetime
from fastapi import APIRouter, Depends, Query, Response


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
    room_id: int,
    date_from: date = Query(..., description=f"Date format is: {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Date format is: {datetime.now().date()}"), 
    user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add_booking(user.id, room_id, date_from, date_to)
    # send_email_booking_confirmation.delay(booking, user.email)           # Celery task, for sending emails you should tune email settings in .env
    if not booking:
        raise RoomCanNotBeBookedException


@router.delete("/{booking_id}")
async def delete_booking(response: Response,
    booking_id: int,
    user: Users = Depends(get_current_user)) -> None:
    await BookingDAO.delete_booking_for_user(booking_id=int(booking_id), user_id=user.id)
    response.status_code = 204

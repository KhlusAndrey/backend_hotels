from datetime import date, timedelta

from app.exceptions import (
    DatesFromBookingException,
    DatesToBookingException,
    IntervalMoreThenBookingException,
)

current_date = date.today()


async def validation_bookings_dates(date_from: date, date_to: date) -> None:
    """Validation correction booking dates input"""
    if date_from < current_date:
        raise DatesFromBookingException
    if date_to < date_from:
        raise DatesToBookingException
    if (date_to - date_from) > timedelta(days=30):
        raise IntervalMoreThenBookingException

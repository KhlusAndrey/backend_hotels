from datetime import datetime, timedelta
from app.helpers.helpers import validation_bookings_dates
from app.exceptions import DatesFromBookingException, DatesToBookingException, IntervalMoreThenBookingException
import pytest

current_date = datetime.today().date()
date_from = current_date + timedelta(days=2)
date_to = current_date + timedelta(days=4)
less_current = current_date - timedelta(days=1)
more_then_30_day = date_from + timedelta(days=31)

@pytest.mark.parametrize("date_from, date_to, raise_exception", [
    (date_from, date_to, None),
    (date_to, date_from, DatesToBookingException),
    (less_current, date_to, DatesFromBookingException),
    (date_from, more_then_30_day, IntervalMoreThenBookingException),
])
def test_validation_dates(date_from, date_to, raise_exception):
    if raise_exception:
        with pytest.raises(raise_exception):
            validation_bookings_dates(date_from, date_to)
    else:
        validation_bookings_dates(date_from, date_to)

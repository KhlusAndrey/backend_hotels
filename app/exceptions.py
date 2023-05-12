from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code: int = 500
    detail: str = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="User already exist"


class IncorrectEmailOrPassword(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Incorrect email or password"


class TokenExpireException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Token expire period not valid"


class TokenAbsentExceptions(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Token is absent"


class IncorrectTokenFormatExceptio(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Token is incorrect"


class IncorrectTokenUsertExceptio(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Token for user is not valid"


class NoAccessPermissionExseption(BookingException):
    status_code=status.HTTP_403_FORBIDDEN
    detail="Access forbidden"


class RoomCanNotBeBookedException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Don't have available rooms"


class BookingsNotExistException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Not found bookings by id"


class DurationBookingException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="booking more than 30 days"


class DatesToBookingException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Date to can not be more than Date from"


class DatesFromBookingException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Date from can not be less than current date"

class IntervalMoreThenBookingException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Booking interval more than 30 days"
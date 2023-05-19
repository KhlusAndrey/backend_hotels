from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email, Users.role]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    page_size = 50
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c]  # Take all columns from model
    column_list += [Bookings.user_email, Bookings.room]
    page_size = 50
    name = "Booking"
    name_plural = "Bookings"
    icon = "fa-solid fa-calendar"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c]
    column_list += [Hotels.rooms]
    page_size = 50
    name = "Hotel"
    name_plural = "Hotels"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c]
    column_list += [Rooms.hotel, Rooms.booking]
    page_size = 50
    name = "Room"
    name_plural = "Rooms"
    icon = "fa-solid fa-bed"

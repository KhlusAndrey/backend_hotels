from fastapi import FastAPI

from app.bookings.router import router as router_bookings
from app.users.router import router as router_user


app = FastAPI()


app.include_router(router_user)
app.include_router(router_bookings)


@app.get('/')
def get_hotels():
    return 'hotels'

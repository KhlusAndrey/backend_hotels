import time

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.helpers.router import router as router_import
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.logger import logger
from app.pages.router import router as router_pages
from app.users.models import Users
from app.users.router import router as router_user

# from contextlib import asynccontextmanager


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.info("Service started")
#     yield
#     logger.info("Service exited")

# Sentry logging
sentry_sdk.init(
    dsn="https://0a7b98aac16746f2b76956910b28abcf@o4505176593399808.ingest.sentry.io/4505176598183936",
    traces_sample_rate=1.0,
)

app = FastAPI(
    title="Hotels booking",
    version="0.1.0",
    root_path="/api",
)
# app = FastAPI(lifespan=lifespan)


app.include_router(router_user)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_images)
app.include_router(router_pages)
app.include_router(router_import)

origins = [
    # 3000 - порт, на котором работает фронтенд на React.js
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

# Versionization (endpont in router get @version(1))
app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/v{major}",
)

# Redis connection for caching
@app.on_event("startup")
def startup():
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")

# Prometeus monitoring
Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
).instrument(app).expose(app)

# Administration panel
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), "static")


# Add logging middleware for castom messages use lib python-json-logger logger.py
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # If use Prometheus + Grafana, this log is not needed
    # logger.info("Request handling time", extra={"process_time": round(process_time, 4)})
    return response

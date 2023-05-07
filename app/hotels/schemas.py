from pydantic import BaseModel, Json


class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    room_quantity: int
    image_id: int
    rooms_left: int

    class Config:
        orm_mode = True


class SHotelsRoomsLeft(SHotels):
    rooms_left: int
    
    
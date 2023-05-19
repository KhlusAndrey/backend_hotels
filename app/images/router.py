import shutil

from fastapi import APIRouter, Response, UploadFile

from app.tasks.tasks import process_pic

router = APIRouter(
    prefix="/images",
    tags=["Images loading"]
)

@router.post("/hotels")
async def add_hotel_image(response: Response, name: str, file: UploadFile):
    img_path = f"app/static/images/{name}.webp"
    with open(img_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_pic.delay(img_path)
    response.status_code = 201
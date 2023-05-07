import smtplib
from pydantic import EmailStr
from app.config import settings
from app.tasks.celery import celery
from PIL import Image
from pathlib import Path

from app.tasks.email_tamplates import create_booking_confirmation_template

# IF ADD NEW TASK DO NOT FORGET RELOAD CELERY TERMINAL!

@celery.task
def process_pic(path: str) -> None:
    img_path = Path(path)
    img = Image.open(img_path)
    img_resize_1000x500 = img.resize((1000, 500))
    img_resize_200x100 = img.resize((200, 100))
    img_resize_1000x500.save(f"app/static/images/resize_1000x500_{img_path.name}")
    img_resize_200x100.save(f"app/static/images/resize_200x100_{img_path.name}")


@celery.task
def send_email_booking_confirmation(
    booking: dict,
    email_to: EmailStr
):
    msg_content = create_booking_confirmation_template(booking, email_to)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)


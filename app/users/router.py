from fastapi import APIRouter, Depends, Response
from app.users.auth import  get_password_hash, autentificate_user, create_acces_token
from app.users.dao import UsersDAO
from app.users.dependencies import get_curent_admin_user, get_current_user
from app.users.models import Users
from app.exceptions import IncorrectEmailOrPassword, UserAlreadyExistException

from app.users.schemas import SUserAuth


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_users = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_users:
        raise UserAlreadyExistException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add_to_db(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await autentificate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPassword
    access_token = create_acces_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}

@router.post("/logout")
async def  logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/current")
async def read_current_user(current_user: Users = Depends(get_current_user)):
    return current_user

@router.get("/all-users")
async def read_current_user(current_user: Users = Depends(get_curent_admin_user)):
    return await UsersDAO.find_all()
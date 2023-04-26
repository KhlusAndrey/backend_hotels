
from datetime import datetime
from jose import jwt, JWTError
from fastapi import Depends, Request

from app.config import settings
from app.exceptions import IncorrectTokenFormatExceptio, IncorrectTokenUsertExceptio, TokenAbsentExceptions, TokenExpireException
from app.users.dao import UsersDAO
from app.users.models import Users


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentExceptions
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatExceptio
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpireException
    user_id: str = payload.get("sub")
    if not user_id:
        raise IncorrectTokenUsertExceptio
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise IncorrectTokenUsertExceptio
    
    return user

# Для добавления админа нужно изменить модель Юзерс, добавить роль.
async def get_curent_admin_user(current_user: Users = Depends(get_current_user)):
    # if current_user.role != "admin":
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return current_user

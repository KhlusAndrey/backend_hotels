from datetime import datetime
from jose import jwt, JWTError
from fastapi import Depends, Request

from app.config import settings
from app.exceptions import IncorrectTokenFormatExceptio, IncorrectTokenUsertExceptio, NoAccessPermissionExseption, TokenAbsentExceptions, TokenExpireException
from app.users.dao import UsersDAO
from app.users.models import Users


def get_token(request: Request):
    """Get token from FastAPI Request"""

    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentExceptions
    return token

async def get_current_user(token: str = Depends(get_token)):
    """ Check and verificate correct JWT with currrent user's JWT"""

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


async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    """Check is current user admin, by Users.role"""

    if current_user.role != "admin":
        raise NoAccessPermissionExseption
    return current_user

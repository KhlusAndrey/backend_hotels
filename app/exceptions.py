from fastapi import HTTPException, status


UserAlreadyExistException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exist"
)

IncorrectEmailOrPassword = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password"
)

TokenExpireException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token expire period not valid"
)

TokenAbsentExceptions = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is absent"
)

IncorrectTokenFormatExceptio = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is incorrect"
)

IncorrectTokenUsertExceptio = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token for user is not valid"
)
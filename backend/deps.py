from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .utils import decode_token
from datetime import datetime
from .schemas import TokenPayLoad, SystemUser
from jose import jwt
from pydantic import ValidationError
from .database import users_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")

def get_current_user(token: str = Depends(oauth2_scheme))->SystemUser:
    try:
        payload = decode_token(token)
        token_data = TokenPayLoad(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token Expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    
    user = users_db.get(token_data.sub, None)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return SystemUser(**user)
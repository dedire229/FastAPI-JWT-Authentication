from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .utils import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", scheme_name="JWT")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return email

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.responses import RedirectResponse
from app.schemas import UserOut, UserAuth, TokenSchema
from fastapi.security import OAuth2PasswordRequestForm
from app.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)

from uuid import uuid4 

app = FastAPI()
users_db = {}

@app.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    # querying database to check if user already exist
    user = users_db.get(data.email, None)
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = {
        'email': data.email,
        'password': get_hashed_password(data.password),
        'id': str(uuid4()),
        "username": data.username
    }
    users_db[data.email] = user    # saving user to database
    return UserOut(id=user["id"],
                   email=user["email"],
                   username=user["username"])

@app.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found!"
        )

    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }

@app.get("/users", response_model=list[UserOut])
async def get_users():
    return [
        {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }
        for user in users_db.values()
    ]

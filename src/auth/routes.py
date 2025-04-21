from fastapi import APIRouter, Depends, status, HTTPException, Query
from fastapi.responses import JSONResponse
from src.auth.schemas import User, UserRegister, UserLogin
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.service import auth_service
from typing import Optional
from src.auth.utils import create_access_token, decode_token
from datetime import timedelta

REFRESH_TOKEN_EXPIRY = 2

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=User)
async def register_user(user_data: UserRegister, session: AsyncSession = Depends(get_session)):
    email_taken = await auth_service.user_exists(user_data.email, session)
    if email_taken:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email already taken")

    user = await auth_service.register_user(user_data, session)
    return user


@router.get("/", response_model=User)
async def get_user(
    user_id: Optional[str] = Query(default=None),
    email: Optional[str] = Query(default=None),
    session: AsyncSession = Depends(get_session)
    ):
    if not user_id and not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID or email is required")
    user = await auth_service.get_user(user_id, email, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@router.post("/login")
async def login_user(login_data: UserLogin, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await auth_service.login_user(email, password, session)

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong credentials")
    
    access_token = create_access_token(user_data={
        "email": user.email,
        "id": str(user.id)
        }
    )

    refresh_token = create_access_token(
        user_data={
            "email": user.email,
            "id": str(user.id)
        },
        refresh=True,
        expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
    )

    return JSONResponse(
        content={
            "message": "Login Successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "email": user.email,
                "username": user.username,
                "id": str(user.id)
            }
        }
    )


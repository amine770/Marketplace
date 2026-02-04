from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.token import Token
from app.core.security import hash_password, verify_password, create_access_token
from app.repositories import user_repo

async def register_user(db: AsyncSession, user_data: UserCreate) -> User:
    existing_user = await user_repo.get_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already exist")

    hashed_password = hash_password(user_data.password)
    user = await user_repo.create(db, user_data, hashed_password)
    return user


async def authenticate(db: AsyncSession, email: str, password: str) -> User:
    user = await user_repo.get_by_email(db, email)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Account Inactive")
    
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password")
    return user

async def login(db: AsyncSession, email: str, password: str):
    user = await authenticate(db, email, password)

    access_token = create_access_token(data = {"sub": user.email})

    return Token(access_token=access_token, token_type="bearer")
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate
from typing import Optional

async def get_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def create(db: AsyncSession, user_data: UserCreate, hashed_password: str) -> User:
    user = User(
        email = user_data.email,
        hashed_password = hashed_password,
        full_name = user_data.full_name,
        location = user_data.location,
        phone = user_data.phone
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
    


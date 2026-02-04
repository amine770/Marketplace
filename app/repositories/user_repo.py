from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.listing import Listing
from app.schemas.user import UserCreate, UserUpdate
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
    
async def update(db: AsyncSession, user: User, user_data: UserUpdate):
    user_data = user_data.model_dump(exclude_unset=True)

    for key, value in user_data.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user

async def listing_user_count(db: AsyncSession, user: User):
    result = await db.execute(select(func.count(Listing.id)).where(Listing.user_id == user.id).where(Listing.status == "active"))
    return result.scalar() or 0

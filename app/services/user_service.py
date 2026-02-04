from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserUpdate
from app.repositories import user_repo

async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    user = await user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="user not found")
    return user
    
async def update_user_profile(db: AsyncSession, user: User, user_data: UserUpdate):
    updated_user = await user_repo.update(db, user, user_data)
    return updated_user

async def get_user_with_stats(db: AsyncSession, user_id: int) -> dict:
    user = await get_user_by_id(db, user_id)
    listings_count = await user_repo.listing_user_count(db, user)
    return {
        "id" : user.id,
        "full_name" : user.full_name,
        "created_at": user.created_at,
        "phone" : user.phone,
        "location" : user.location,
        "listings_count" : listings_count
    }
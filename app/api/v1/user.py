from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import user_service
from app.models.user import User
from app.db.session import get_db
from app.core.dependencies import get_current_User
from app.schemas.user import UserResponse, UserUpdate, UserWithStatesResponse


router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(cur_user: User = Depends(get_current_User)):
    return UserResponse.model_validate(cur_user)

@router.put("/me", response_model=UserResponse)
async def update_cur_user_profile(user_data: UserUpdate, cur_user: User = Depends(get_current_User), db: AsyncSession = Depends(get_db)):
    user_updated = await user_service.update_user_profile(db, cur_user, user_data)
    return UserResponse.model_validate(user_updated)

@router.get("/{user_id}", response_model=UserWithStatesResponse)
async def get_user_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_service.get_user_with_stats(db, user_id)
    return user
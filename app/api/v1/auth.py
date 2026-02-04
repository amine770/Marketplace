from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_User
from app.db.session import get_db
from app.schemas.token import Token
from app.schemas.user import UserResponse, UserCreate, UserLogin
from app.services import auth_service
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await auth_service.register_user(db, user_data)
    return UserResponse.model_validate(user)

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    access_token = await auth_service.login(db, user_data.email, user_data.password)
    return access_token

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_User)):
    return UserResponse.model_validate(current_user)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.db.repositories import UserRepository
from app.database import get_async_session

router = APIRouter(prefix="/users", tags=["users"])

def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return UserRepository(session)

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, repo: UserRepository = Depends(get_user_repository)):
    user = await repo.create(username=user_create.username, email=user_create.email)
    return user

@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(user_id: int, repo: UserRepository = Depends(get_user_repository)):
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserRead])
async def get_users(repo: UserRepository = Depends(get_user_repository)):
    return await repo.get_all()

@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user_update: UserUpdate, repo: UserRepository = Depends(get_user_repository)):
    user = await repo.update(user_id, username=user_update.username, email=user_update.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, repo: UserRepository = Depends(get_user_repository)):
    deleted = await repo.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
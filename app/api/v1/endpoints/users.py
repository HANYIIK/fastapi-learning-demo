"""
用户管理相关的 API 端点
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user, get_current_active_user
from app.core.database import get_db
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取用户列表
    
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    """
    # 这里应该从数据库查询用户
    # 为了演示，我们返回模拟数据
    users = [
        User(id=1, username="admin", email="admin@example.com", is_active=True),
        User(id=2, username="user1", email="user1@example.com", is_active=True),
        User(id=3, username="user2", email="user2@example.com", is_active=True),
    ]
    return users[skip : skip + limit]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    根据 ID 获取用户信息
    
    - **user_id**: 用户 ID
    """
    # 这里应该从数据库查询用户
    # 为了演示，我们返回模拟数据
    if user_id == 1:
        return User(id=1, username="admin", email="admin@example.com", is_active=True)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )


@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    创建新用户
    
    - **user**: 用户信息
    """
    # 这里应该保存用户到数据库
    # 为了演示，我们直接返回
    new_user = User(
        id=4,
        username=user.username,
        email=user.email,
        is_active=user.is_active
    )
    return new_user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    更新用户信息
    
    - **user_id**: 用户 ID
    - **user_update**: 更新的用户信息
    """
    # 这里应该更新数据库中的用户
    # 为了演示，我们直接返回
    updated_user = User(
        id=user_id,
        username=user_update.username or "updated_user",
        email=user_update.email or "updated@example.com",
        is_active=user_update.is_active if user_update.is_active is not None else True
    )
    return updated_user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    删除用户
    
    - **user_id**: 用户 ID
    """
    # 这里应该从数据库删除用户
    # 为了演示，我们直接返回成功
    return {"message": f"用户 {user_id} 已删除"} 
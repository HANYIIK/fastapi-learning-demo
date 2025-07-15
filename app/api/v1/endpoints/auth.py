"""
认证相关的 API 端点
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.auth import verify_password, create_access_token, get_current_user
from app.core.config import settings
from app.core.database import get_db
from app.schemas.user import Token, UserResponse
from app.models.user import User

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    用户登录接口
    
    - **username**: 用户名
    - **password**: 密码
    """
    # 这里应该从数据库验证用户
    # 为了演示，我们使用硬编码的用户
    if form_data.username != "admin" or form_data.password != "password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse)
async def register(
    username: str,
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    """
    用户注册接口
    
    - **username**: 用户名
    - **email**: 邮箱
    - **password**: 密码
    """
    # 这里应该检查用户是否已存在
    # 为了演示，我们直接返回成功
    user = User(
        username=username,
        email=email,
        hashed_password="hashed_password_here"
    )
    
    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    获取当前用户信息
    """
    return current_user 
"""
认证相关的 API 端点 - MongoDB 版本
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.auth import verify_password, create_access_token, get_current_user, get_password_hash, get_user_by_username
from app.core.config import settings
from app.core.database import get_database
from app.models.user import UserResponse, UserCreate, UserDocument, Token
from loguru import logger

router = APIRouter()

# 获取数据库依赖
async def get_database_dependency():
    database = get_database()
    if database is None:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    return database

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    database = Depends(get_database_dependency)
):
    """
    用户登录接口
    
    - **username**: 用户名
    - **password**: 密码
    """
    try:
        # 从数据库获取用户
        user = await get_user_by_username(form_data.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 验证密码
        if not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 检查用户是否激活
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户已被禁用"
            )
        
        # 创建访问令牌
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"登录失败: {e}")
        raise HTTPException(status_code=500, detail="登录失败")


@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    database = Depends(get_database_dependency)
):
    """
    用户注册接口
    
    - **user_data**: 用户注册信息
    """
    try:
        # 检查用户名是否已存在
        existing_user = await database.users.find_one({"username": user_data.username})
        if existing_user:
            raise HTTPException(status_code=400, detail="用户名已存在")
        
        # 检查邮箱是否已存在
        existing_email = await database.users.find_one({"email": user_data.email})
        if existing_email:
            raise HTTPException(status_code=400, detail="邮箱已存在")
        
        # 创建新用户，显式设置中国时间
        hashed_password = get_password_hash(user_data.password)
        user_doc = UserDocument(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            is_active=user_data.is_active,
            is_superuser=user_data.is_superuser
        )
        
        result = await database.users.insert_one(user_doc.dict(by_alias=True))
        user_doc.id = result.inserted_id
        
        return UserResponse(
            id=str(user_doc.id),
            username=user_doc.username,
            email=user_doc.email,
            is_active=user_doc.is_active,
            is_superuser=user_doc.is_superuser,
            created_at=user_doc.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"注册失败: {e}")
        raise HTTPException(status_code=500, detail="注册失败")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: UserDocument = Depends(get_current_user)
):
    """
    获取当前用户信息
    """
    return UserResponse(
        id=str(current_user.id),
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        created_at=current_user.created_at
    ) 
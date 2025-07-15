"""
用户管理相关的 API 端点 - MongoDB 版本
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from datetime import datetime

from app.core.auth import get_current_user, get_current_active_user, get_password_hash
from app.core.database import get_database
from app.models.user import UserDocument
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from loguru import logger

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: UserDocument = Depends(get_current_active_user)
):
    """
    获取用户列表
    
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    """
    database = get_database()
    if database is None:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        cursor = database.users.find().skip(skip).limit(limit)
        users = []
        async for user_data in cursor:
            # 确保数据格式正确
            user_data["id"] = user_data.pop("_id", None)
            user_doc = UserDocument(**user_data)
            users.append(UserResponse(
                id=str(user_doc.id),
                username=user_doc.username,
                email=user_doc.email,
                is_active=user_doc.is_active,
                is_superuser=user_doc.is_superuser,
                created_at=user_doc.created_at
            ))
        return users
    except Exception as e:
        logger.error(f"获取用户列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取用户列表失败")


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: UserDocument = Depends(get_current_active_user)
):
    """
    根据 ID 获取用户信息
    
    - **user_id**: 用户 ID
    """
    database = get_database()
    if database is None:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="无效的用户ID")
        
        user_data = await database.users.find_one({"_id": ObjectId(user_id)})
        if not user_data:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 确保数据格式正确
        user_data["id"] = user_data.pop("_id", None)
        user_doc = UserDocument(**user_data)
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
        logger.error(f"获取用户失败: {e}")
        raise HTTPException(status_code=500, detail="获取用户失败")


@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    current_user: UserDocument = Depends(get_current_active_user)
):
    """
    创建新用户
    
    - **user**: 用户信息
    """
    database = get_database()
    if database is None:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        # 检查用户名是否已存在
        existing_user = await database.users.find_one({"username": user.username})
        if existing_user:
            raise HTTPException(status_code=400, detail="用户名已存在")
        
        # 检查邮箱是否已存在
        existing_email = await database.users.find_one({"email": user.email})
        if existing_email:
            raise HTTPException(status_code=400, detail="邮箱已存在")
        
        # 创建新用户
        hashed_password = get_password_hash(user.password)
        user_doc = UserDocument(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            is_active=user.is_active,
            is_superuser=user.is_superuser
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
        logger.error(f"创建用户失败: {e}")
        raise HTTPException(status_code=500, detail="创建用户失败")


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user: UserDocument = Depends(get_current_active_user)
):
    """
    更新用户信息
    
    - **user_id**: 用户 ID
    - **user_update**: 更新的用户信息
    """
    database = get_database()
    if database is None:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="无效的用户ID")
        
        # 检查用户是否存在
        existing_user = await database.users.find_one({"_id": ObjectId(user_id)})
        if not existing_user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 构建更新数据
        update_data = {}
        if user_update.username is not None:
            # 检查新用户名是否已被其他用户使用
            if user_update.username != existing_user["username"]:
                username_exists = await database.users.find_one({"username": user_update.username})
                if username_exists:
                    raise HTTPException(status_code=400, detail="用户名已存在")
            update_data["username"] = user_update.username
        
        if user_update.email is not None:
            # 检查新邮箱是否已被其他用户使用
            if user_update.email != existing_user["email"]:
                email_exists = await database.users.find_one({"email": user_update.email})
                if email_exists:
                    raise HTTPException(status_code=400, detail="邮箱已存在")
            update_data["email"] = user_update.email
        
        if user_update.password is not None:
            update_data["hashed_password"] = get_password_hash(user_update.password)
        
        if user_update.is_active is not None:
            update_data["is_active"] = user_update.is_active
        
        update_data["updated_at"] = datetime.utcnow()
        
        # 更新用户
        await database.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        # 获取更新后的用户
        updated_user_data = await database.users.find_one({"_id": ObjectId(user_id)})
        if not updated_user_data:
            raise HTTPException(status_code=404, detail="用户不存在")
        # 确保数据格式正确
        updated_user_data["id"] = updated_user_data.pop("_id", None)
        updated_user = UserDocument(**updated_user_data)
        
        return UserResponse(
            id=str(updated_user.id),
            username=updated_user.username,
            email=updated_user.email,
            is_active=updated_user.is_active,
            is_superuser=updated_user.is_superuser,
            created_at=updated_user.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新用户失败: {e}")
        raise HTTPException(status_code=500, detail="更新用户失败")


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    current_user: UserDocument = Depends(get_current_active_user)
):
    """
    删除用户
    
    - **user_id**: 用户 ID
    """
    database = get_database()
    if database is None:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="无效的用户ID")
        
        # 检查用户是否存在
        existing_user = await database.users.find_one({"_id": ObjectId(user_id)})
        if not existing_user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 删除用户
        await database.users.delete_one({"_id": ObjectId(user_id)})
        
        return {"message": f"用户 {user_id} 已删除"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除用户失败: {e}")
        raise HTTPException(status_code=500, detail="删除用户失败") 
"""
物品管理相关的 API 端点 - MongoDB 版本
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime

from app.core.auth import get_current_active_user
from app.core.database import get_database
from app.models.user import UserDocument
from loguru import logger

router = APIRouter()


# 物品相关的 Pydantic 模型
class ItemBase(BaseModel):
    """物品基础模型"""
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)


class ItemCreate(ItemBase):
    """创建物品模型"""
    pass


class ItemUpdate(BaseModel):
    """更新物品模型"""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)


class ItemResponse(ItemBase):
    """物品响应模型"""
    id: str
    owner_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {ObjectId: str}


# MongoDB 物品文档模型
class ItemDocument(BaseModel):
    """MongoDB 物品文档模型"""
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    title: str
    description: Optional[str] = None
    price: float
    owner_id: ObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


@router.get("/", response_model=List[ItemResponse])
async def get_items(
    skip: int = 0,
    limit: int = 100,
    current_user: UserDocument = Depends(get_current_active_user)
):
    """
    获取物品列表
    
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    """
    database = get_database()
    if database is None:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        cursor = database.items.find().skip(skip).limit(limit)
        items = []
        async for item_data in cursor:
            # 确保数据格式正确
            item_data["id"] = item_data.pop("_id", None)
            item_doc = ItemDocument(**item_data)
            items.append(ItemResponse(
                id=str(item_doc.id),
                title=item_doc.title,
                description=item_doc.description,
                price=item_doc.price,
                owner_id=str(item_doc.owner_id),
                created_at=item_doc.created_at
            ))
        return items
    except Exception as e:
        logger.error(f"获取物品列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取物品列表失败")


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: str,
    current_user: UserDocument = Depends(get_current_active_user)
):
    """
    根据 ID 获取物品信息
    
    - **item_id**: 物品 ID
    """
    database = get_database()
    if database is None:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        if not ObjectId.is_valid(item_id):
            raise HTTPException(status_code=400, detail="无效的物品ID")
        
        item_data = await database.items.find_one({"_id": ObjectId(item_id)})
        if not item_data:
            raise HTTPException(status_code=404, detail="物品不存在")
        
        # 确保数据格式正确
        item_data["id"] = item_data.pop("_id", None)
        item_doc = ItemDocument(**item_data)
        return ItemResponse(
            id=str(item_doc.id),
            title=item_doc.title,
            description=item_doc.description,
            price=item_doc.price,
            owner_id=str(item_doc.owner_id),
            created_at=item_doc.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取物品失败: {e}")
        raise HTTPException(status_code=500, detail="获取物品失败")


@router.post("/", response_model=ItemResponse)
async def create_item(
    item: ItemCreate,
    current_user: UserDocument = Depends(get_current_active_user)
):
    """
    创建新物品
    
    - **item**: 物品信息
    """
    database = get_database()
    if database is None:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        item_doc = ItemDocument(
            title=item.title,
            description=item.description,
            price=item.price,
            owner_id=current_user.id if current_user.id else ObjectId()
        )
        
        result = await database.items.insert_one(item_doc.dict(by_alias=True))
        item_doc.id = result.inserted_id
        
        return ItemResponse(
            id=str(item_doc.id),
            title=item_doc.title,
            description=item_doc.description,
            price=item_doc.price,
            owner_id=str(item_doc.owner_id),
            created_at=item_doc.created_at
        )
    except Exception as e:
        logger.error(f"创建物品失败: {e}")
        raise HTTPException(status_code=500, detail="创建物品失败")


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: str,
    item_update: ItemUpdate,
    current_user: UserDocument = Depends(get_current_active_user)
):
    """
    更新物品信息
    
    - **item_id**: 物品 ID
    - **item_update**: 更新的物品信息
    """
    database = get_database()
    if database is None:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        if not ObjectId.is_valid(item_id):
            raise HTTPException(status_code=400, detail="无效的物品ID")
        
        # 检查物品是否存在
        existing_item = await database.items.find_one({"_id": ObjectId(item_id)})
        if not existing_item:
            raise HTTPException(status_code=404, detail="物品不存在")
        
        # 检查权限
        if existing_item["owner_id"] != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="没有权限修改此物品"
            )
        
        # 构建更新数据
        update_data = {}
        if item_update.title is not None:
            update_data["title"] = item_update.title
        if item_update.description is not None:
            update_data["description"] = item_update.description
        if item_update.price is not None:
            update_data["price"] = item_update.price
        
        update_data["updated_at"] = datetime.utcnow()
        
        # 更新物品
        await database.items.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": update_data}
        )
        
        # 获取更新后的物品
        updated_item_data = await database.items.find_one({"_id": ObjectId(item_id)})
        if not updated_item_data:
            raise HTTPException(status_code=404, detail="物品不存在")
        # 确保数据格式正确
        updated_item_data["id"] = updated_item_data.pop("_id", None)
        updated_item = ItemDocument(**updated_item_data)
        
        return ItemResponse(
            id=str(updated_item.id),
            title=updated_item.title,
            description=updated_item.description,
            price=updated_item.price,
            owner_id=str(updated_item.owner_id),
            created_at=updated_item.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新物品失败: {e}")
        raise HTTPException(status_code=500, detail="更新物品失败")


@router.delete("/{item_id}")
async def delete_item(
    item_id: str,
    current_user: UserDocument = Depends(get_current_active_user)
):
    """
    删除物品
    
    - **item_id**: 物品 ID
    """
    database = get_database()
    if database is None:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        if not ObjectId.is_valid(item_id):
            raise HTTPException(status_code=400, detail="无效的物品ID")
        
        # 检查物品是否存在
        existing_item = await database.items.find_one({"_id": ObjectId(item_id)})
        if not existing_item:
            raise HTTPException(status_code=404, detail="物品不存在")
        
        # 检查权限
        if existing_item["owner_id"] != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="没有权限删除此物品"
            )
        
        # 删除物品
        await database.items.delete_one({"_id": ObjectId(item_id)})
        
        return {"message": f"物品 '{existing_item['title']}' 已删除"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除物品失败: {e}")
        raise HTTPException(status_code=500, detail="删除物品失败") 
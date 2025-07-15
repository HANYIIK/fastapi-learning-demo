"""
物品管理相关的 API 端点
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.auth import get_current_active_user
from app.core.database import get_db
from app.models.user import User

router = APIRouter()


# 物品相关的 Pydantic 模型
class ItemBase(BaseModel):
    """物品基础模型"""
    title: str
    description: Optional[str] = None
    price: float


class ItemCreate(ItemBase):
    """创建物品模型"""
    pass


class ItemUpdate(BaseModel):
    """更新物品模型"""
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class ItemResponse(ItemBase):
    """物品响应模型"""
    id: int
    owner_id: int
    
    class Config:
        from_attributes = True


# 模拟数据
items_db = [
    {"id": 1, "title": "笔记本电脑", "description": "高性能笔记本电脑", "price": 5999.0, "owner_id": 1},
    {"id": 2, "title": "手机", "description": "智能手机", "price": 2999.0, "owner_id": 1},
    {"id": 3, "title": "耳机", "description": "无线蓝牙耳机", "price": 299.0, "owner_id": 2},
]


@router.get("/", response_model=List[ItemResponse])
async def get_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取物品列表
    
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    """
    return items_db[skip : skip + limit]


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    根据 ID 获取物品信息
    
    - **item_id**: 物品 ID
    """
    for item in items_db:
        if item["id"] == item_id:
            return item
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="物品不存在"
    )


@router.post("/", response_model=ItemResponse)
async def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    创建新物品
    
    - **item**: 物品信息
    """
    new_item = {
        "id": len(items_db) + 1,
        "title": item.title,
        "description": item.description,
        "price": item.price,
        "owner_id": current_user.id
    }
    items_db.append(new_item)
    return new_item


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item_update: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    更新物品信息
    
    - **item_id**: 物品 ID
    - **item_update**: 更新的物品信息
    """
    for item in items_db:
        if item["id"] == item_id:
            if item["owner_id"] != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="没有权限修改此物品"
                )
            
            # 更新物品信息
            if item_update.title is not None:
                item["title"] = item_update.title
            if item_update.description is not None:
                item["description"] = item_update.description
            if item_update.price is not None:
                item["price"] = item_update.price
            
            return item
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="物品不存在"
    )


@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    删除物品
    
    - **item_id**: 物品 ID
    """
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            if item["owner_id"] != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="没有权限删除此物品"
                )
            
            deleted_item = items_db.pop(i)
            return {"message": f"物品 '{deleted_item['title']}' 已删除"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="物品不存在"
    ) 
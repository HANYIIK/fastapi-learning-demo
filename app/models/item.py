"""
物品数据模型 - MongoDB 版本
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from app.models.common import PyObjectId


# Pydantic 模型用于 API
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


# MongoDB 文档模型
class ItemDocument(BaseModel):
    """MongoDB 物品文档模型"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: Optional[str] = None
    price: float
    owner_id: PyObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str} 
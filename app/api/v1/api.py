"""
API v1 主路由
"""
from fastapi import APIRouter

from app.api.v1.endpoints import users, auth, items

api_router = APIRouter()

# 注册各个模块的路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户管理"])
api_router.include_router(items.router, prefix="/items", tags=["物品管理"]) 
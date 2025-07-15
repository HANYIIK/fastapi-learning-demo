"""
FastAPI 学习项目主应用文件
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import uvicorn
from loguru import logger

from app.core.config import settings
from app.core.database import init_db, close_mongo_connection
from app.api.v1.api import api_router
from app.core.auth import get_current_user

# 安全认证
security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("🚀 启动 FastAPI 应用...")
    # 初始化数据库
    await init_db()
    logger.info("✅ MongoDB 数据库初始化完成")
    
    yield
    
    # 关闭时执行
    logger.info("🛑 关闭 FastAPI 应用...")
    # 关闭数据库连接
    await close_mongo_connection()


# 创建 FastAPI 应用实例
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """根路径 - 欢迎页面"""
    return {
        "message": settings.DESCRIPTION,
        "docs": "/docs",
        "redoc": "/redoc",
        "version": settings.VERSION
    }


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "message": "服务运行正常"}


@app.get("/protected")
async def protected_route(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user = Depends(get_current_user)
):
    """受保护的路由示例"""
    return {
        "message": "这是一个受保护的路由",
        "user": current_user.username,
        "token": credentials.credentials[:20] + "..."  # 只显示前20个字符
    }


# 注册 API 路由
app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level="info"
    ) 
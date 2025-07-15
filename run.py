#!/usr/bin/env python3
"""
FastAPI 学习项目运行脚本
"""
import uvicorn
from loguru import logger
from app.core.config import settings

if __name__ == "__main__":
    logger.info("🚀 启动 FastAPI 学习项目...")
    logger.info(f"配置信息 - HOST: {settings.HOST}, PORT: {settings.PORT}")
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level="info",
        access_log=True
    ) 
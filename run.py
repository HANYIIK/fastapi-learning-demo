#!/usr/bin/env python3
"""
FastAPI 学习项目运行脚本
"""
import uvicorn
from loguru import logger

if __name__ == "__main__":
    logger.info("🚀 启动 FastAPI 学习项目...")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    ) 
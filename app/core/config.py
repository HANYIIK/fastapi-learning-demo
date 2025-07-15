"""
应用配置管理
"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """应用配置类
    
    配置优先级：
    1. 环境变量（最高）
    2. .env 文件
    3. 默认值（最低）
    
    生产环境请通过环境变量或 .env 文件覆盖敏感配置
    """
    
    # 项目基本信息
    PROJECT_NAME: str = "FastAPI Learning Project"
    DESCRIPTION: str = "FastAPI 学习项目"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # 数据库配置
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "fastapi-learning-db"
    
    # 安全配置
    SECRET_KEY: str = "change-this-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS 配置
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings() 
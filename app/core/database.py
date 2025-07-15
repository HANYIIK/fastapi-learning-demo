"""
数据库连接和初始化
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from loguru import logger

from app.core.config import settings

# 创建数据库引擎
if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite 异步引擎
    engine = create_async_engine(
        settings.DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///"),
        echo=settings.DEBUG
    )
    SessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False
    )
else:
    # PostgreSQL 异步引擎
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG
    )
    SessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False
    )

# 创建基础模型类
Base = declarative_base()

# 元数据
metadata = MetaData()


async def init_db():
    """初始化数据库"""
    try:
        # 创建所有表
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ 数据库表创建成功")
    except Exception as e:
        logger.error(f"❌ 数据库初始化失败: {e}")
        raise


async def get_db():
    """获取数据库会话"""
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


async def get_async_db():
    """获取异步数据库会话"""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 
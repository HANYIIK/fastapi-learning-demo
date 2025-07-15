"""
MongoDB 数据库连接和初始化
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING
from loguru import logger

from app.core.config import settings

# MongoDB 客户端
client = None
database = None


async def connect_to_mongo():
    """连接到 MongoDB"""
    global client, database
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        database = client[settings.MONGODB_DB_NAME]
        
        # 测试连接
        await client.admin.command('ping')
        logger.info("✅ MongoDB 连接成功")
        
        # 创建索引
        await create_indexes()
        
    except Exception as e:
        logger.error(f"❌ MongoDB 连接失败: {e}")
        raise


async def close_mongo_connection():
    """关闭 MongoDB 连接"""
    global client
    if client:
        client.close()
        logger.info("🛑 MongoDB 连接已关闭")


async def create_indexes():
    """创建数据库索引"""
    if database is None:
        logger.error("❌ 数据库未连接")
        return
        
    try:
        # 用户集合索引
        await database.users.create_index([("username", ASCENDING)], unique=True)
        await database.users.create_index([("email", ASCENDING)], unique=True)
        await database.users.create_index([("created_at", DESCENDING)])
        
        # 物品集合索引
        await database.items.create_index([("title", ASCENDING)])
        await database.items.create_index([("owner_id", ASCENDING)])
        await database.items.create_index([("created_at", DESCENDING)])
        
        logger.info("✅ 数据库索引创建成功")
    except Exception as e:
        logger.error(f"❌ 创建索引失败: {e}")
        raise


async def init_db():
    """初始化数据库"""
    try:
        await connect_to_mongo()
        logger.info("✅ 数据库初始化完成")
    except Exception as e:
        logger.error(f"❌ 数据库初始化失败: {e}")
        raise


def get_database():
    """获取数据库实例"""
    return database


async def get_collection(collection_name: str):
    """获取集合实例"""
    if database is None:
        return None
    return database[collection_name] 
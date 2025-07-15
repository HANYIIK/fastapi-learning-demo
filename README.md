# FastAPI 学习项目

这是一个用于学习 FastAPI 框架的完整项目模板，包含了现代 Web API 开发中常用的功能和最佳实践。

## 🚀 项目特性

- **FastAPI 框架**: 现代化的 Python Web 框架
- **JWT 认证**: 基于 JWT 的用户认证系统
- **MongoDB 数据库**: 使用 Motor 异步 MongoDB 驱动
- **API 文档**: 自动生成的 Swagger/OpenAPI 文档
- **依赖注入**: 使用 FastAPI 的 Depends 系统
- **数据验证**: Pydantic 模型验证
- **CORS 支持**: 跨域资源共享
- **日志系统**: 结构化日志记录（Loguru）
- **异步支持**: 全异步数据库操作
- **测试支持**: 单元测试框架

## 📁 项目结构

```
fastapi-learning-project/
├── app/                    # 应用主目录
│   ├── api/               # API 路由
│   │   └── v1/           # API v1 版本
│   │       ├── endpoints/ # API 端点
│   │       └── api.py    # 主路由
│   ├── core/             # 核心配置
│   │   ├── auth.py      # 认证模块
│   │   ├── config.py    # 配置管理
│   │   └── database.py  # MongoDB 连接
│   ├── models/          # 数据模型
│   ├── schemas/         # Pydantic 模式
│   ├── services/        # 业务逻辑
│   └── utils/           # 工具函数
├── tests/               # 测试文件
├── main.py             # 应用入口
├── run.py              # 运行脚本
├── requirements.txt    # 依赖包
└── README.md          # 项目说明
```

## ⚙️ 项目配置

### MongoDB 配置

项目默认配置：
- **数据库 URL**: `mongodb://localhost:27017`
- **数据库名称**: `fastapi-learning-db`
- **端口**: `27017`

可在 `app/core/config.py` 中修改配置：
```python
MONGODB_URL: str = "mongodb://localhost:27017"
MONGODB_DB_NAME: str = "fastapi-learning-db"
```

## 🛠️ 安装和运行

### 1. 安装 MongoDB

```bash
# 使用 Homebrew 安装 MongoDB
brew tap mongodb/brew
brew install mongodb-community

# 或下载官方安装包
# https://www.mongodb.com/try/download/community
```

### 2. 创建虚拟环境

```bash
# 使用 conda
conda create -n fastapi-learning python=3.9
conda activate fastapi-learning

# 或使用 venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动 MongoDB

```bash
# 使用 Homebrew 启动 MongoDB
brew services start mongodb-community

# 或手动启动 MongoDB
mongod --dbpath /path/to/your/data/directory --port 27017

# 检查 MongoDB 是否运行
ps aux | grep mongod
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 运行应用

```bash
# 开发模式（推荐）
python run.py

# 或直接运行主文件
python main.py

# 或使用 uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. 访问应用

- **API 文档**: http://localhost:8000/docs
- **ReDoc 文档**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/health
- **根路径**: http://localhost:8000/ - 欢迎页面
- **受保护路由**: http://localhost:8000/protected - 需要认证

## 📚 API 端点

### 认证相关

- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/register` - 用户注册
- `GET /api/v1/auth/me` - 获取当前用户信息

### 系统相关

- `GET /` - 欢迎页面
- `GET /health` - 健康检查
- `GET /protected` - 受保护的路由（需要认证）

### 用户管理

- `GET /api/v1/users/` - 获取用户列表
- `GET /api/v1/users/{user_id}` - 获取用户详情
- `POST /api/v1/users/` - 创建用户
- `PUT /api/v1/users/{user_id}` - 更新用户
- `DELETE /api/v1/users/{user_id}` - 删除用户

### 物品管理

- `GET /api/v1/items/` - 获取物品列表
- `GET /api/v1/items/{item_id}` - 获取物品详情
- `POST /api/v1/items/` - 创建物品
- `PUT /api/v1/items/{item_id}` - 更新物品
- `DELETE /api/v1/items/{item_id}` - 删除物品

## 🧪 API 测试命令

### 🔐 认证相关接口

#### 1. 用户登录
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

#### 2. 用户注册
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123",
    "is_active": true,
    "is_superuser": false
  }'
```

#### 3. 获取当前用户信息
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1MjU2NjkwN30.uwolFA7g0j3AYpqR4hqAZ5bTF8NNrDgFoQoAoPMG2K0"
```

### 👥 用户管理接口

#### 4. 获取用户列表
```bash
curl -X GET "http://localhost:8000/api/v1/users/?skip=0&limit=10" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1MjU2NjkwN30.uwolFA7g0j3AYpqR4hqAZ5bTF8NNrDgFoQoAoPMG2K0"
```

#### 5. 根据ID获取用户
```bash
curl -X GET "http://localhost:8000/api/v1/users/USER_ID_HERE" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1MjU2NjkwN30.uwolFA7g0j3AYpqR4hqAZ5bTF8NNrDgFoQoAoPMG2K0"
```

#### 6. 创建新用户
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1MjU2NjkwN30.uwolFA7g0j3AYpqR4hqAZ5bTF8NNrDgFoQoAoPMG2K0" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "password123",
    "is_active": true,
    "is_superuser": false
  }'
```

#### 7. 更新用户信息
```bash
curl -X PUT "http://localhost:8000/api/v1/users/USER_ID_HERE" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1MjU2NjkwN30.uwolFA7g0j3AYpqR4hqAZ5bTF8NNrDgFoQoAoPMG2K0" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "updateduser",
    "email": "updated@example.com",
    "password": "newpassword123",
    "is_active": true
  }'
```

#### 8. 删除用户
```bash
curl -X DELETE "http://localhost:8000/api/v1/users/USER_ID_HERE" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1MjU2NjkwN30.uwolFA7g0j3AYpqR4hqAZ5bTF8NNrDgFoQoAoPMG2K0"
```

### 📦 物品管理接口

#### 9. 获取物品列表
```bash
curl -X GET "http://localhost:8000/api/v1/items/?skip=0&limit=10" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1MjU2NjkwN30.uwolFA7g0j3AYpqR4hqAZ5bTF8NNrDgFoQoAoPMG2K0"
```

#### 10. 根据ID获取物品
```bash
curl -X GET "http://localhost:8000/api/v1/items/ITEM_ID_HERE" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1MjU2NjkwN30.uwolFA7g0j3AYpqR4hqAZ5bTF8NNrDgFoQoAoPMG2K0"
```

#### 11. 创建新物品
```bash
curl -X POST "http://localhost:8000/api/v1/items/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1MjU2NjkwN30.uwolFA7g0j3AYpqR4hqAZ5bTF8NNrDgFoQoAoPMG2K0" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "测试物品",
    "description": "这是一个测试物品",
    "price": 99.99
  }'
```

#### 12. 更新物品信息
```bash
curl -X PUT "http://localhost:8000/api/v1/items/ITEM_ID_HERE" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1MjU2NjkwN30.uwolFA7g0j3AYpqR4hqAZ5bTF8NNrDgFoQoAoPMG2K0" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "更新后的物品",
    "description": "这是更新后的描述",
    "price": 199.99
  }'
```

#### 13. 删除物品
```bash
curl -X DELETE "http://localhost:8000/api/v1/items/ITEM_ID_HERE" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1MjU2NjkwN30.uwolFA7g0j3AYpqR4hqAZ5bTF8NNrDgFoQoAoPMG2K0"
```

### 🔄 获取新 Token 的快捷命令

```bash
# 登录获取新token
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" | jq -r '.access_token')

echo "新token: $TOKEN"
```

### 📝 使用说明

1. **Token 有效期**：JWT token 有30分钟有效期，过期后需要重新登录获取新token
2. **替换 ID**：将 `USER_ID_HERE` 和 `ITEM_ID_HERE` 替换为实际的用户ID和物品ID
3. **权限说明**：
   - 只有超级用户才能创建、更新、删除其他用户
   - 用户只能修改自己创建的物品
   - 所有接口都需要有效的 JWT token

### 🔧 调试命令

```bash
# 查看详细响应
curl -v http://localhost:8000/

# 保存响应到文件
curl http://localhost:8000/ > response.json

# 检查 MongoDB 连接
mongosh
```

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_auth.py

# 运行测试并显示覆盖率
pytest --cov=app
```

## 📝 学习要点

### 1. 依赖注入 (Depends)

```python
@router.get("/protected")
async def protected_route(
    current_user: User = Depends(get_current_user)
):
    return {"user": current_user.username}
```

### 2. 数据验证 (Pydantic)

```python
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
```

### 3. 数据库操作 (MongoDB)

```python
# 获取数据库实例
database = get_database()

# 获取集合
users_collection = database.users

# 查询用户
user = await users_collection.find_one({"username": "testuser"})

# 插入文档
result = await users_collection.insert_one(user_doc.dict(by_alias=True))

# 更新文档
await users_collection.update_one(
    {"_id": ObjectId(user_id)},
    {"$set": update_data}
)

# 删除文档
await users_collection.delete_one({"_id": ObjectId(user_id)})
```

### 4. 错误处理

```python
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="用户不存在"
)
```

## 🔧 开发工具

### 代码格式化

```bash
# 使用 black 格式化代码
black app/

# 使用 isort 排序导入
isort app/

# 使用 flake8 检查代码风格
flake8 app/
```

### MongoDB 管理

```bash
# 连接到 MongoDB
mongosh

# 查看数据库
show dbs

# 使用项目数据库
use fastapi-learning-db

# 查看集合
show collections

# 查看用户数据
db.users.find()

# 查看物品数据
db.items.find()

# 查看索引
db.users.getIndexes()
db.items.getIndexes()
```

## 📖 学习资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Pydantic 文档](https://pydantic-docs.helpmanual.io/)
- [MongoDB 文档](https://docs.mongodb.com/)
- [Motor (MongoDB 异步驱动)](https://motor.readthedocs.io/)
- [JWT 认证](https://jwt.io/)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## �� 许可证

MIT License 
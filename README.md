# FastAPI 学习项目

这是一个用于学习 FastAPI 框架的完整项目模板，包含了现代 Web API 开发中常用的功能和最佳实践。

## 🚀 项目特性

- **FastAPI 框架**: 现代化的 Python Web 框架
- **JWT 认证**: 基于 JWT 的用户认证系统
- **数据库集成**: SQLAlchemy 异步 ORM 支持
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
│   │   └── database.py  # 数据库连接
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

## 🛠️ 安装和运行

### 1. 创建虚拟环境

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

### 3. 配置环境变量

```bash
# 复制环境变量示例文件
cp env.example .env

# 编辑 .env 文件，修改配置
```

### 4. 运行应用

```bash
# 开发模式（推荐）
python run.py

# 或直接运行主文件
python main.py

# 或使用 uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 访问应用

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

## 🔐 认证示例

### 1. 登录获取 Token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=password"
```

### 2. 使用 Token 访问受保护的接口

```bash
curl -X GET "http://localhost:8000/api/v1/users/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
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

### 3. 数据库操作 (SQLAlchemy)

```python
async def get_db():
    """获取数据库会话"""
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
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

### 数据库迁移

```bash
# 初始化 Alembic
alembic init alembic

# 创建迁移
alembic revision --autogenerate -m "Add user table"

# 执行迁移
alembic upgrade head
```

## 📖 学习资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Pydantic 文档](https://pydantic-docs.helpmanual.io/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
- [JWT 认证](https://jwt.io/)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## �� 许可证

MIT License 
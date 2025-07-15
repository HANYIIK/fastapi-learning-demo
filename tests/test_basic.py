"""
基础测试文件
"""
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_root():
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """测试健康检查"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_docs_available():
    """测试文档是否可用"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_available():
    """测试 ReDoc 是否可用"""
    response = client.get("/redoc")
    assert response.status_code == 200 
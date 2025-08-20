# test_main.py
from initDB import db_config, init_db, db_session
import pytest

def test_database_connection():
    # 测试数据库连接配置是否正确
    assert db_config["database"] == "reservation_system"  # 检查数据库名是否正确

def test_init_db():
    # 测试初始化表结构
    init_db()
    # 可进一步查询表是否存在（略）
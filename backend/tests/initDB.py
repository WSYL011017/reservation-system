# initDB.py
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 数据库连接配置（根据你的实际环境修改）
db_config = {
    'host': '39.103.56.52',       # 数据库主机地址
    'port': 3306,              # 数据库端口
    'user': 'root',            # 数据库用户名
    'password': 'Suyala1017..',  # 数据库密码
    'database': 'reservation_system'  # 数据库名（已创建的 reservation_system）
}

# SQLAlchemy 配置（与 Flask-SQLAlchemy 配合使用）
# 数据库连接 URL（格式：mysql+mysqldb://用户:密码@主机:端口/数据库名）
DATABASE_URI = f"mysql+mysqldb://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?charset=utf8mb4"

# 初始化 SQLAlchemy 引擎
engine = create_engine(DATABASE_URI, echo=False)  # echo=True 会打印 SQL 语句，调试用

# 创建会话工厂
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# 声明基类（所有模型类继承此类）
Base = declarative_base()
Base.query = db_session.query_property()  # 给模型类添加 query 属性，方便查询


def init_db():
    """初始化数据库：创建所有表结构（如果使用 SQLAlchemy 模型）"""
    # 导入所有模型类（确保模型类被加载，否则无法创建表）
    from app.models import User, Reservation, ServiceType, TimeSlot  # 根据你的模型路径修改
    Base.metadata.create_all(bind=engine)
    print("数据库表结构初始化完成")


def init_default_data():
    """添加默认数据（如初始服务类型、时间槽等）"""
    try:
        # 添加默认服务类型
        default_services = [
            {"name": "基础服务", "description": "标准服务流程", "duration_minutes": 60, "price": 99.00},
            {"name": "高级服务", "description": "包含额外增值服务", "duration_minutes": 90, "price": 199.00}
        ]
        for service in default_services:
            # 检查是否已存在，避免重复添加
            if not ServiceType.query.filter_by(name=service["name"]).first():
                new_service = ServiceType(
                    name=service["name"],
                    description=service["description"],
                    duration_minutes=service["duration_minutes"],
                    price=service["price"]
                )
                db_session.add(new_service)
        db_session.commit()
        print("默认服务类型添加完成")
    except Exception as e:
        db_session.rollback()
        print(f"添加默认数据失败：{str(e)}")


def connect_mysql():
    """直接使用 mysql.connector 连接数据库（备用方法，非必须）"""
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"成功连接到 MySQL 服务器，版本：{db_info}")
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print(f"当前数据库：{record[0]}")
            return connection
    except Error as e:
        print(f"连接数据库失败：{e}")
    return connection


# 应用退出时关闭会话
def shutdown_session(exception=None):
    db_session.remove()
    print("数据库会话已关闭")

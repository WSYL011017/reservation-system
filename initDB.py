
import pymysql
from pymysql.cursors import DictCursor

def execute_sql_file(file_path, db_config):
    """
    执行SQL文件
    
    参数:
        file_path: SQL文件路径
        db_config: 数据库配置字典，包含host, port, user, password, db
    """
    # 读取SQL文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
    except Exception as e:
        print(f"读取SQL文件失败: {str(e)}")
        return

    # 连接数据库
    conn = None
    cursor = None
    try:
        # 建立连接
        conn = pymysql.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            db=db_config['db'],
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        cursor = conn.cursor()

        # 分割SQL语句（处理分号分隔的多个语句）
        sql_statements = sql_content.split(';')
        
        # 执行每个SQL语句
        for sql in sql_statements:
            sql = sql.strip()
            if sql:  # 跳过空语句
                try:
                    cursor.execute(sql)
                    print(f"执行成功: {sql[:50]}...")  # 只显示前50个字符
                except Exception as e:
                    print(f"执行失败: {sql[:50]}... 错误: {str(e)}")
                    conn.rollback()  # 回滚事务
                    return

        # 提交事务
        conn.commit()
        print("所有SQL语句执行完成并已提交")

    except Exception as e:
        print(f"数据库操作失败: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        # 关闭连接
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # 数据库配置
    db_config = {
        'host': '39.103.56.52',    # 数据库主机地址
        'port': 3306,           # 数据库端口
        'user': 'root',         # 数据库用户名
        'password': 'Suyala1017..',   # 数据库密码
        'db': 'reservation_system'         # 数据库名称
    }
    
    # SQL文件路径
    sql_file_path = 'database.sql'  # 替换为你的SQL文件路径
    
    # 执行SQL文件
    execute_sql_file(sql_file_path, db_config)

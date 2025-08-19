import socket
import pymysql
import time
from datetime import datetime

def test_server_reachability(host, port=3306, timeout=10):
    """测试服务器是否可达"""
    print(f"\n[{datetime.now()}] 测试服务器 {host}:{port} 可达性...")
    try:
        # 创建socket连接测试
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            start_time = time.time()
            result = s.connect_ex((host, port))
            end_time = time.time()
            
            if result == 0:
                print(f"✅ 服务器 {host}:{port} 可达，响应时间: {round((end_time - start_time) * 1000, 2)}ms")
                return True
            else:
                print(f"❌ 服务器 {host}:{port} 不可达，错误代码: {result}")
                return False
    except Exception as e:
        print(f"❌ 测试服务器可达性时出错: {str(e)}")
        return False

def test_mysql_connection(db_config, timeout=10):
    """测试MySQL数据库连接"""
    host = db_config['host']
    port = db_config.get('port', 3306)
    user = db_config['user']
    db_name = db_config.get('db', '未知数据库')
    
    print(f"\n[{datetime.now()}] 测试连接到 {host}:{port} 的 {db_name} 数据库...")
    conn = None
    try:
        start_time = time.time()
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=db_config['password'],
            db=db_config.get('db'),
            charset='utf8mb4',
            connect_timeout=timeout
        )
        end_time = time.time()
        
        print(f"✅ 成功连接到数据库！响应时间: {round((end_time - start_time) * 1000, 2)}ms")
        
        # 尝试执行简单查询
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()[0]
                print(f"数据库版本: {version}")
                
                cursor.execute("SELECT DATABASE()")
                current_db = cursor.fetchone()[0]
                print(f"当前数据库: {current_db}")
            return True
        except Exception as e:
            print(f"⚠️ 连接成功但执行查询出错: {str(e)}")
            return True
            
    except pymysql.OperationalError as e:
        error_code, error_msg = e.args
        print(f"❌ 数据库连接失败 (错误代码: {error_code}): {error_msg}")
        print("可能的原因:")
        if error_code in (2003, 10061):
            print("- 服务器未运行或端口未开放")
            print("- 防火墙阻止了连接")
            print("- 主机地址或端口错误")
        elif error_code == 1045:
            print("- 用户名或密码错误")
            print("- 用户没有远程访问权限")
        elif error_code == 1049:
            print("- 数据库不存在")
        elif error_code == 2006:
            print("- 连接超时，服务器响应太慢")
            print("- 服务器负载过高")
        return False
    except Exception as e:
        print(f"❌ 数据库连接时发生意外错误: {str(e)}")
        return False
    finally:
        if conn:
            try:
                conn.close()
                print("连接已关闭")
            except:
                pass

def main():
    print("=== MySQL数据库连接测试工具 ===")
    print("这个工具将帮助你诊断数据库连接超时问题\n")
    
    # 数据库配置 - 请根据实际情况修改
    db_config = {
        'host': input("请输入数据库主机地址: "),  # 例如: '192.168.1.100' 或 'db.example.com'
        'port': int(input("请输入数据库端口 (默认3306): ") or 3306),
        'user': input("请输入数据库用户名: "),
        'password': input("请输入数据库密码: "),
        'db': input("请输入数据库名称 (可选): ") or None
    }
    
    # 逐步测试
    # 1. 测试服务器可达性
    reachable = test_server_reachability(db_config['host'], db_config['port'])
    
    if not reachable:
        print("\n排查建议:")
        print("1. 检查服务器是否已启动")
        print("2. 确认主机地址和端口是否正确")
        print("3. 检查服务器防火墙是否允许该端口的连接")
        print("4. 尝试从命令行执行 ping 命令测试网络连通性")
        return
    
    # 2. 测试数据库连接
    connected = test_mysql_connection(db_config)
    
    if not connected:
        print("\n排查建议:")
        print("1. 确认MySQL服务是否正在运行")
        print("2. 检查MySQL配置文件是否允许远程连接 (bind-address)")
        print("3. 验证用户名和密码是否正确")
        print("4. 确认该用户具有远程访问权限 (可执行 GRANT ALL ON *.* TO 'user'@'%' IDENTIFIED BY 'password';)")
        print("5. 检查MySQL的max_connections设置是否已满")
        print("6. 查看MySQL错误日志获取更多信息")

def test():
    conn = pymysql.connect(
        host="39.103.56.52",
        port=3306,
        user="root",
        password="Suyala1017..",
        connect_timeout=30  # 延长超时时间（秒）
    )
if __name__ == "__main__":
    main()
    # test()
    
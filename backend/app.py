from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# 数据库配置
db_config = {
    'host': '39.103.56.52',
    'user': 'root',
    'password': 'Suyala1017..',
    'database': 'reservation_system',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    try:
        return pymysql.connect(**db_config)
    except Exception as e:
        print(f"数据库连接失败: {str(e)}")
        return None

# 统一的响应格式
def success_response(data=None, message='成功'):
    return jsonify({'code': 0, 'message': message, 'data': data or []})

def error_response(message, status_code=500):
    response = jsonify({'code': status_code, 'message': str(message)})
    response.status_code = status_code
    return response

# 健康检查
@app.route('/api/health', methods=['GET'])
def health_check():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return error_response('数据库连接失败')
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                return success_response(message='服务正常运行')
            else:
                return error_response('数据库查询失败')
    except Exception as e:
        return error_response(f'健康检查失败: {str(e)}')
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

# 获取服务类型
@app.route('/api/services', methods=['GET'])
def get_services():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return error_response('数据库连接失败')
            
        with conn.cursor() as cursor:
            sql = "SELECT * FROM service_types WHERE status = 'active' ORDER BY id"
            cursor.execute(sql)
            services = cursor.fetchall()
        return success_response(services)
    except Exception as e:
        return error_response(f'获取服务失败: {str(e)}')
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

# 获取时间槽
@app.route('/api/time-slots', methods=['GET'])
def get_time_slots():
    conn = None
    try:
        date = request.args.get('date')
        if not date:
            return error_response('请提供日期', status_code=400)
            
        conn = get_db_connection()
        if conn is None:
            return error_response('数据库连接失败')
            
        with conn.cursor() as cursor:
            sql = """
                SELECT 
                    service_date,
                    time_slot as service_time,
                    total_capacity,
                    booked_count,
                    CASE 
                        WHEN booked_count >= total_capacity THEN 'full'
                        ELSE 'available'
                    END as status
                FROM time_slots 
                WHERE service_date = %s 
                ORDER BY time_slot
            """
            cursor.execute(sql, (date,))
            slots = cursor.fetchall()
        return success_response(slots)
    except Exception as e:
        return error_response(f'获取时间槽失败: {str(e)}')
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

# 获取或创建用户（基于手机号）
def get_or_create_user(phone):
    """根据手机号获取或创建用户"""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return None
            
        with conn.cursor() as cursor:
            # 检查用户是否存在
            check_sql = "SELECT id FROM users WHERE phone = %s"
            cursor.execute(check_sql, (phone,))
            user = cursor.fetchone()
            
            if user:
                return user['id']
            else:
                # 创建新用户
                insert_sql = """
                    INSERT INTO users (phone, created_at) 
                    VALUES (%s, NOW())
                """
                cursor.execute(insert_sql, (phone,))
                conn.commit()
                return cursor.lastrowid
                
    except Exception as e:
        print(f"用户处理失败: {str(e)}")
        return None
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

# 创建预约
@app.route('/api/reservations', methods=['POST'])
def create_reservation():
    conn = None
    try:
        data = request.json
        
        # 参数验证
        required_fields = ['service_type', 'service_date', 'service_time', 
                          'name', 'phone']
        
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return error_response(f'缺少必要参数: {", ".join(missing_fields)}', status_code=400)
        
        # 验证手机号格式
        phone = data.get('phone')
        if not phone or len(phone) != 11 or not phone.startswith('1'):
            return error_response('手机号码格式不正确', status_code=400)
        
        # 获取或创建用户
        user_id = get_or_create_user(phone)
        if not user_id:
            return error_response('用户处理失败')
        
        conn = get_db_connection()
        if conn is None:
            return error_response('数据库连接失败')
            
        with conn.cursor() as cursor:
            # 检查时间槽是否可用
            check_sql = """
                SELECT COUNT(*) as count
                FROM reservations
                WHERE service_date = %s AND service_time = %s
                AND status != 'cancelled'
            """
            cursor.execute(check_sql, (
                data['service_date'], 
                data['service_time']
            ))
            result = cursor.fetchone()
            
            if result and result['count'] >= 5:  # 假设每个时间槽最多5个预约
                return error_response('该时间段已被约满', status_code=400)
            
            # 创建预约
            insert_sql = """
                INSERT INTO reservations 
                (user_id, service_type, service_date, service_time, 
                 customer_name, customer_phone, notes, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """
            cursor.execute(insert_sql, (
                user_id,
                data['service_type'],
                data['service_date'],
                data['service_time'],
                data['name'],
                data['phone'],
                data.get('remark', ''),
                'pending'
            ))
            reservation_id = cursor.lastrowid
            conn.commit()
            
        return success_response(
            data={'reservation_id': reservation_id},
            message='预约创建成功'
        )
    except Exception as e:
        if conn:
            conn.rollback()
        return error_response(f'创建预约失败: {str(e)}')
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

# 获取用户预约列表
@app.route('/api/reservations', methods=['GET'])
def get_reservations():
    conn = None
    try:
        phone = request.args.get('phone')
        if not phone:
            return error_response('请提供手机号', status_code=400)
            
        conn = get_db_connection()
        if conn is None:
            return error_response('数据库连接失败')
            
        with conn.cursor() as cursor:
            # 获取用户ID
            user_sql = "SELECT id FROM users WHERE phone = %s"
            cursor.execute(user_sql, (phone,))
            user = cursor.fetchone()
            
            if not user:
                return success_response([])  # 用户不存在，返回空列表
            
            # 获取用户的预约
            sql = """
                SELECT 
                    r.*,
                    st.name as service_name
                FROM reservations r
                LEFT JOIN service_types st ON r.service_type = st.id
                WHERE r.user_id = %s
                ORDER BY r.service_date DESC, r.service_time DESC
            """
            cursor.execute(sql, (user['id'],))
            reservations = cursor.fetchall()
            
            # 格式化数据
            for res in reservations:
                res['date'] = res['service_date'].strftime('%Y-%m-%d')
                res['time'] = res['service_time']
                res['name'] = res['customer_name']
                
        return success_response(reservations)
    except Exception as e:
        return error_response(f'获取预约列表失败: {str(e)}')
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

# 取消预约
@app.route('/api/reservations/<int:reservation_id>/cancel', methods=['PUT'])
def cancel_reservation(reservation_id):
    conn = None
    try:
        phone = request.json.get('phone')
        if not phone:
            return error_response('请提供手机号', status_code=400)
            
        conn = get_db_connection()
        if conn is None:
            return error_response('数据库连接失败')
            
        with conn.cursor() as cursor:
            # 验证预约属于该用户
            check_sql = """
                SELECT r.*, u.phone 
                FROM reservations r
                JOIN users u ON r.user_id = u.id
                WHERE r.id = %s AND u.phone = %s
            """
            cursor.execute(check_sql, (reservation_id, phone))
            reservation = cursor.fetchone()
            
            if not reservation:
                return error_response('预约不存在或无权操作', status_code=404)
            
            # 更新状态为已取消
            update_sql = "UPDATE reservations SET status = 'cancelled' WHERE id = %s"
            cursor.execute(update_sql, (reservation_id,))
            conn.commit()
            
        return success_response(message='预约已取消')
    except Exception as e:
        if conn:
            conn.rollback()
        return error_response(f'取消预约失败: {str(e)}')
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
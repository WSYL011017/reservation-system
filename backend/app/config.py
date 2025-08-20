'''
配置文件，包含应用的配置信息。
'''
import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

class Config:
    """基础配置类"""
    # 从环境变量获取密钥，如未设置则使用默认值（仅用于开发环境）
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # 设为True可查看SQL执行语句，方便调试
    # 主库（写）配置
    MASTER_SQLALCHEMY_DATABASE_URI = os.getenv('MASTER_DATABASE_URL')
    # 从库（读）配置（拆分为列表）
    SLAVE_SQLALCHEMY_DATABASE_URIS = os.getenv('SLAVE_DATABASE_URLS', '').split(',')
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_recycle': 300,
        'pool_pre_ping': True,
    }

    # 邮件配置
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    # 使用PyMySQL连接MySQL数据库
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 
                                        'mysql+pymysql://root:Suyala1017..@39.103.56.52/reservation_system')



class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL',
                                        'mysql+pymysql://root:Suyala1017..@39.103.56.52/reservation_system')
    # 测试时禁用CSRF保护
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    # 生产环境必须从环境变量获取数据库连接信息
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'mysql://root:Suyala1017..@39.103.56.52/reservation_system')
    # 生产环境中确保设置了SECRET_KEY
    SECRET_KEY = os.getenv('SECRET_KEY')

    if not SECRET_KEY:
        raise ValueError('No secret key set for production environment')

# 配置字典，用于根据环境选择配置
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


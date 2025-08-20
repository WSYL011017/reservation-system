'''
扩展初始化
'''
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
api = Api()
bcrypt = Bcrypt()
login_manager = LoginManager()
csrf = CSRFProtect()

# 配置登录管理器
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录以访问此页面'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """用户加载函数,用于Flask-Login"""
    from app.models.users import User
    return User.query.get(int(user_id))

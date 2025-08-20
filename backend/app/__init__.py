'''
应用工厂函数
'''
import os
from flask import Flask
from .extensions import db, migrate, cors
from .config import config

def create_app(config_name=None):
    if config_name is None:
        # 从环境变量获取配置名称，默认使用开发环境
        config_name = os.getenv('FLASK_CONFIG', 'default')
    
    # 创建Flask应用
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    register_extensions(app)
    
    # 注册蓝图
    register_blueprints(app)
    
    # 注册错误处理
    register_error_handlers(app)
    
    # 应用启动时的操作
    with app.app_context():
        # 确保数据库表存在
        db.create_all()
        
        # 可以在这里添加初始化数据
        
    return app

def register_extensions(app):
    """注册扩展"""
    # 初始化数据库
    db.init_app(app)
    # 初始化迁移工具
    migrate.init_app(app, db)
    # 初始化CORS，允许所有域访问API蓝图
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

def register_blueprints(app):
    """注册蓝图"""
    # 导入蓝图
    from .main.routes import bp as main_blueprint
    from .auth.routes import bp as auth_blueprint
    from .api.routes import bp as api_blueprint

    
    # 注册蓝图
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(api_blueprint, url_prefix='/api')

def register_error_handlers(app):
    """注册错误处理函数"""
    @app.errorhandler(404)
    def handle_404(error):
        return {"error": "Not found"}, 404
    
    @app.errorhandler(500)
    def handle_500(error):
        return {"error": "Internal server error"}, 500

from datetime import datetime
from flask_login import UserMixin
from app.extensions import db, bcrypt

class User(UserMixin,db.Model):
    """用户表模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(100), unique=True, nullable=False)
    nickname = db.Column(db.String(100))
    avatar_url = db.Column(db.String(500))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系：一个用户可以有多个预约
    reservations = db.relationship('Reservation', backref='user', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<User {self.username}>'
    def set_password(self, password):
        """设置密码哈希"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """验证密码"""
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        """转换为字典,用于API响应"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }
    def create_user(self, openid, nickname, avatar_url):
        self.openid = openid
        self.nickname = nickname
        self.avatar_url = avatar_url
        db.session.add(self)
        db.session.commit()
        return self


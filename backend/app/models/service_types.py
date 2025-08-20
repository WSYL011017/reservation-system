from datetime import datetime
from sqlalchemy.dialects.mysql import ENUM
from app.extensions import db


class ServiceType(db.Model):
    """服务类型表模型"""
    __tablename__ = 'service_types'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration_minutes = db.Column(db.Integer, default=60)
    price = db.Column(db.Numeric(10, 2))
    status = db.Column(ENUM('active', 'inactive'), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ServiceType {self.name}>'
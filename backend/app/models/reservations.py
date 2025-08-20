from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.mysql import ENUM


class Reservation(db.Model):
    """预约表模型"""
    __tablename__ = 'reservations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    service_date = db.Column(db.Date, nullable=False)
    service_time = db.Column(db.String(20), nullable=False)
    customer_name = db.Column(db.String(50), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    status = db.Column(ENUM('pending', 'confirmed', 'completed', 'cancelled'), default='pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Reservation {self.id} - {self.service_type}>'








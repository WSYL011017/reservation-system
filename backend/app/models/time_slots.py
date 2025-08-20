from datetime import datetime
from sqlalchemy.dialects.mysql import ENUM
from app.extensions import db

class TimeSlot(db.Model):
    """时间槽表模型"""
    __tablename__ = 'time_slots'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(20), nullable=False)
    total_capacity = db.Column(db.Integer, default=10)
    booked_count = db.Column(db.Integer, default=0)
    status = db.Column(ENUM('available', 'full', 'closed'), default='available')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 唯一约束：日期和时间段组合唯一
    __table_args__ = (
        db.UniqueConstraint('service_date', 'time_slot', name='unique_date_slot'),
    )
    
    def __repr__(self):
        return f'<TimeSlot {self.service_date} {self.time_slot}>'
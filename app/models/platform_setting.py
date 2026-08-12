from ..extensions import db
from datetime import datetime

class PlatformSetting(db.Model):
    __tablename__ = 'platform_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='general')
    description = db.Column(db.String(500))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PlatformSetting {self.key}>'
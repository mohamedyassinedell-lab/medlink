from ..extensions import db
from datetime import datetime
import re

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    first_name_ar = db.Column(db.String(50))
    last_name_ar = db.Column(db.String(50))
    slug = db.Column(db.String(200), unique=True, nullable=False)
    
    # Professional info
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.id'), nullable=False)
    sub_specialty = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    bio = db.Column(db.Text)
    bio_ar = db.Column(db.Text)
    
    # Location
    wilaya_id = db.Column(db.Integer, db.ForeignKey('wilayas.id'), nullable=False)
    commune_id = db.Column(db.Integer, db.ForeignKey('communes.id'), nullable=False)
    address = db.Column(db.String(500))
    address_ar = db.Column(db.String(500))
    
    # Contact
    phone = db.Column(db.String(20), nullable=False)
    phone_secondary = db.Column(db.String(20))
    email = db.Column(db.String(120))
    
    # Clinic
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=False)
    
    # Media
    profile_image = db.Column(db.String(200))
    
    # Status
    accepts_new_patients = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    services = db.relationship('DoctorService', backref='doctor', lazy='dynamic', cascade='all, delete-orphan')
    working_hours = db.relationship('WorkingHour', backref='doctor', lazy='dynamic', cascade='all, delete-orphan')
    holidays = db.relationship('Holiday', backref='doctor', lazy='dynamic', cascade='all, delete-orphan')
    reports = db.relationship('Report', backref='doctor', lazy='dynamic')
    
    def __repr__(self):
        return f'<Doctor {self.first_name} {self.last_name}>'
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name_ar(self):
        if self.first_name_ar and self.last_name_ar:
            return f"{self.first_name_ar} {self.last_name_ar}"
        return self.full_name
    
    @property
    def status(self):
        """Calculate current status based on working hours and holidays"""
        from datetime import datetime, time
        import pytz
        from ..services.status_service import StatusService
        return StatusService.get_status(self)
    
    def generate_slug(self):
        """Generate SEO-friendly slug from name"""
        name = f"{self.first_name} {self.last_name}".lower()
        # Remove Arabic characters for slug
        name = re.sub(r'[^\w\s-]', '', name)
        name = re.sub(r'[-\s]+', '-', name)
        return name.strip('-')
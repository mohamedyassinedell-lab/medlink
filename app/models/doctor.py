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
    
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.id'), nullable=False)
    sub_specialty = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    bio = db.Column(db.Text)
    bio_ar = db.Column(db.Text)
    
    wilaya_id = db.Column(db.Integer, db.ForeignKey('wilayas.id'), nullable=False)
    commune_id = db.Column(db.Integer, db.ForeignKey('communes.id'), nullable=False)
    address = db.Column(db.String(500))
    address_ar = db.Column(db.String(500))
    
    phone = db.Column(db.String(20), nullable=False)
    phone_secondary = db.Column(db.String(20))
    email = db.Column(db.String(120))
    
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=False)
    profile_image = db.Column(db.String(200))
    
    accepts_new_patients = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ===== العلاقات مع Cascade Delete =====
    services = db.relationship('DoctorService', backref='doctor', lazy='dynamic', cascade='all, delete-orphan')
    working_hours = db.relationship('WorkingHour', backref='doctor', lazy='dynamic', cascade='all, delete-orphan')
    holidays = db.relationship('Holiday', backref='doctor', lazy='dynamic', cascade='all, delete-orphan')
    reports = db.relationship('Report', backref='doctor', lazy='dynamic', cascade='all, delete-orphan')
    
    # العلاقات المرجعية
    specialty_ref = db.relationship('Specialty', foreign_keys=[specialty_id])
    wilaya_ref = db.relationship('Wilaya', foreign_keys=[wilaya_id])
    commune_ref = db.relationship('Commune', foreign_keys=[commune_id])
    clinic_ref = db.relationship('Clinic', foreign_keys=[clinic_id])
    
    # ... (بقية الكود كما هو)
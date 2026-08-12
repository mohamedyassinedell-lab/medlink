from ..extensions import db
from datetime import datetime

class Wilaya(db.Model):
    __tablename__ = 'wilayas'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    name_ar = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(5), unique=True, nullable=False)
    
    # Relationships
    communes = db.relationship('Commune', backref='wilaya', lazy='dynamic', cascade='all, delete-orphan')
    doctors = db.relationship('Doctor', backref='wilaya_ref', lazy='dynamic', foreign_keys='Doctor.wilaya_id')
    clinics = db.relationship('Clinic', backref='wilaya_ref', lazy='dynamic', foreign_keys='Clinic.wilaya_id')
    
    def __repr__(self):
        return f'<Wilaya {self.name_ar}>'

class Commune(db.Model):
    __tablename__ = 'communes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    name_ar = db.Column(db.String(50), nullable=False)
    wilaya_id = db.Column(db.Integer, db.ForeignKey('wilayas.id'), nullable=False)
    code = db.Column(db.String(10))
    
    # Relationships
    doctors = db.relationship('Doctor', backref='commune_ref', lazy='dynamic', foreign_keys='Doctor.commune_id')
    clinics = db.relationship('Clinic', backref='commune_ref', lazy='dynamic', foreign_keys='Clinic.commune_id')
    
    def __repr__(self):
        return f'<Commune {self.name_ar}>'
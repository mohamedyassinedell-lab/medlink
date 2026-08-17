from ..extensions import db
from datetime import datetime


class Clinic(db.Model):
    __tablename__ = 'clinics'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    name_ar = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    address_ar = db.Column(db.String(500))

    wilaya_id = db.Column(db.Integer, db.ForeignKey('wilayas.id'), nullable=False)
    commune_id = db.Column(db.Integer, db.ForeignKey('communes.id'), nullable=True)

    phone = db.Column(db.String(20), nullable=True)  # اختياري
    phone_secondary = db.Column(db.String(20))
    email = db.Column(db.String(120))
    description = db.Column(db.Text)
    description_ar = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    google_maps_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    doctors = db.relationship('Doctor', back_populates='clinic_ref', lazy='dynamic')
    wilaya_ref = db.relationship('Wilaya', foreign_keys=[wilaya_id], back_populates='clinics')
    commune_ref = db.relationship('Commune', foreign_keys=[commune_id], back_populates='clinics')

    def __repr__(self):
        return f'<Clinic {self.name_ar}>'
from ..extensions import db
from datetime import datetime
import re
from sqlalchemy.orm import validates


class Doctor(db.Model):
    __tablename__ = 'doctors'
    __table_args__ = {'extend_existing': True}

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    first_name_ar = db.Column(
        db.String(50)
    )

    last_name_ar = db.Column(
        db.String(50)
    )

    slug = db.Column(
        db.String(200),
        unique=True,
        nullable=False
    )

    # ============================================================
    # Professional info
    # ============================================================

    specialty_id = db.Column(
        db.Integer,
        db.ForeignKey('specialties.id'),
        nullable=False
    )

    sub_specialty = db.Column(
        db.String(100)
    )

    experience_years = db.Column(
        db.Integer
    )

    bio = db.Column(
        db.Text
    )

    bio_ar = db.Column(
        db.Text
    )

    # ============================================================
    # Location
    # ============================================================

    wilaya_id = db.Column(
        db.Integer,
        db.ForeignKey('wilayas.id'),
        nullable=False
    )

    commune_id = db.Column(
        db.Integer,
        db.ForeignKey('communes.id'),
        nullable=False
    )

    address = db.Column(
        db.String(500)
    )

    address_ar = db.Column(
        db.String(500)
    )

    # ============================================================
    # Contact
    # ============================================================

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    phone_secondary = db.Column(
        db.String(20)
    )

    email = db.Column(
        db.String(120)
    )

    # ============================================================
    # Clinic
    # ============================================================

    clinic_id = db.Column(
        db.Integer,
        db.ForeignKey('clinics.id'),
        nullable=False
    )

    # ============================================================
    # Media
    # ============================================================

    profile_image = db.Column(
        db.String(200)
    )

    # ============================================================
    # Status
    # ============================================================

    accepts_new_patients = db.Column(
        db.Boolean,
        default=True
    )

    is_verified = db.Column(
        db.Boolean,
        default=False
    )

    is_featured = db.Column(
        db.Boolean,
        default=False
    )

    is_published = db.Column(
        db.Boolean,
        default=True
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    # ============================================================
    # Timestamps
    # ============================================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # ============================================================
    # العلاقات
    # ============================================================

    services = db.relationship(
        'DoctorService',
        backref='doctor',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    working_hours = db.relationship(
        'WorkingHour',
        backref='doctor',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    holidays = db.relationship(
        'Holiday',
        backref='doctor',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    reports = db.relationship(
        'Report',
        backref='doctor',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    # ============================================================
    # العلاقات المرجعية
    # ============================================================

    specialty_ref = db.relationship(
        'Specialty',
        foreign_keys=[specialty_id],
        back_populates='doctors'
    )

    clinic_ref = db.relationship(
        'Clinic',
        foreign_keys=[clinic_id],
        back_populates='doctors'
    )

    # ============================================================
    # الخصائص المحسوبة
    # ============================================================

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def full_name_ar(self):
        if self.first_name_ar and self.last_name_ar:
            return f"{self.first_name_ar} {self.last_name_ar}".strip()

        return self.full_name

    @property
    def status(self):
        from ..services.status_service import StatusService
        return StatusService.get_status(self)

    # ============================================================
    # دوال مساعدة
    # ============================================================

    def generate_slug(self):
        if self.first_name and self.last_name:
            base = f"{self.first_name} {self.last_name}".lower()
        else:
            base = f"doctor-{self.id or 'new'}"

        slug = re.sub(
            r'[^\w\s-]',
            '',
            base
        )

        slug = re.sub(
            r'[-\s]+',
            '-',
            slug
        ).strip('-')

        existing = Doctor.query.filter(
            Doctor.slug == slug,
            Doctor.id != self.id
        ).first()

        if existing:
            import random
            slug = f"{slug}-{random.randint(100, 999)}"

        return slug

    @validates('slug')
    def validate_slug(self, key, slug):
        if not slug:
            return self.generate_slug()

        return slug

    def __repr__(self):
        return f'<Doctor {self.full_name}>'

    def get_working_hours_by_day(self):
        hours = {}

        for wh in self.working_hours.all():
            hours[wh.day_of_week] = wh

        return hours

    def get_current_holiday(self):
        from datetime import date

        today = date.today()

        for holiday in self.holidays.all():
            if holiday.start_date <= today <= holiday.end_date:
                return holiday

        return None

    def is_available_now(self):
        status = self.status

        return status.get('status') == 'AVAILABLE'
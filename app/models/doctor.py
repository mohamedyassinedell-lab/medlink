from ..extensions import db
from datetime import datetime
import re
from sqlalchemy.orm import validates


class Doctor(db.Model):
    __tablename__ = 'doctors'
    __table_args__ = {'extend_existing': True}

    # =========================
    # Basic information (OPTIONAL now)
    # =========================

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=True)   # اختياري
    last_name = db.Column(db.String(50), nullable=True)    # اختياري
    first_name_ar = db.Column(db.String(50))
    last_name_ar = db.Column(db.String(50))
    slug = db.Column(db.String(200), unique=True, nullable=False)

    # =========================
    # Professional information (OPTIONAL now)
    # =========================

    specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.id'), nullable=True)  # اختياري
    sub_specialty = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    bio = db.Column(db.Text)
    bio_ar = db.Column(db.Text)

    # =========================
    # Location (wilaya is REQUIRED)
    # =========================

    wilaya_id = db.Column(db.Integer, db.ForeignKey('wilayas.id'), nullable=False)  # إجباري
    commune_id = db.Column(db.Integer, db.ForeignKey('communes.id'), nullable=True)  # اختياري
    address = db.Column(db.String(500))
    address_ar = db.Column(db.String(500))

    # =========================
    # Contact (OPTIONAL)
    # =========================

    phone = db.Column(db.String(20), nullable=True)        # اختياري
    phone_secondary = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)

    # =========================
    # Clinic (OPTIONAL)
    # =========================

    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=True)   # اختياري

    # =========================
    # Media
    # =========================

    profile_image = db.Column(db.String(200))

    # =========================
    # Status
    # =========================

    accepts_new_patients = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)

    # =========================
    # Timestamps
    # =========================

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # =========================
    # Relationships
    # =========================

    services = db.relationship('DoctorService', backref='doctor', lazy='dynamic', cascade='all, delete-orphan')
    working_hours = db.relationship('WorkingHour', backref='doctor', lazy='dynamic', cascade='all, delete-orphan')
    holidays = db.relationship('Holiday', backref='doctor', lazy='dynamic', cascade='all, delete-orphan')
    reports = db.relationship('Report', backref='doctor', lazy='dynamic', cascade='all, delete-orphan')

    specialty_ref = db.relationship('Specialty', foreign_keys=[specialty_id], back_populates='doctors')
    clinic_ref = db.relationship('Clinic', foreign_keys=[clinic_id], back_populates='doctors')

    # =========================
    # Properties
    # =========================

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return "طبيب"

    @property
    def full_name_ar(self):
        if self.first_name_ar and self.last_name_ar:
            return f"{self.first_name_ar} {self.last_name_ar}".strip()
        elif self.first_name_ar:
            return self.first_name_ar
        elif self.last_name_ar:
            return self.last_name_ar
        return self.full_name

    @property
    def status(self):
        from ..services.status_service import StatusService
        return StatusService.get_status(self)

    # =========================
    # Slug - FIXED
    # =========================

    def generate_slug(self):
        """إنشاء slug فريد بناءً على الاسم أو معرف مؤقت"""
        # 1. محاولة بناء slug من الأسماء
        if self.first_name and self.last_name:
            base = f"{self.first_name} {self.last_name}".lower()
        elif self.first_name:
            base = self.first_name.lower()
        elif self.last_name:
            base = self.last_name.lower()
        else:
            # 2. إذا لم يكن هناك اسم، استخدم معرفًا مؤقتًا
            base = f"doctor-{self.id or 'new'}"

        # 3. تنظيف النص (إزالة الأحرف غير المسموحة)
        import re
        slug = re.sub(r'[^\w\s-]', '', base)
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')

        # 4. إذا أصبح slug فارغًا، استخدم قيمة افتراضية
        if not slug:
            slug = f"doctor-{self.id or 'new'}"

        # 5. التأكد من أن slug فريد (إضافة رقم عشوائي إذا كان موجودًا)
        existing = Doctor.query.filter(Doctor.slug == slug, Doctor.id != self.id).first()
        if existing:
            import random
            slug = f"{slug}-{random.randint(100, 999)}"

        return slug

    @validates('slug')
    def validate_slug(self, key, slug):
        if not slug:
            return self.generate_slug()
        return slug

    # =========================
    # Representation
    # =========================

    def __repr__(self):
        return f'<Doctor {self.full_name}>'

    # =========================
    # Working hours
    # =========================

    def get_working_hours_by_day(self):
        hours = {}
        for wh in self.working_hours.all():
            hours[wh.day_of_week] = wh
        return hours

    # =========================
    # Holidays
    # =========================

    def get_current_holiday(self):
        from datetime import date
        today = date.today()
        for holiday in self.holidays.all():
            if holiday.start_date <= today <= holiday.end_date:
                return holiday
        return None

    # =========================
    # Availability
    # =========================

    def is_available_now(self):
        status = self.status
        return status.get('status') == 'AVAILABLE'
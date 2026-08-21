from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Email, Optional, Length, NumberRange

class DoctorForm(FlaskForm):
    # ===== الأساسيات =====
    first_name = StringField('الاسم', validators=[Optional(), Length(max=50)])
    last_name = StringField('اللقب', validators=[Optional(), Length(max=50)])
    first_name_ar = StringField('الاسم (عربي)', validators=[Optional(), Length(max=50)])
    last_name_ar = StringField('اللقب (عربي)', validators=[Optional(), Length(max=50)])

    # ===== التخصص (اختياري) =====
    specialty_id = SelectField('التخصص', validators=[Optional()], coerce=int, choices=[])

    # ===== الولاية (إجباري) =====
    wilaya_id = SelectField('الولاية', validators=[DataRequired()], coerce=int, choices=[])

    # ===== البلدية (نصية اختيارية) =====
    commune_name = StringField('البلدية', validators=[Optional(), Length(max=100)])

    # ===== العيادة (نصية اختيارية) =====
    clinic_name = StringField('العيادة', validators=[Optional(), Length(max=200)])

    # ===== العنوان =====
    address = StringField('العنوان', validators=[Optional(), Length(max=500)])
    address_ar = StringField('العنوان (عربي)', validators=[Optional(), Length(max=500)])

    # ===== الهاتف =====
    phone = StringField('الهاتف', validators=[Optional(), Length(max=20)])
    phone_secondary = StringField('هاتف إضافي', validators=[Optional(), Length(max=20)])
    email = StringField('البريد الإلكتروني', validators=[Optional(), Email(), Length(max=120)])

    # ===== السيرة الذاتية =====
    bio = TextAreaField('نبذة', validators=[Optional()])
    bio_ar = TextAreaField('نبذة (عربي)', validators=[Optional()])

    # ===== الصورة =====
    profile_image = FileField('صورة الطبيب', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'الصور فقط')])

    # ===== الخيارات =====
    accepts_new_patients = BooleanField('يستقبل مرضى جدد')
    is_verified = BooleanField('موثق')
    is_featured = BooleanField('مميز')
    is_published = BooleanField('منشور')

    # ===== معلومات إضافية =====
    sub_specialty = StringField('التخصص الفرعي', validators=[Optional(), Length(max=100)])
    experience_years = IntegerField('سنوات الخبرة', validators=[Optional(), NumberRange(min=0, max=100)])


class HolidayForm(FlaskForm):
    start_date = DateTimeField('تاريخ البدء', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateTimeField('تاريخ النهاية', validators=[DataRequired()], format='%Y-%m-%d')
    note = StringField('ملاحظة')
    note_ar = StringField('ملاحظة (عربي)')
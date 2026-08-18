from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Email, Optional, Length, NumberRange

class DoctorForm(FlaskForm):
    # ===== الأساسيات =====
    first_name = StringField('الاسم', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('اللقب', validators=[DataRequired(), Length(max=50)])
    first_name_ar = StringField('الاسم (عربي)', validators=[Length(max=50)])
    last_name_ar = StringField('اللقب (عربي)', validators=[Length(max=50)])

    # ===== التخصص =====
    specialty_id = SelectField('التخصص', validators=[DataRequired()], coerce=int, choices=[])

    # ===== الولاية =====
    wilaya_id = SelectField('الولاية', validators=[DataRequired()], coerce=int, choices=[])

    # ===== البلدية (نصية) =====
    commune_name = StringField(
        'البلدية',
        validators=[Optional(), Length(max=100)]
    )

    # ===== العيادة (نصية) =====
    clinic_name = StringField(
        'العيادة',
        validators=[Optional(), Length(max=200)]
    )

    # ===== العنوان =====
    address = StringField('العنوان', validators=[Length(max=500)])
    address_ar = StringField('العنوان (عربي)', validators=[Length(max=500)])

    # ===== الهاتف =====
    phone = StringField('الهاتف', validators=[Optional(), Length(max=20)])
    phone_secondary = StringField('هاتف إضافي', validators=[Length(max=20)])
    email = StringField('البريد الإلكتروني', validators=[Optional(), Email(), Length(max=120)])

    # ===== السيرة الذاتية =====
    bio = TextAreaField('نبذة')
    bio_ar = TextAreaField('نبذة (عربي)')

    # ===== الصورة =====
    profile_image = FileField('صورة الطبيب', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'الصور فقط')])

    # ===== الخيارات =====
    accepts_new_patients = BooleanField('يستقبل مرضى جدد')
    is_verified = BooleanField('موثق')
    is_featured = BooleanField('مميز')
    is_published = BooleanField('منشور')

    # ===== معلومات إضافية =====
    sub_specialty = StringField('التخصص الفرعي', validators=[Length(max=100)])
    experience_years = IntegerField('سنوات الخبرة', validators=[Optional(), NumberRange(min=0, max=100)])


class HolidayForm(FlaskForm):
    start_date = DateTimeField('تاريخ البدء', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateTimeField('تاريخ النهاية', validators=[DataRequired()], format='%Y-%m-%d')
    note = StringField('ملاحظة')
    note_ar = StringField('ملاحظة (عربي)')
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Optional, Length

class ReportForm(FlaskForm):
    issue_type = SelectField(
        'نوع المشكلة',
        choices=[
            ('wrong_phone', 'رقم الهاتف خاطئ'),
            ('wrong_address', 'العنوان خاطئ'),
            ('not_working', 'الطبيب لم يعد يعمل هنا'),
            ('wrong_info', 'معلومات الطبيب غير صحيحة'),
            ('clinic_closed', 'العيادة مغلقة'),
            ('other', 'أخرى')
        ],
        validators=[DataRequired()]
    )
    description = TextAreaField('الوصف', validators=[DataRequired(), Length(min=10, max=500)])
    reporter_name = StringField('اسمك (اختياري)', validators=[Optional(), Length(max=100)])
    reporter_email = StringField('بريدك الإلكتروني (اختياري)', validators=[Optional(), Email(), Length(max=120)])
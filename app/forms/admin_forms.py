from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

class SettingsForm(FlaskForm):
    platform_name = StringField('اسم المنصة', validators=[DataRequired(), Length(max=100)])
    platform_description = StringField('وصف المنصة', validators=[Length(max=500)])
    platform_email = StringField('البريد الإلكتروني', validators=[DataRequired(), Email()])
    platform_phone = StringField('الهاتف', validators=[DataRequired(), Length(max=20)])
    platform_address = StringField('العنوان', validators=[Length(max=500)])
    
    submit = SubmitField('حفظ الإعدادات')
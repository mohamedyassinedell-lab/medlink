from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, Optional, Length

class ClinicForm(FlaskForm):
    name = StringField('اسم العيادة', validators=[DataRequired(), Length(max=200)])
    name_ar = StringField('اسم العيادة (عربي)', validators=[DataRequired(), Length(max=200)])
    
    wilaya_id = SelectField('الولاية', validators=[DataRequired()], coerce=int)
    commune_id = SelectField('البلدية', validators=[DataRequired()], coerce=int)
    address = StringField('العنوان', validators=[DataRequired(), Length(max=500)])
    address_ar = StringField('العنوان (عربي)', validators=[Length(max=500)])
    
    phone = StringField('الهاتف', validators=[DataRequired(), Length(max=20)])
    phone_secondary = StringField('هاتف إضافي', validators=[Length(max=20)])
    email = StringField('البريد الإلكتروني', validators=[Optional(), Email(), Length(max=120)])
    
    description = TextAreaField('الوصف')
    description_ar = TextAreaField('الوصف (عربي)')
    
    latitude = FloatField('خط العرض', validators=[Optional()])
    longitude = FloatField('خط الطول', validators=[Optional()])
    google_maps_url = StringField('رابط Google Maps', validators=[Length(max=500)])
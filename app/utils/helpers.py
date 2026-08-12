from flask import current_app
from app.models import PlatformSetting
import datetime

def register_filters(app):
    """تسجيل جميع الفلاتر المخصصة في Jinja2"""
    
    @app.template_filter('format_date')
    def format_date(date, format='%d/%m/%Y'):
        if date:
            return date.strftime(format)
        return ''
    
    @app.template_filter('format_phone')
    def format_phone(phone):
        if not phone:
            return ''
        return phone
    
    @app.template_filter('truncate_text')
    def truncate_text(text, length=100, suffix='...'):
        if not text:
            return ''
        if len(text) <= length:
            return text
        return text[:length].rsplit(' ', 1)[0] + suffix
    
    @app.template_filter('get_platform_setting')
    def get_platform_setting(key):
        setting = PlatformSetting.query.filter_by(key=key).first()
        return setting.value if setting else None
    
    # إضافة سياق عام لجميع القوالب
    @app.context_processor
    def utility_processor():
        def get_setting(key):
            setting = PlatformSetting.query.filter_by(key=key).first()
            return setting.value if setting else None
        
        return dict(
            get_platform_setting=get_setting,
            now=datetime.datetime.now()
        )
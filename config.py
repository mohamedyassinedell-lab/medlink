import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///medical_platform.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Admin settings
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@tabibdz.com'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'Admin123!'
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    
    # Platform settings
    PLATFORM_NAME = os.environ.get('PLATFORM_NAME') or 'TabibDZ'
    PLATFORM_DESCRIPTION = os.environ.get('PLATFORM_DESCRIPTION') or 'دليل الأطباء والعيادات في الجزائر'
    PLATFORM_EMAIL = os.environ.get('PLATFORM_EMAIL') or 'contact@tabibdz.com'
    PLATFORM_PHONE = os.environ.get('PLATFORM_PHONE') or '0555-555555'
    PLATFORM_ADDRESS = os.environ.get('PLATFORM_ADDRESS') or 'الجزائر العاصمة، الجزائر'
    
    # File upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Timezone
    TIMEZONE = os.environ.get('TIMEZONE') or 'Africa/Algiers'
    
    # Pagination
    DOCTORS_PER_PAGE = 12
    
    # ⚠️ هذه الدالة مهمة جداً
    @staticmethod
    def init_app(app):
        """تطبيق إعدادات إضافية على التطبيق إذا لزم الأمر"""
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
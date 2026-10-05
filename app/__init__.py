from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from .extensions import db, migrate, login_manager
from config import config
from .utils.helpers import register_filters


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'يرجى تسجيل الدخول أولاً'
    login_manager.login_message_category = 'warning'

    # Register blueprints
    from .routes.public import public_bp
    from .routes.admin import admin_bp
    from .routes.auth import auth_bp
    from .routes.user import user_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp)

    # Register filters
    register_filters(app)

    # ============================================================
    # ✅ GLOBAL CONTEXT PROCESSOR
    # يجعل المتغيرات متاحة في جميع القوالب (public + admin + auth + user)
    # ============================================================
    @app.context_processor
    def inject_global_data():
        from .models import Specialty
        try:
            specialties = Specialty.query.filter_by(is_active=True).all()
        except Exception:
            specialties = []
        
        return {
            'specialties': specialties
        }

    # Ensure upload directory exists
    import os
    upload_dir = app.config.get('UPLOAD_FOLDER')
    if upload_dir and not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    return app


@login_manager.user_loader
def load_user(user_id):
    from .models.user import User
    return User.query.get(int(user_id))
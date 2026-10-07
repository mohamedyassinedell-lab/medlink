from datetime import timedelta
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from .extensions import db, migrate, login_manager, jwt, cors
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

    # === JWT Configuration ===
    app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    jwt.init_app(app)

    # === CORS Configuration (Flutter mobile) ===
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": "*"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    # Register blueprints
    from .routes.public import public_bp
    from .routes.admin import admin_bp
    from .routes.auth import auth_bp
    from .routes.user import user_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp)

    # === API blueprint for mobile ===
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Register filters
    register_filters(app)

    # Global context processor
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
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
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'يرجى تسجيل الدخول أولاً'
    login_manager.login_message_category = 'warning'
    
    from .routes.public import public_bp
    from .routes.admin import admin_bp
    from .routes.auth import auth_bp
    
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    register_filters(app)
    
    import os
    upload_dir = app.config.get('UPLOAD_FOLDER')
    if upload_dir and not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    with app.app_context():
        db.create_all()
    
    return app

@login_manager.user_loader
def load_user(user_id):
    from .models.user import User
    return User.query.get(int(user_id))
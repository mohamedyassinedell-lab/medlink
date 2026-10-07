from datetime import datetime
from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from app.extensions import db
from app.models import User
from app.api.blueprint import api_bp


@api_bp.route('/auth/register', methods=['POST'])
def api_register():
    data = request.get_json() or {}

    username = (data.get('username') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not username or not email or not password:
        return jsonify({'error': 'جميع الحقول مطلوبة'}), 400

    if len(password) < 6:
        return jsonify({'error': 'كلمة المرور قصيرة جداً (6 أحرف على الأقل)'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'البريد الإلكتروني مستخدم مسبقاً'}), 409

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'اسم المستخدم مستخدم مسبقاً'}), 409

    user = User(username=username, email=email, is_admin=False, is_active=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    access = create_access_token(identity=str(user.id))
    refresh = create_refresh_token(identity=str(user.id))

    return jsonify({
        'user': {'id': user.id, 'username': user.username, 'email': user.email},
        'access_token': access,
        'refresh_token': refresh,
    }), 201


@api_bp.route('/auth/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'بيانات الدخول غير صحيحة'}), 401

    if not user.is_active:
        return jsonify({'error': 'الحساب معطّل'}), 403

    if user.is_admin:
        return jsonify({'error': 'استخدم تطبيق الويب للإدارة'}), 403

    user.last_login = datetime.utcnow()
    db.session.commit()

    access = create_access_token(identity=str(user.id))
    refresh = create_refresh_token(identity=str(user.id))

    return jsonify({
        'user': {'id': user.id, 'username': user.username, 'email': user.email},
        'access_token': access,
        'refresh_token': refresh,
    })


@api_bp.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def api_refresh():
    user_id = get_jwt_identity()
    return jsonify({'access_token': create_access_token(identity=user_id)})


@api_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def api_me():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'المستخدم غير موجود'}), 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat() if user.created_at else None,
    })
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db
from ..models import User
from ..forms.auth_forms import LoginForm, RegistrationForm
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


# ============================================================
# 👤 دخول المستخدم العادي (User Login)
# ============================================================

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل دخول المستخدم العادي"""
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        next_page = request.args.get('next')
        return redirect(next_page or url_for('user.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data) and user.is_active:
            # منع Admin من الدخول من هنا
            if user.is_admin:
                flash('يرجى استخدام صفحة تسجيل دخول الإدارة', 'warning')
                return redirect(url_for('auth.admin_login'))
            
            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash('تم تسجيل الدخول بنجاح', 'success')
            return redirect(next_page or url_for('user.dashboard'))
        else:
            flash('البريد الإلكتروني أو كلمة المرور غير صحيحة', 'danger')
    
    return render_template('auth/login.html', form=form)


# ============================================================
# 📝 تسجيل مستخدم جديد (User Registration)
# ============================================================

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """صفحة إنشاء حساب جديد للمستخدمين"""
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        next_page = request.args.get('next')
        return redirect(next_page or url_for('user.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # التحقق من عدم وجود البريد
        if User.query.filter_by(email=form.email.data).first():
            flash('البريد الإلكتروني مستخدم مسبقاً', 'danger')
            return render_template('auth/register.html', form=form)
        
        # التحقق من عدم وجود اسم المستخدم
        if User.query.filter_by(username=form.username.data).first():
            flash('اسم المستخدم مستخدم مسبقاً', 'danger')
            return render_template('auth/register.html', form=form)
        
        # إنشاء المستخدم
        user = User(
            username=form.username.data,
            email=form.email.data,
            is_admin=False,
            is_active=True
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        # تسجيل الدخول تلقائياً
        login_user(user)
        flash('🎉 تم إنشاء حسابك بنجاح! مرحباً بك', 'success')
        
        next_page = request.args.get('next')
        return redirect(next_page or url_for('user.dashboard'))
    
    return render_template('auth/register.html', form=form)


# ============================================================
# 👑 دخول Admin (Admin Login)
# ============================================================

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """صفحة تسجيل دخول الإدارة فقط"""
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data) and user.is_active:
            # التأكد أنه Admin
            if not user.is_admin:
                flash('هذا الحساب ليس حساب إدارة', 'danger')
                return render_template('admin/login.html', form=form)
            
            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user, remember=form.remember_me.data)
            flash('تم تسجيل الدخول كمدير بنجاح', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('البريد الإلكتروني أو كلمة المرور غير صحيحة', 'danger')
    
    return render_template('admin/login.html', form=form)


# ============================================================
# 🚪 تسجيل الخروج
# ============================================================

@auth_bp.route('/logout')
@login_required
def logout():
    """تسجيل الخروج"""
    logout_user()
    flash('تم تسجيل الخروج بنجاح', 'info')
    return redirect(url_for('public.index'))
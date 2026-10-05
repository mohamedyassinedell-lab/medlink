from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db
from ..models import User
from ..forms.auth_forms import LoginForm, RegistrationForm
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل الدخول"""
    if current_user.is_authenticated:
        next_page = request.args.get('next')
        if current_user.is_admin:
            return redirect(next_page or url_for('admin.dashboard'))
        return redirect(next_page or url_for('user.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data) and user.is_active:
            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash('تم تسجيل الدخول بنجاح', 'success')
            
            if user.is_admin:
                return redirect(next_page or url_for('admin.dashboard'))
            return redirect(next_page or url_for('user.dashboard'))
        else:
            flash('البريد الإلكتروني أو كلمة المرور غير صحيحة', 'danger')
    
    return render_template('admin/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """صفحة إنشاء حساب جديد"""
    # إذا كان المستخدم مسجل دخول بالفعل
    if current_user.is_authenticated:
        next_page = request.args.get('next')
        if current_user.is_admin:
            return redirect(next_page or url_for('admin.dashboard'))
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
        
        # ✅ تسجيل الدخول تلقائياً بعد التسجيل
        login_user(user)
        
        flash('🎉 تم إنشاء حسابك بنجاح! مرحباً بك في TebGuide', 'success')
        
        # ✅ التوجيه إلى next إذا كان موجوداً
        next_page = request.args.get('next')
        return redirect(next_page or url_for('user.dashboard'))
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """تسجيل الخروج"""
    logout_user()
    flash('تم تسجيل الخروج بنجاح', 'info')
    return redirect(url_for('public.index'))
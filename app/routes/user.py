from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Doctor, Specialty, Wilaya, Clinic, Commune
from ..forms.doctor_forms import DoctorForm
import os
from werkzeug.utils import secure_filename
import re


user_bp = Blueprint('user', __name__, url_prefix='/my-account')


def get_or_create_commune(name, wilaya_id):
    if not name or not name.strip():
        return None
    name = name.strip()
    commune = Commune.query.filter(
        (Commune.name == name) | (Commune.name_ar == name),
        Commune.wilaya_id == wilaya_id
    ).first()
    if not commune:
        commune = Commune(name=name, name_ar=name, wilaya_id=wilaya_id)
        db.session.add(commune)
        db.session.flush()
    return commune


def get_or_create_clinic(name, wilaya_id, commune_id=None):
    if not name or not name.strip():
        return None
    name = name.strip()
    clinic = Clinic.query.filter(
        (Clinic.name == name) | (Clinic.name_ar == name)
    ).first()
    if not clinic:
        clinic = Clinic(
            name=name, name_ar=name,
            address='', address_ar='',
            wilaya_id=wilaya_id, commune_id=commune_id,
            phone='', is_active=True
        )
        db.session.add(clinic)
        db.session.flush()
    return clinic


@user_bp.before_request
@login_required
def require_user():
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))


@user_bp.route('/')
def dashboard():
    """لوحة تحكم المستخدم"""
    my_doctors = Doctor.query.filter_by(submitted_by=current_user.id).order_by(Doctor.created_at.desc()).all()
    
    stats = {
        'total': len(my_doctors),
        'approved': sum(1 for d in my_doctors if d.is_approved),
        'pending': sum(1 for d in my_doctors if not d.is_approved),
    }
    
    return render_template('user/dashboard.html', doctors=my_doctors, stats=stats)


@user_bp.route('/doctors/add', methods=['GET', 'POST'])
def add_doctor():
    """إضافة طبيب جديد (يحتاج موافقة Admin)"""
    form = DoctorForm()
    
    form.specialty_id.choices = [(s.id, s.name_ar) for s in Specialty.query.filter_by(is_active=True).all()]
    form.wilaya_id.choices = [(w.id, w.name_ar) for w in Wilaya.query.all()]
    
    if form.validate_on_submit():
        try:
            commune = get_or_create_commune(form.commune_name.data, form.wilaya_id.data)
            clinic = get_or_create_clinic(form.clinic_name.data, form.wilaya_id.data, commune.id if commune else None)
            
            doctor = Doctor(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                first_name_ar=form.first_name_ar.data,
                last_name_ar=form.last_name_ar.data,
                specialty_id=form.specialty_id.data,
                sub_specialty=form.sub_specialty.data,
                experience_years=form.experience_years.data,
                bio=form.bio.data,
                bio_ar=form.bio_ar.data,
                wilaya_id=form.wilaya_id.data,
                commune_id=commune.id if commune else None,
                address=form.address.data,
                address_ar=form.address_ar.data,
                phone=form.phone.data,
                phone_secondary=form.phone_secondary.data,
                email=form.email.data,
                clinic_id=clinic.id if clinic else None,
                accepts_new_patients=form.accepts_new_patients.data,
                is_verified=False,
                is_featured=False,
                is_published=False,
                is_approved=False,
                is_active=True,
                submitted_by=current_user.id
            )
            
            doctor.slug = doctor.generate_slug()
            
            if form.profile_image.data:
                file = form.profile_image.data
                filename = secure_filename(f"doctor_{current_user.id}_{file.filename}")
                upload_path = current_app.config.get('UPLOAD_FOLDER')
                if upload_path:
                    os.makedirs(upload_path, exist_ok=True)
                    file.save(os.path.join(upload_path, filename))
                    doctor.profile_image = f"/static/uploads/{filename}"
            
            db.session.add(doctor)
            db.session.commit()
            
            flash('تم إرسال معلومات الطبيب بنجاح! سيتم مراجعتها من قبل الإدارة.', 'success')
            return redirect(url_for('user.dashboard'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')
    
    return render_template('user/add_doctor.html', form=form, title='إضافة طبيب جديد')


@user_bp.route('/doctors/<int:id>/edit', methods=['GET', 'POST'])
def edit_doctor(id):
    """تعديل طبيب أضافه المستخدم"""
    doctor = Doctor.query.get_or_404(id)
    
    # التأكد أن المستخدم هو صاحب الطبيب
    if doctor.submitted_by != current_user.id:
        abort(403)
    
    form = DoctorForm(obj=doctor)
    form.specialty_id.choices = [(s.id, s.name_ar) for s in Specialty.query.filter_by(is_active=True).all()]
    form.wilaya_id.choices = [(w.id, w.name_ar) for w in Wilaya.query.all()]
    
    if request.method == 'GET':
        if doctor.commune_ref:
            form.commune_name.data = doctor.commune_ref.name_ar or doctor.commune_ref.name
        if doctor.clinic_ref:
            form.clinic_name.data = doctor.clinic_ref.name_ar or doctor.clinic_ref.name
    
    if form.validate_on_submit():
        try:
            commune = get_or_create_commune(form.commune_name.data, form.wilaya_id.data)
            clinic = get_or_create_clinic(form.clinic_name.data, form.wilaya_id.data, commune.id if commune else None)
            
            form.populate_obj(doctor)
            doctor.commune_id = commune.id if commune else None
            doctor.clinic_id = clinic.id if clinic else None
            doctor.slug = doctor.generate_slug()
            doctor.is_approved = False  # إعادة المراجعة بعد التعديل
            
            if form.profile_image.data:
                file = form.profile_image.data
                filename = secure_filename(f"doctor_{doctor.id}_{file.filename}")
                upload_path = current_app.config.get('UPLOAD_FOLDER')
                if upload_path:
                    os.makedirs(upload_path, exist_ok=True)
                    file.save(os.path.join(upload_path, filename))
                    doctor.profile_image = f"/static/uploads/{filename}"
            
            db.session.commit()
            flash('تم تحديث بيانات الطبيب. سيتم مراجعتها من جديد.', 'success')
            return redirect(url_for('user.dashboard'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')
    
    return render_template('user/add_doctor.html', form=form, doctor=doctor, title='تعديل طبيب')
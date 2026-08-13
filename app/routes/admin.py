from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Doctor, Clinic, Wilaya, Report, WorkingHour, Holiday

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# --- 1. إرسال المتغيرات العامة لجميع القوالب (تمنع خطأ pending_reports UndefinedError) ---
@admin_bp.context_processor
def inject_global_vars():
    try:
        pending_count = Report.query.filter_by(status='pending').count()
    except Exception:
        pending_count = 0
    return dict(pending_reports=pending_count)


# --- 2. الرئيسية (لوحة التحكم) ---
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    doctor_count = Doctor.query.count()
    published_count = Doctor.query.filter_by(is_published=True).count()
    verified_count = Doctor.query.filter_by(is_verified=True).count()
    clinic_count = Clinic.query.count()
    wilaya_count = Wilaya.query.count()
    recent_doctors = Doctor.query.order_by(Doctor.id.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                           doctor_count=doctor_count,
                           published_count=published_count,
                           verified_count=verified_count,
                           clinic_count=clinic_count,
                           wilaya_count=wilaya_count,
                           recent_doctors=recent_doctors)


# --- 3. إدارة الأطباء ---
@admin_bp.route('/doctors')
@login_required
def doctors():
    status = request.args.get('status', 'all')
    page = request.args.get('page', 1, type=int)
    
    query = Doctor.query
    if status == 'published':
        query = query.filter_by(is_published=True)
    elif status == 'unpublished':
        query = query.filter_by(is_published=False)
        
    pagination = query.order_by(Doctor.id.desc()).paginate(page=page, per_page=10, error_out=False)
    
    return render_template('admin/doctors.html', 
                           doctors=pagination.items, 
                           pagination=pagination)


@admin_bp.route('/doctors/delete/<int:id>', methods=['POST'])
@login_required
def delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    try:
        # حذف التبعيات يدوياً لضمان عدم حدوث خطأ Foreign Key Constraint
        WorkingHour.query.filter_by(doctor_id=doctor.id).delete()
        Holiday.query.filter_by(doctor_id=doctor.id).delete()
        Report.query.filter_by(doctor_id=doctor.id).delete()

        db.session.delete(doctor)
        db.session.commit()
        flash('تم حذف الطبيب وجميع بياناته المرتبطة بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء حذف الطبيب: {str(e)}', 'danger')

    return redirect(url_for('admin.doctors'))


@admin_bp.route('/doctors/toggle-publish/<int:id>', methods=['POST'])
@login_required
def toggle_publish(id):
    doctor = Doctor.query.get_or_404(id)
    doctor.is_published = not doctor.is_published
    db.session.commit()
    flash('تم تغيير حالة النشر بنجاح', 'success')
    return redirect(url_for('admin.doctors'))


# --- 4. إدارة العيادات (مصححة ومحمية بالكامل) ---
@admin_bp.route('/clinics')
@login_required
def clinics():
    try:
        clinics_list = Clinic.query.order_by(Clinic.id.desc()).all()
    except Exception:
        clinics_list = []
    return render_template('admin/clinics.html', clinics=clinics_list)


@admin_bp.route('/clinics/add', methods=['GET', 'POST'])
@login_required
def add_clinic():
    wilayas = Wilaya.query.order_by(Wilaya.code.asc()).all()
    
    if request.method == 'POST':
        name_ar = request.form.get('name_ar')
        name = request.form.get('name')
        wilaya_id = request.form.get('wilaya_id')
        phone = request.form.get('phone')
        address_ar = request.form.get('address_ar')

        if not name_ar or not wilaya_id:
            flash('يرجى ملء اسم العيادة واختيار الولاية!', 'warning')
            return render_template('admin/clinic_form.html', wilayas=wilayas, title='إضافة عيادة جديدة')

        try:
            new_clinic = Clinic(
                name_ar=name_ar,
                name=name,
                wilaya_id=int(wilaya_id),
                phone=phone,
                address_ar=address_ar
            )
            db.session.add(new_clinic)
            db.session.commit()
            flash('تمت إضافة العيادة بنجاح!', 'success')
            return redirect(url_for('admin.clinics'))
        except Exception as e:
            db.session.rollback()
            flash(f'تعذر حفظ العيادة: {str(e)}', 'danger')

    return render_template('admin/clinic_form.html', wilayas=wilayas, title='إضافة عيادة جديدة')


@admin_bp.route('/clinics/delete/<int:id>', methods=['POST'])
@login_required
def delete_clinic(id):
    clinic = Clinic.query.get_or_404(id)
    try:
        # فك ارتباط الأطباء بالعيادة قبل الحذف لتفادي الأخطاء
        Doctor.query.filter_by(clinic_id=clinic.id).update({Doctor.clinic_id: None})
        db.session.delete(clinic)
        db.session.commit()
        flash('تم حذف العيادة بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'تعذر حذف العيادة: {str(e)}', 'danger')

    return redirect(url_for('admin.clinics'))


# --- 5. إدارة الولايات ---
@admin_bp.route('/wilayas')
@login_required
def wilayas():
    wilaya_list = Wilaya.query.order_by(Wilaya.code.asc()).all()
    return render_template('admin/wilayas.html', wilayas=wilaya_list)


@admin_bp.route('/wilayas/add', methods=['POST'])
@login_required
def add_wilaya():
    code = request.form.get('code')
    name_ar = request.form.get('name_ar')
    name = request.form.get('name')

    if not code or not name_ar:
        flash('يرجى إدخال رمز الولاية والاسم بالعربية', 'warning')
        return redirect(url_for('admin.wilayas'))

    try:
        existing = Wilaya.query.filter_by(code=int(code)).first()
        if existing:
            flash('رمز هذه الولاية موجود مسبقاً!', 'danger')
        else:
            new_wilaya = Wilaya(code=int(code), name_ar=name_ar, name=name)
            db.session.add(new_wilaya)
            db.session.commit()
            flash('تمت إضافة الولاية بنجاح!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ عند إضافة الولاية: {str(e)}', 'danger')

    return redirect(url_for('admin.wilayas'))


@admin_bp.route('/wilayas/delete/<int:id>', methods=['POST'])
@login_required
def delete_wilaya(id):
    wilaya = Wilaya.query.get_or_404(id)
    try:
        # حماية: التأكد من عدم وجود أطباء أو عيادات مرتبطة بالولاية
        if Doctor.query.filter_by(wilaya_id=wilaya.id).first() or Clinic.query.filter_by(wilaya_id=wilaya.id).first():
            flash('لا يمكن حذف الولاية لأنها مرتبطة بأطباء أو عيادات مسجلة!', 'danger')
            return redirect(url_for('admin.wilayas'))

        db.session.delete(wilaya)
        db.session.commit()
        flash('تم حذف الولاية بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'تعذر حذف الولاية: {str(e)}', 'danger')

    return redirect(url_for('admin.wilayas'))


# --- 6. إدارة البلاغات ---
@admin_bp.route('/reports')
@login_required
def reports():
    reports_list = Report.query.order_by(Report.id.desc()).all()
    return render_template('admin/reports.html', reports=reports_list)


@admin_bp.route('/reports/update/<int:id>', methods=['POST'])
@login_required
def update_report(id):
    report = Report.query.get_or_404(id)
    report.status = request.form.get('status')
    report.admin_notes = request.form.get('admin_notes')
    db.session.commit()
    flash('تم تحديث حالة البلاغ بنجاح', 'success')
    return redirect(url_for('admin.reports'))
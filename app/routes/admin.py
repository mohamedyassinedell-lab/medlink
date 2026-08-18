from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user

from ..extensions import db

from ..models import (
    Doctor,
    Clinic,
    Specialty,
    Wilaya,
    Commune,
    Service,
    WorkingHour,
    Holiday,
    Report,
    PlatformSetting,
    DoctorService
)

from ..forms.doctor_forms import DoctorForm, HolidayForm
from ..forms.clinic_forms import ClinicForm
from ..forms.admin_forms import SettingsForm

from datetime import datetime
import os
import re

from werkzeug.utils import secure_filename


admin_bp = Blueprint('admin', __name__)


# ============================================================
# دوال مساعدة
# ============================================================

def get_or_create_commune(name, wilaya_id):
    if not name or not name.strip():
        return None
    name = name.strip()
    commune = Commune.query.filter(
        (Commune.name == name) | (Commune.name_ar == name),
        Commune.wilaya_id == wilaya_id
    ).first()
    if not commune:
        if re.search(r'[أ-ي]', name):
            commune = Commune(name=name, name_ar=name, wilaya_id=wilaya_id)
        else:
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
        if re.search(r'[أ-ي]', name):
            clinic = Clinic(
                name=name, name_ar=name,
                address='', address_ar='',
                wilaya_id=wilaya_id,
                commune_id=commune_id,
                phone='', is_active=True
            )
        else:
            clinic = Clinic(
                name=name, name_ar=name,
                address='', address_ar='',
                wilaya_id=wilaya_id,
                commune_id=commune_id,
                phone='', is_active=True
            )
        db.session.add(clinic)
        db.session.flush()
    return clinic


# ============================================================
# التحقق من المدير
# ============================================================

@admin_bp.before_request
@login_required
def require_admin():
    if not current_user.is_admin:
        abort(403)


# ============================================================
# لوحة التحكم
# ============================================================

@admin_bp.route('/')
def dashboard():
    doctor_count = Doctor.query.count()
    clinic_count = Clinic.query.count()
    specialty_count = Specialty.query.count()
    wilaya_count = Wilaya.query.count()
    published_count = Doctor.query.filter_by(is_published=True).count()
    featured_count = Doctor.query.filter_by(is_featured=True).count()
    verified_count = Doctor.query.filter_by(is_verified=True).count()
    recent_doctors = Doctor.query.order_by(Doctor.created_at.desc()).limit(5).all()
    pending_reports = Report.query.filter_by(status='pending').count()
    return render_template(
        'admin/dashboard.html',
        doctor_count=doctor_count,
        clinic_count=clinic_count,
        specialty_count=specialty_count,
        wilaya_count=wilaya_count,
        published_count=published_count,
        featured_count=featured_count,
        verified_count=verified_count,
        recent_doctors=recent_doctors,
        pending_reports=pending_reports
    )


# ============================================================
# تعبئة قاعدة البيانات
# ============================================================

@admin_bp.route('/force-seed')
def force_seed():
    from app.services.seed_service import seed_database
    seed_database()
    return "✅ Database seeded successfully!"


# ============================================================
# إدارة الأطباء
# ============================================================

@admin_bp.route('/doctors')
def doctors():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    query = Doctor.query
    status = request.args.get('status', '')
    if status == 'published':
        query = query.filter_by(is_published=True)
    elif status == 'unpublished':
        query = query.filter_by(is_published=False)
    pagination = query.order_by(Doctor.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('admin/doctors.html', doctors=pagination.items, pagination=pagination)


@admin_bp.route('/doctors/add', methods=['GET', 'POST'])
def add_doctor():
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
                is_verified=form.is_verified.data,
                is_featured=form.is_featured.data,
                is_published=form.is_published.data
            )
            doctor.slug = doctor.generate_slug()
            if form.profile_image.data:
                file = form.profile_image.data
                filename = secure_filename(f"doctor_{doctor.id}_{file.filename}")
                upload_path = current_app.config.get('UPLOAD_FOLDER')
                if upload_path:
                    os.makedirs(upload_path, exist_ok=True)
                    file.save(os.path.join(upload_path, filename))
                    doctor.profile_image = f"/static/uploads/{filename}"
            db.session.add(doctor)
            db.session.commit()
            flash('تم إضافة الطبيب بنجاح', 'success')
            return redirect(url_for('admin.doctors'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')
            print(f"ERROR: {e}")
    return render_template('admin/doctor_form.html', form=form, title='إضافة طبيب')


@admin_bp.route('/doctors/<int:id>/edit', methods=['GET', 'POST'])
def edit_doctor(id):
    doctor = Doctor.query.get_or_404(id)
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
            if form.profile_image.data:
                file = form.profile_image.data
                filename = secure_filename(f"doctor_{doctor.id}_{file.filename}")
                upload_path = current_app.config.get('UPLOAD_FOLDER')
                if upload_path:
                    os.makedirs(upload_path, exist_ok=True)
                    file.save(os.path.join(upload_path, filename))
                    doctor.profile_image = f"/static/uploads/{filename}"
            db.session.commit()
            flash('تم تحديث بيانات الطبيب بنجاح', 'success')
            return redirect(url_for('admin.doctors'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')
    return render_template('admin/doctor_form.html', form=form, doctor=doctor, title='تعديل طبيب')


@admin_bp.route('/doctors/<int:id>/delete', methods=['POST'])
def delete_doctor(id):
    try:
        doctor = Doctor.query.get_or_404(id)
        db.session.delete(doctor)
        db.session.commit()
        flash('تم حذف الطبيب بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('admin.doctors'))


@admin_bp.route('/doctors/<int:id>/toggle-publish', methods=['POST'])
def toggle_publish(id):
    try:
        doctor = Doctor.query.get_or_404(id)
        doctor.is_published = not doctor.is_published
        db.session.commit()
        status = 'نشر' if doctor.is_published else 'إلغاء النشر'
        flash(f'تم {status} الطبيب بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('admin.doctors'))


@admin_bp.route('/doctors/<int:id>/working-hours', methods=['GET', 'POST'])
def manage_working_hours(id):
    doctor = Doctor.query.get_or_404(id)
    if request.method == 'POST':
        try:
            WorkingHour.query.filter_by(doctor_id=doctor.id).delete()
            for day in range(7):
                start = request.form.get(f'start_{day}')
                end = request.form.get(f'end_{day}')
                is_closed = request.form.get(f'closed_{day}') == 'on'
                if not is_closed and start and end:
                    wh = WorkingHour(doctor_id=doctor.id, day_of_week=day, start_time=start, end_time=end, is_closed=False)
                    db.session.add(wh)
                elif is_closed:
                    wh = WorkingHour(doctor_id=doctor.id, day_of_week=day, start_time='00:00', end_time='00:00', is_closed=True)
                    db.session.add(wh)
            db.session.commit()
            flash('تم تحديث أوقات العمل بنجاح', 'success')
            return redirect(url_for('admin.doctors'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')
    hours_list = doctor.working_hours.all() if hasattr(doctor.working_hours, 'all') else doctor.working_hours
    working_hours = {wh.day_of_week: wh for wh in hours_list}
    return render_template('admin/working_hours.html', doctor=doctor, working_hours=working_hours)


@admin_bp.route('/doctors/<int:id>/holidays', methods=['GET', 'POST'])
def manage_holidays(id):
    doctor = Doctor.query.get_or_404(id)
    form = HolidayForm()
    if form.validate_on_submit():
        try:
            holiday = Holiday(
                doctor_id=doctor.id,
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                note=form.note.data,
                note_ar=form.note_ar.data
            )
            db.session.add(holiday)
            db.session.commit()
            flash('تم إضافة العطلة بنجاح', 'success')
            return redirect(url_for('admin.manage_holidays', id=doctor.id))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')
    holidays = doctor.holidays.order_by(Holiday.start_date.desc()).all()
    return render_template('admin/holidays.html', doctor=doctor, holidays=holidays, form=form)


@admin_bp.route('/holidays/<int:id>/delete', methods=['POST'])
def delete_holiday(id):
    try:
        holiday = Holiday.query.get_or_404(id)
        doctor_id = holiday.doctor_id
        db.session.delete(holiday)
        db.session.commit()
        flash('تم حذف العطلة بنجاح', 'success')
        return redirect(url_for('admin.manage_holidays', id=doctor_id))
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
        return redirect(url_for('admin.doctors'))


# ============================================================
# إدارة العيادات
# ============================================================

@admin_bp.route('/clinics')
def clinics():
    clinics = Clinic.query.order_by(Clinic.created_at.desc()).all()
    return render_template('admin/clinics.html', clinics=clinics)


@admin_bp.route('/clinics/add', methods=['GET', 'POST'])
def add_clinic():
    form = ClinicForm()
    form.wilaya_id.choices = [(w.id, w.name_ar) for w in Wilaya.query.all()]
    form.commune_id.choices = [(c.id, c.name_ar) for c in Commune.query.all()]
    if form.validate_on_submit():
        try:
            clinic = Clinic(
                name=form.name.data,
                name_ar=form.name_ar.data,
                address=form.address.data,
                address_ar=form.address_ar.data,
                wilaya_id=form.wilaya_id.data,
                commune_id=form.commune_id.data or None,
                phone=form.phone.data,
                phone_secondary=form.phone_secondary.data,
                email=form.email.data,
                description=form.description.data,
                description_ar=form.description_ar.data,
                latitude=form.latitude.data,
                longitude=form.longitude.data,
                google_maps_url=form.google_maps_url.data,
                is_active=True
            )
            db.session.add(clinic)
            db.session.commit()
            flash('تم إضافة العيادة بنجاح', 'success')
            return redirect(url_for('admin.clinics'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')
    return render_template('admin/clinic_form.html', form=form, wilayas=Wilaya.query.all(), title='إضافة عيادة')


@admin_bp.route('/clinics/<int:id>/delete', methods=['POST'])
def delete_clinic(id):
    try:
        clinic = Clinic.query.get_or_404(id)
        if clinic.doctors.count() > 0:
            flash('لا يمكن حذف العيادة لأنها مرتبطة بأطباء.', 'error')
            return redirect(url_for('admin.clinics'))
        db.session.delete(clinic)
        db.session.commit()
        flash('تم حذف العيادة بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('admin.clinics'))


# ============================================================
# إدارة التخصصات
# ============================================================

@admin_bp.route('/specialties')
def specialties():
    specialties = Specialty.query.order_by(Specialty.name_ar).all()
    return render_template('admin/specialties.html', specialties=specialties)


@admin_bp.route('/specialties/add', methods=['GET', 'POST'])
def add_specialty():
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            name_ar = request.form.get('name_ar', '').strip()
            icon = request.form.get('icon', '').strip()
            if not name or not name_ar:
                flash('يرجى ملء جميع المعلومات الأساسية.', 'error')
                return render_template('admin/specialty_form.html')
            if Specialty.query.filter_by(name=name).first():
                flash('التخصص موجود مسبقاً.', 'error')
                return render_template('admin/specialty_form.html')
            specialty = Specialty(name=name, name_ar=name_ar, icon=icon or 'stethoscope', is_active=True)
            db.session.add(specialty)
            db.session.commit()
            flash('تم إضافة التخصص بنجاح.', 'success')
            return redirect(url_for('admin.specialties'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')
    return render_template('admin/specialty_form.html')


@admin_bp.route('/specialties/<int:id>/edit', methods=['GET', 'POST'])
def edit_specialty(id):
    specialty = Specialty.query.get_or_404(id)
    if request.method == 'POST':
        try:
            specialty.name = request.form.get('name', '').strip()
            specialty.name_ar = request.form.get('name_ar', '').strip()
            specialty.icon = request.form.get('icon', '').strip() or 'stethoscope'
            db.session.commit()
            flash('تم تحديث التخصص بنجاح.', 'success')
            return redirect(url_for('admin.specialties'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')
    return render_template('admin/specialty_form.html', specialty=specialty)


@admin_bp.route('/specialties/<int:id>/delete', methods=['POST'])
def delete_specialty(id):
    try:
        specialty = Specialty.query.get_or_404(id)
        if specialty.doctors.filter_by(is_published=True).count() > 0:
            flash('لا يمكن حذف التخصص لأنه مرتبط بأطباء.', 'error')
            return redirect(url_for('admin.specialties'))
        db.session.delete(specialty)
        db.session.commit()
        flash('تم حذف التخصص بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('admin.specialties'))


# ============================================================
# إدارة الولايات
# ============================================================

@admin_bp.route('/wilayas')
def wilayas():
    wilayas = Wilaya.query.order_by(Wilaya.name_ar).all()
    return render_template('admin/wilayas.html', wilayas=wilayas)


@admin_bp.route('/wilayas/add', methods=['GET', 'POST'])
def add_wilaya():
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            name_ar = request.form.get('name_ar', '').strip()
            code = request.form.get('code', '').strip()
            if not name or not name_ar or not code:
                flash('يرجى ملء جميع المعلومات.', 'error')
                return render_template('admin/wilaya_form.html')
            if Wilaya.query.filter_by(code=code).first():
                flash('رمز الولاية موجود مسبقاً.', 'error')
                return render_template('admin/wilaya_form.html')
            wilaya = Wilaya(name=name, name_ar=name_ar, code=code)
            db.session.add(wilaya)
            db.session.commit()
            flash('تمت إضافة الولاية بنجاح.', 'success')
            return redirect(url_for('admin.wilayas'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')
    return render_template('admin/wilaya_form.html')


@admin_bp.route('/wilayas/<int:id>/delete', methods=['POST'])
def delete_wilaya(id):
    try:
        wilaya = Wilaya.query.get_or_404(id)
        if wilaya.doctors.count() > 0:
            flash('لا يمكن حذف الولاية لأنها مرتبطة بأطباء.', 'error')
            return redirect(url_for('admin.wilayas'))
        if wilaya.clinics.count() > 0:
            flash('لا يمكن حذف الولاية لأنها مرتبطة بعيادات.', 'error')
            return redirect(url_for('admin.wilayas'))
        if wilaya.communes.count() > 0:
            flash('لا يمكن حذف الولاية لأنها تحتوي على بلديات.', 'error')
            return redirect(url_for('admin.wilayas'))
        db.session.delete(wilaya)
        db.session.commit()
        flash('تم حذف الولاية بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('admin.wilayas'))


# ============================================================
# إدارة البلديات (كاملة)
# ============================================================

@admin_bp.route('/communes')
def communes():
    communes = Commune.query.join(Wilaya).order_by(Wilaya.name_ar, Commune.name_ar).all()
    return render_template('admin/communes.html', communes=communes)


@admin_bp.route('/communes/add', methods=['GET', 'POST'])
def add_commune():
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            name_ar = request.form.get('name_ar', '').strip()
            wilaya_id = request.form.get('wilaya_id', type=int)
            code = request.form.get('code', '').strip()
            if not name or not name_ar or not wilaya_id:
                flash('يرجى ملء جميع المعلومات الأساسية.', 'error')
                wilayas = Wilaya.query.all()
                return render_template('admin/commune_form.html', wilayas=wilayas)
            # التحقق من وجود الولاية
            wilaya = Wilaya.query.get(wilaya_id)
            if not wilaya:
                flash('الولاية غير موجودة.', 'error')
                wilayas = Wilaya.query.all()
                return render_template('admin/commune_form.html', wilayas=wilayas)
            # منع التكرار
            existing = Commune.query.filter_by(name=name, wilaya_id=wilaya_id).first()
            if existing:
                flash('البلدية موجودة مسبقاً في هذه الولاية.', 'error')
                wilayas = Wilaya.query.all()
                return render_template('admin/commune_form.html', wilayas=wilayas)
            commune = Commune(name=name, name_ar=name_ar, wilaya_id=wilaya_id, code=code)
            db.session.add(commune)
            db.session.commit()
            flash('تم إضافة البلدية بنجاح.', 'success')
            return redirect(url_for('admin.communes'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')
    wilayas = Wilaya.query.all()
    return render_template('admin/commune_form.html', wilayas=wilayas)


@admin_bp.route('/communes/<int:id>/edit', methods=['GET', 'POST'])
def edit_commune(id):
    commune = Commune.query.get_or_404(id)
    if request.method == 'POST':
        try:
            commune.name = request.form.get('name', '').strip()
            commune.name_ar = request.form.get('name_ar', '').strip()
            commune.code = request.form.get('code', '').strip()
            wilaya_id = request.form.get('wilaya_id', type=int)
            if wilaya_id:
                commune.wilaya_id = wilaya_id
            db.session.commit()
            flash('تم تحديث البلدية بنجاح.', 'success')
            return redirect(url_for('admin.communes'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')
    wilayas = Wilaya.query.all()
    return render_template('admin/commune_form.html', commune=commune, wilayas=wilayas)


@admin_bp.route('/communes/<int:id>/delete', methods=['POST'])
def delete_commune(id):
    try:
        commune = Commune.query.get_or_404(id)
        # التحقق من وجود أطباء أو عيادات مرتبطة
        if commune.doctors.count() > 0 or commune.clinics.count() > 0:
            flash('لا يمكن حذف البلدية لأنها مرتبطة بأطباء أو عيادات.', 'error')
            return redirect(url_for('admin.communes'))
        db.session.delete(commune)
        db.session.commit()
        flash('تم حذف البلدية بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('admin.communes'))


# ============================================================
# إدارة الخدمات (كاملة)
# ============================================================

@admin_bp.route('/services')
def services():
    services = Service.query.order_by(Service.name_ar).all()
    return render_template('admin/services.html', services=services)


@admin_bp.route('/services/add', methods=['GET', 'POST'])
def add_service():
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            name_ar = request.form.get('name_ar', '').strip()
            description = request.form.get('description', '').strip()
            description_ar = request.form.get('description_ar', '').strip()
            price = request.form.get('price', type=float)
            if not name or not name_ar:
                flash('يرجى ملء جميع المعلومات الأساسية.', 'error')
                return render_template('admin/service_form.html')
            if Service.query.filter_by(name=name).first():
                flash('الخدمة موجودة مسبقاً.', 'error')
                return render_template('admin/service_form.html')
            service = Service(
                name=name,
                name_ar=name_ar,
                description=description,
                description_ar=description_ar,
                price=price,
                is_active=True
            )
            db.session.add(service)
            db.session.commit()
            flash('تم إضافة الخدمة بنجاح.', 'success')
            return redirect(url_for('admin.services'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')
    return render_template('admin/service_form.html')


@admin_bp.route('/services/<int:id>/edit', methods=['GET', 'POST'])
def edit_service(id):
    service = Service.query.get_or_404(id)
    if request.method == 'POST':
        try:
            service.name = request.form.get('name', '').strip()
            service.name_ar = request.form.get('name_ar', '').strip()
            service.description = request.form.get('description', '').strip()
            service.description_ar = request.form.get('description_ar', '').strip()
            service.price = request.form.get('price', type=float)
            db.session.commit()
            flash('تم تحديث الخدمة بنجاح.', 'success')
            return redirect(url_for('admin.services'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')
    return render_template('admin/service_form.html', service=service)


@admin_bp.route('/services/<int:id>/delete', methods=['POST'])
def delete_service(id):
    try:
        service = Service.query.get_or_404(id)
        # التحقق من وجود خدمات مرتبطة بأطباء
        if service.doctor_services.count() > 0:
            flash('لا يمكن حذف الخدمة لأنها مرتبطة بأطباء.', 'error')
            return redirect(url_for('admin.services'))
        db.session.delete(service)
        db.session.commit()
        flash('تم حذف الخدمة بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('admin.services'))


# ============================================================
# إدارة البلاغات
# ============================================================

@admin_bp.route('/reports')
def reports():
    reports = Report.query.order_by(Report.created_at.desc()).all()
    return render_template('admin/reports.html', reports=reports)


@admin_bp.route('/reports/<int:id>/update', methods=['POST'])
def update_report(id):
    try:
        report = Report.query.get_or_404(id)
        report.status = request.form.get('status')
        report.admin_notes = request.form.get('admin_notes')
        db.session.commit()
        flash('تم تحديث البلاغ بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('admin.reports'))


# ============================================================
# إعدادات المنصة
# ============================================================

@admin_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingsForm()
    settings = PlatformSetting.query.all()
    settings_dict = {s.key: s.value for s in settings}
    if form.validate_on_submit():
        try:
            for key, value in form.data.items():
                if key in settings_dict:
                    setting = PlatformSetting.query.filter_by(key=key).first()
                    if setting:
                        setting.value = value
            db.session.commit()
            flash('تم تحديث الإعدادات بنجاح', 'success')
            return redirect(url_for('admin.settings'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ: {str(e)}', 'danger')
    for key, value in settings_dict.items():
        if hasattr(form, key):
            getattr(form, key).data = value
    return render_template('admin/settings.html', form=form)
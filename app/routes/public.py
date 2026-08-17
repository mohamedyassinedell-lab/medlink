from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from ..extensions import db
from ..models import Doctor, Specialty, Wilaya, Commune, Clinic, Service, Report
from ..services.status_service import StatusService
from sqlalchemy import or_

public_bp = Blueprint('public', __name__)


@public_bp.context_processor
def inject_public_data():
    try:
        specialties = Specialty.query.filter_by(is_active=True).all()
    except Exception:
        specialties = []
    return {'specialties': specialties}


@public_bp.route('/')
def index():
    doctors = Doctor.query.filter_by(is_published=True, is_active=True).limit(8).all()
    specialties = Specialty.query.filter_by(is_active=True).all()
    wilayas = Wilaya.query.all()

    doctor_count = Doctor.query.filter_by(is_published=True, is_active=True).count()
    clinic_count = Clinic.query.filter_by(is_active=True).count()
    specialty_count = Specialty.query.filter_by(is_active=True).count()
    wilaya_count = Wilaya.query.count()

    return render_template(
        'public/index.html',
        doctors=doctors,
        specialties=specialties,
        wilayas=wilayas,
        doctor_count=doctor_count,
        clinic_count=clinic_count,
        specialty_count=specialty_count,
        wilaya_count=wilaya_count
    )


@public_bp.route('/doctors')
def doctors():
    page = request.args.get('page', 1, type=int)
    per_page = 12

    query = Doctor.query.filter_by(is_published=True, is_active=True)

    search = request.args.get('search', '').strip()
    specialty = request.args.get('specialty', '').strip()
    wilaya = request.args.get('wilaya', '').strip()
    commune = request.args.get('commune', '').strip()
    accepts_new = request.args.get('accepts_new', '')

    if search:
        terms = search.split()
        for term in terms:
            query = query.filter(
                or_(
                    Doctor.first_name.ilike(f'%{term}%'),
                    Doctor.last_name.ilike(f'%{term}%'),
                    Doctor.first_name_ar.ilike(f'%{term}%'),
                    Doctor.last_name_ar.ilike(f'%{term}%')
                )
            )

    if specialty:
        query = query.join(Specialty).filter(
            or_(
                Specialty.name.ilike(f'%{specialty}%'),
                Specialty.name_ar.ilike(f'%{specialty}%')
            )
        )

    if wilaya:
        query = query.join(Wilaya, Doctor.wilaya_id == Wilaya.id).filter(
            or_(
                Wilaya.name.ilike(f'%{wilaya}%'),
                Wilaya.name_ar.ilike(f'%{wilaya}%')
            )
        )

    if commune:
        query = query.join(Commune, Doctor.commune_id == Commune.id).filter(
            or_(
                Commune.name.ilike(f'%{commune}%'),
                Commune.name_ar.ilike(f'%{commune}%')
            )
        )

    if accepts_new == '1':
        query = query.filter(Doctor.accepts_new_patients == True)

    query = query.order_by(Doctor.is_featured.desc(), Doctor.created_at.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    doctors_list = pagination.items

    specialties = Specialty.query.filter_by(is_active=True).all()
    wilayas = Wilaya.query.all()

    return render_template(
        'public/doctors.html',
        doctors=doctors_list,
        pagination=pagination,
        specialties=specialties,
        wilayas=wilayas,
        search=search,
        selected_specialty=specialty,
        selected_wilaya=wilaya
    )


@public_bp.route('/doctors/<slug>')
def doctor_detail(slug):
    try:
        doctor = Doctor.query.filter_by(slug=slug, is_published=True).first_or_404()
    except Exception:
        flash('الطبيب غير موجود', 'danger')
        return redirect(url_for('public.index'))

    try:
        services = doctor.services.all()
    except Exception:
        services = []

    try:
        working_hours = doctor.working_hours.all()
    except Exception:
        working_hours = []

    if working_hours:
        try:
            status = StatusService.get_status(doctor)
        except Exception:
            status = {'status': 'UNKNOWN', 'label': 'ℹ️', 'message': 'المعلومات غير متوفرة', 'return_date': None}
    else:
        status = {'status': 'UNKNOWN', 'label': 'ℹ️', 'message': 'أوقات العمل غير متوفرة', 'return_date': None}

    specialties = Specialty.query.filter_by(is_active=True).all()

    return render_template(
        'public/doctor_detail.html',
        doctor=doctor,
        status=status,
        services=services,
        working_hours=working_hours,
        specialties=specialties
    )


@public_bp.route('/report-doctor/<slug>', methods=['POST'])
def report_doctor(slug):
    doctor = Doctor.query.filter_by(slug=slug, is_published=True).first_or_404()

    issue_type = request.form.get('issue_type')
    description = request.form.get('description')
    reporter_name = request.form.get('reporter_name')
    reporter_email = request.form.get('reporter_email')
    reporter_phone = request.form.get('reporter_phone')

    if not issue_type or not description:
        flash('يرجى ملء جميع الحقول المطلوبة', 'danger')
        return redirect(url_for('public.doctor_detail', slug=slug))

    report = Report(
        doctor_id=doctor.id,
        issue_type=issue_type,
        description=description,
        reporter_name=reporter_name,
        reporter_email=reporter_email,
        reporter_phone=reporter_phone,
        status='pending'
    )

    db.session.add(report)
    db.session.commit()

    flash('تم إرسال البلاغ بنجاح، سيتم مراجعته قريباً', 'success')
    return redirect(url_for('public.doctor_detail', slug=slug))


@public_bp.route('/api/search-doctors')
def search_doctors():
    q = request.args.get('q', '').strip()
    results = []

    if len(q) >= 2:
        doctors = Doctor.query.filter(
            or_(
                Doctor.first_name.ilike(f'%{q}%'),
                Doctor.last_name.ilike(f'%{q}%'),
                Doctor.first_name_ar.ilike(f'%{q}%'),
                Doctor.last_name_ar.ilike(f'%{q}%')
            ),
            Doctor.is_published == True,
            Doctor.is_active == True
        ).limit(5).all()

        for doctor in doctors:
            results.append({
                'id': doctor.id,
                'name': doctor.full_name,
                'name_ar': doctor.full_name_ar,
                'slug': doctor.slug,
                'specialty': doctor.specialty_ref.name_ar if doctor.specialty_ref else '',
                'profile_image': doctor.profile_image or '/static/images/default-avatar.jpg'
            })

    return jsonify(results)


@public_bp.route('/about')
def about():
    return render_template('public/about.html')
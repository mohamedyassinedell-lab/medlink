from flask import Blueprint, render_template, request, jsonify
from ..extensions import db
from ..models import (
    Doctor,
    Specialty,
    Wilaya,
    Commune,
    Clinic,
    Service
)
from ..services.status_service import StatusService
from sqlalchemy import or_


public_bp = Blueprint('public', __name__)


# =========================================================
# توفير التخصصات للـ base.html
# =========================================================

@public_bp.app_context_processor
def inject_global_data():
    return {
        'specialties': Specialty.query.filter_by(is_active=True).all()
    }


# =========================================================
# الصفحة الرئيسية
# =========================================================

@public_bp.route('/')
def index():
    """Homepage"""

    doctors = Doctor.query.filter_by(
        is_published=True,
        is_active=True
    ).limit(8).all()

    specialties = Specialty.query.filter_by(
        is_active=True
    ).all()

    wilayas = Wilaya.query.all()

    doctor_count = Doctor.query.filter_by(
        is_published=True,
        is_active=True
    ).count()

    clinic_count = Clinic.query.filter_by(
        is_active=True
    ).count()

    specialty_count = Specialty.query.filter_by(
        is_active=True
    ).count()

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


# =========================================================
# قائمة الأطباء
# =========================================================

@public_bp.route('/doctors')
def doctors():
    """List all published and active doctors with filters"""

    page = request.args.get('page', 1, type=int)
    per_page = 12

    query = Doctor.query.filter_by(
        is_published=True,
        is_active=True
    )

    # -----------------------------------------------------
    # الفلاتر
    # -----------------------------------------------------

    search = request.args.get('search', '')
    specialty = request.args.get('specialty', '')
    wilaya = request.args.get('wilaya', '')
    commune = request.args.get('commune', '')
    accepts_new = request.args.get('accepts_new', '')

    # -----------------------------------------------------
    # البحث
    # -----------------------------------------------------

    if search:
        search_terms = search.split()

        for term in search_terms:
            query = query.filter(
                or_(
                    Doctor.first_name.ilike(f'%{term}%'),
                    Doctor.last_name.ilike(f'%{term}%'),
                    Doctor.first_name_ar.ilike(f'%{term}%'),
                    Doctor.last_name_ar.ilike(f'%{term}%')
                )
            )

    # -----------------------------------------------------
    # التخصص
    # -----------------------------------------------------

    if specialty:
        query = query.join(
            Specialty,
            Doctor.specialty_id == Specialty.id
        ).filter(
            or_(
                Specialty.name.ilike(f'%{specialty}%'),
                Specialty.name_ar.ilike(f'%{specialty}%')
            )
        )

    # -----------------------------------------------------
    # الولاية
    # -----------------------------------------------------

    if wilaya:
        query = query.join(
            Wilaya,
            Doctor.wilaya_id == Wilaya.id
        ).filter(
            or_(
                Wilaya.name.ilike(f'%{wilaya}%'),
                Wilaya.name_ar.ilike(f'%{wilaya}%')
            )
        )

    # -----------------------------------------------------
    # البلدية
    # -----------------------------------------------------

    if commune:
        query = query.join(
            Commune,
            Doctor.commune_id == Commune.id
        ).filter(
            or_(
                Commune.name.ilike(f'%{commune}%'),
                Commune.name_ar.ilike(f'%{commune}%')
            )
        )

    # -----------------------------------------------------
    # يقبل مرضى جدد
    # -----------------------------------------------------

    if accepts_new == '1':
        query = query.filter(
            Doctor.accepts_new_patients == True
        )

    # -----------------------------------------------------
    # الترتيب
    # -----------------------------------------------------

    query = query.order_by(
        Doctor.is_featured.desc(),
        Doctor.created_at.desc()
    )

    # -----------------------------------------------------
    # Pagination
    # -----------------------------------------------------

    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    doctors_list = pagination.items

    specialties_list = Specialty.query.filter_by(
        is_active=True
    ).all()

    wilayas = Wilaya.query.all()

    return render_template(
        'public/doctors.html',
        doctors=doctors_list,
        pagination=pagination,
        specialties=specialties_list,
        wilayas=wilayas,
        search=search,
        selected_specialty=specialty,
        selected_wilaya=wilaya
    )


# =========================================================
# ملف الطبيب
# =========================================================

@public_bp.route('/doctors/<slug>')
def doctor_detail(slug):
    """
    عرض ملف الطبيب.

    ملاحظة:
    هنا نتحقق فقط من is_published.
    لا نشترط is_active.
    """

    doctor = Doctor.query.filter_by(
        slug=slug,
        is_published=True
    ).first_or_404()

    # -----------------------------------------------------
    # حالة الطبيب
    # -----------------------------------------------------

    status = StatusService.get_status(doctor)

    # -----------------------------------------------------
    # الخدمات
    # -----------------------------------------------------

    services = doctor.services.all()

    # -----------------------------------------------------
    # أوقات العمل
    # -----------------------------------------------------

    working_hours = doctor.working_hours.all()

    # -----------------------------------------------------
    # التخصصات
    # -----------------------------------------------------

    specialties_list = Specialty.query.filter_by(
        is_active=True
    ).all()

    # -----------------------------------------------------
    # عرض الملف
    # -----------------------------------------------------

    return render_template(
        'public/doctor_detail.html',
        doctor=doctor,
        status=status,
        services=services,
        working_hours=working_hours,
        specialties=specialties_list
    )


# =========================================================
# البحث عن الأطباء API
# =========================================================

@public_bp.route('/api/search-doctors')
def search_doctors():
    """API endpoint for doctor search"""

    q = request.args.get('q', '')
    results = []

    if len(q) >= 2:

        doctors_list = Doctor.query.filter(
            or_(
                Doctor.first_name.ilike(f'%{q}%'),
                Doctor.last_name.ilike(f'%{q}%'),
                Doctor.first_name_ar.ilike(f'%{q}%'),
                Doctor.last_name_ar.ilike(f'%{q}%')
            ),
            Doctor.is_published == True,
            Doctor.is_active == True
        ).limit(5).all()

        for doctor in doctors_list:

            results.append({
                'id': doctor.id,
                'name': doctor.full_name,
                'name_ar': doctor.full_name_ar,
                'slug': doctor.slug,
                'specialty': (
                    doctor.specialty_ref.name_ar
                    if doctor.specialty_ref
                    else ''
                ),
                'profile_image': (
                    doctor.profile_image
                    or '/static/images/default-avatar.jpg'
                )
            })

    return jsonify(results)


# =========================================================
# About
# =========================================================

@public_bp.route('/about')
def about():
    """About page"""

    return render_template(
        'public/about.html'
    )
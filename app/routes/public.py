from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, send_from_directory, current_app
from ..extensions import db
from ..models import (
    Doctor,
    Specialty,
    Wilaya,
    Commune,
    Clinic,
    Service,
    Report
)
from ..services.status_service import StatusService
from sqlalchemy import or_
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


public_bp = Blueprint('public', __name__)


# ============================================================
# PUBLIC CONTEXT
# ============================================================

@public_bp.context_processor
def inject_public_data():
    """
    Variables available automatically in all public templates.
    This prevents 'specialties is undefined' errors in base.html.
    """
    try:
        specialties = Specialty.query.filter_by(
            is_active=True
        ).all()
    except Exception:
        specialties = []

    return {
        'specialties': specialties
    }


# ============================================================
# HOME
# ============================================================

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


# ============================================================
# DOCTORS LIST
# ============================================================

@public_bp.route('/doctors')
def doctors():
    """List all doctors with filters"""

    page = request.args.get('page', 1, type=int)
    per_page = 12

    query = Doctor.query.filter_by(
        is_published=True,
        is_active=True
    )

    # Filters
    search = request.args.get('search', '').strip()
    specialty = request.args.get('specialty', '').strip()
    wilaya = request.args.get('wilaya', '').strip()
    commune = request.args.get('commune', '').strip()
    accepts_new = request.args.get('accepts_new', '')
    simple_mode = request.args.get('simple', '0') == '1'

    if search:
        if simple_mode:
            # البحث فقط في اسم الطبيب (من الصفحة الرئيسية)
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
        else:
            # البحث الكامل (من صفحة الأطباء)
            terms = search.split()
            for term in terms:
                query = query.filter(
                    or_(
                        Doctor.first_name.ilike(f'%{term}%'),
                        Doctor.last_name.ilike(f'%{term}%'),
                        Doctor.first_name_ar.ilike(f'%{term}%'),
                        Doctor.last_name_ar.ilike(f'%{term}%'),
                        Specialty.name.ilike(f'%{term}%'),
                        Specialty.name_ar.ilike(f'%{term}%'),
                        Wilaya.name.ilike(f'%{term}%'),
                        Wilaya.name_ar.ilike(f'%{term}%'),
                        Commune.name.ilike(f'%{term}%'),
                        Commune.name_ar.ilike(f'%{term}%')
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

    query = query.order_by(
        Doctor.is_featured.desc(),
        Doctor.created_at.desc()
    )

    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    doctors_list = pagination.items

    specialties = Specialty.query.filter_by(
        is_active=True
    ).all()

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


# ============================================================
# DOCTOR DETAIL
# ============================================================

@public_bp.route('/doctors/<slug>')
def doctor_detail(slug):
    """
    Public doctor profile.
    """

    doctor = Doctor.query.filter_by(
        slug=slug,
        is_published=True
    ).first_or_404()

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
            status = {
                'status': 'UNKNOWN',
                'label': 'ℹ️',
                'message': 'المعلومات غير متوفرة',
                'return_date': None
            }
    else:
        status = {
            'status': 'UNKNOWN',
            'label': 'ℹ️',
            'message': 'أوقات العمل غير متوفرة',
            'return_date': None
        }

    specialties = Specialty.query.filter_by(
        is_active=True
    ).all()

    return render_template(
        'public/doctor_detail.html',
        doctor=doctor,
        status=status,
        services=services,
        working_hours=working_hours,
        specialties=specialties
    )


# ============================================================
# REPORT DOCTOR
# ============================================================

@public_bp.route('/report-doctor/<slug>', methods=['POST'])
def report_doctor(slug):
    """Handle doctor report submission"""
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


# ============================================================
# SEARCH API
# ============================================================

@public_bp.route('/api/search-doctors')
def search_doctors():
    """API endpoint for doctor search"""

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


# ============================================================
# ABOUT
# ============================================================

@public_bp.route('/about')
def about():
    """About page"""

    return render_template(
        'public/about.html'
    )


# ============================================================
# SITEMAP.XML (SEO)
# ============================================================

@public_bp.route('/sitemap.xml')
def sitemap():
    """Generate sitemap.xml dynamically for SEO"""
    
    urlset = Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # الصفحة الرئيسية
    url = SubElement(urlset, 'url')
    loc = SubElement(url, 'loc')
    loc.text = request.url_root
    priority = SubElement(url, 'priority')
    priority.text = '1.0'
    
    # صفحة الأطباء
    url = SubElement(urlset, 'url')
    loc = SubElement(url, 'loc')
    loc.text = request.url_root + 'doctors'
    priority = SubElement(url, 'priority')
    priority.text = '0.8'
    
    # صفحة من نحن
    url = SubElement(urlset, 'url')
    loc = SubElement(url, 'loc')
    loc.text = request.url_root + 'about'
    priority = SubElement(url, 'priority')
    priority.text = '0.5'
    
    # الأطباء المنشورون
    doctors = Doctor.query.filter_by(is_published=True, is_active=True).all()
    for doctor in doctors:
        url = SubElement(urlset, 'url')
        loc = SubElement(url, 'loc')
        loc.text = request.url_root + 'doctors/' + doctor.slug
        priority = SubElement(url, 'priority')
        priority.text = '0.7'
    
    # التخصصات النشطة
    specialties = Specialty.query.filter_by(is_active=True).all()
    for specialty in specialties:
        url = SubElement(urlset, 'url')
        loc = SubElement(url, 'loc')
        loc.text = request.url_root + 'doctors?specialty=' + specialty.name
        priority = SubElement(url, 'priority')
        priority.text = '0.6'
    
    # الولايات
    wilayas = Wilaya.query.all()
    for wilaya in wilayas:
        url = SubElement(urlset, 'url')
        loc = SubElement(url, 'loc')
        loc.text = request.url_root + 'doctors?wilaya=' + wilaya.name
        priority = SubElement(url, 'priority')
        priority.text = '0.6'
    
    # تحويل إلى XML
    rough_string = tostring(urlset, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    return pretty_xml, 200, {'Content-Type': 'application/xml'}


# ============================================================
# ROBOTS.TXT
# ============================================================

@public_bp.route('/robots.txt')
def robots_txt():
    """Serve robots.txt file"""
    return send_from_directory('static', 'robots.txt')


# ============================================================
# GOOGLE VERIFICATION FILE
# ============================================================

@public_bp.route('/google57c881331ae6cd7c.html')
def google_verification():
    """Serve Google Search Console verification file"""
    return send_from_directory('static', 'google57c881331ae6cd7c.html')


# ============================================================
# STATIC FILES (Fallback)
# ============================================================

@public_bp.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)
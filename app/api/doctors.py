from flask import request, jsonify
from sqlalchemy import or_
from app.models import Doctor, Report
from app.extensions import db
from app.api.blueprint import api_bp
from app.api.utils import serialize_doctor


@api_bp.route('/doctors', methods=['GET'])
def list_doctors():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 15, type=int), 50)

    query = Doctor.query.filter_by(is_published=True, is_active=True)

    search = request.args.get('search', '').strip()
    specialty_id = request.args.get('specialty_id', type=int)
    wilaya_id = request.args.get('wilaya_id', type=int)
    commune_id = request.args.get('commune_id', type=int)
    accepts_new = request.args.get('accepts_new', type=str)
    featured = request.args.get('featured', type=str)

    if search:
        for term in search.split():
            query = query.filter(or_(
                Doctor.first_name.ilike(f'%{term}%'),
                Doctor.last_name.ilike(f'%{term}%'),
                Doctor.first_name_ar.ilike(f'%{term}%'),
                Doctor.last_name_ar.ilike(f'%{term}%'),
            ))

    if specialty_id:
        query = query.filter(Doctor.specialty_id == specialty_id)
    if wilaya_id:
        query = query.filter(Doctor.wilaya_id == wilaya_id)
    if commune_id:
        query = query.filter(Doctor.commune_id == commune_id)
    if accepts_new == 'true':
        query = query.filter(Doctor.accepts_new_patients == True)
    if featured == 'true':
        query = query.filter(Doctor.is_featured == True)

    query = query.order_by(
        Doctor.is_featured.desc(),
        Doctor.created_at.desc(),
    )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'doctors': [serialize_doctor(d) for d in pagination.items],
        'pagination': {
            'page': pagination.page,
            'pages': pagination.pages,
            'per_page': per_page,
            'total': pagination.total,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev,
        },
    })


@api_bp.route('/doctors/<slug>', methods=['GET'])
def doctor_detail(slug):
    doctor = Doctor.query.filter_by(
        slug=slug, is_published=True, is_active=True
    ).first()

    if not doctor:
        return jsonify({'error': 'الطبيب غير موجود'}), 404

    return jsonify(serialize_doctor(doctor, full=True))


@api_bp.route('/search/suggest', methods=['GET'])
def search_suggest():
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return jsonify([])

    doctors = Doctor.query.filter(
        or_(
            Doctor.first_name.ilike(f'%{q}%'),
            Doctor.last_name.ilike(f'%{q}%'),
            Doctor.first_name_ar.ilike(f'%{q}%'),
            Doctor.last_name_ar.ilike(f'%{q}%'),
        ),
        Doctor.is_published == True,
        Doctor.is_active == True,
    ).limit(8).all()

    return jsonify([
        {
            'slug': d.slug,
            'name': d.full_name_ar,
            'specialty': d.specialty_ref.name_ar if d.specialty_ref else '',
            'image': d.profile_image,
        }
        for d in doctors
    ])


@api_bp.route('/doctors/<slug>/report', methods=['POST'])
def report_doctor(slug):
    doctor = Doctor.query.filter_by(slug=slug, is_published=True).first()
    if not doctor:
        return jsonify({'error': 'الطبيب غير موجود'}), 404

    data = request.get_json() or {}
    if not data.get('issue_type') or not data.get('description'):
        return jsonify({'error': 'الحقول المطلوبة ناقصة'}), 400

    report = Report(
        doctor_id=doctor.id,
        issue_type=data['issue_type'],
        description=data['description'],
        reporter_name=data.get('reporter_name'),
        reporter_email=data.get('reporter_email'),
        reporter_phone=data.get('reporter_phone'),
        status='pending',
    )
    db.session.add(report)
    db.session.commit()

    return jsonify({'message': 'تم إرسال البلاغ بنجاح'}), 201


@api_bp.route('/home', methods=['GET'])
def home_data():
    featured = (
        Doctor.query
        .filter_by(is_published=True, is_active=True, is_featured=True)
        .limit(6)
        .all()
    )
    recent = (
        Doctor.query
        .filter_by(is_published=True, is_active=True)
        .order_by(Doctor.created_at.desc())
        .limit(6)
        .all()
    )
    from app.models import Specialty, Wilaya
    from app.api.utils import serialize_specialty, serialize_wilaya

    specialties = Specialty.query.filter_by(is_active=True).all()
    wilayas = Wilaya.query.order_by(Wilaya.code).all()

    return jsonify({
        'featured': [serialize_doctor(d) for d in featured],
        'recent': [serialize_doctor(d) for d in recent],
        'specialties': [serialize_specialty(s) for s in specialties],
        'wilayas': [serialize_wilaya(w) for w in wilayas],
        'stats': {
            'doctors': Doctor.query.filter_by(is_published=True).count(),
            'specialties': len(specialties),
            'wilayas': len(wilayas),
        },
    })
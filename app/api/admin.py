from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import (
    User, Doctor, Report, Clinic, Specialty, Wilaya, Commune, PlatformSetting
)
from app.api.blueprint import api_bp


def _check_admin():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or not user.is_admin:
        return None
    return user


# ============================================================
# STATS
# ============================================================

@api_bp.route('/admin/stats', methods=['GET'])
@jwt_required()
def admin_stats():
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    return jsonify({
        'doctors': Doctor.query.count(),
        'published': Doctor.query.filter_by(is_published=True).count(),
        'pending': Doctor.query.filter_by(is_approved=False).count(),
        'reports': Report.query.filter_by(status='pending').count(),
        'clinics': Clinic.query.count(),
        'specialties': Specialty.query.count(),
        'wilayas': Wilaya.query.count(),
        'users': User.query.count(),
    })


# ============================================================
# DOCTORS MANAGEMENT
# ============================================================

@api_bp.route('/admin/doctors', methods=['GET'])
@jwt_required()
def admin_list_doctors():
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    from app.api.utils import serialize_doctor
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    search = request.args.get('search', '').strip()

    query = Doctor.query
    if search:
        query = query.filter(
            db.or_(
                Doctor.first_name_ar.ilike(f'%{search}%'),
                Doctor.last_name_ar.ilike(f'%{search}%'),
                Doctor.first_name.ilike(f'%{search}%'),
                Doctor.last_name.ilike(f'%{search}%'),
            )
        )
    query = query.order_by(Doctor.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'doctors': [serialize_doctor(d) for d in pagination.items],
        'pagination': {
            'page': pagination.page,
            'pages': pagination.pages,
            'total': pagination.total,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev,
        }
    })


@api_bp.route('/admin/doctors/pending', methods=['GET'])
@jwt_required()
def admin_pending_doctors():
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    from app.api.utils import serialize_doctor
    doctors = Doctor.query.filter_by(is_approved=False).order_by(Doctor.created_at.desc()).all()
    return jsonify([serialize_doctor(d, full=True) for d in doctors])


@api_bp.route('/admin/doctors/<int:id>', methods=['GET'])
@jwt_required()
def admin_get_doctor(id):
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    from app.api.utils import serialize_doctor
    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({'error': 'الطبيب غير موجود'}), 404
    return jsonify(serialize_doctor(doctor, full=True))


@api_bp.route('/admin/doctors', methods=['POST'])
@jwt_required()
def admin_add_doctor():
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    data = request.get_json() or {}
    if not data.get('wilaya_id'):
        return jsonify({'error': 'الولاية مطلوبة'}), 400

    # إنشاء بلدية إن لم تكن موجودة
    commune = None
    if data.get('commune_name'):
        commune = Commune.query.filter(
            Commune.wilaya_id == data['wilaya_id'],
            (Commune.name == data['commune_name']) | (Commune.name_ar == data['commune_name'])
        ).first()
        if not commune:
            commune = Commune(name=data['commune_name'], name_ar=data['commune_name'], wilaya_id=data['wilaya_id'])
            db.session.add(commune)
            db.session.flush()

    # إنشاء عيادة إن لم تكن موجودة
    clinic = None
    if data.get('clinic_name'):
        clinic = Clinic.query.filter(
            (Clinic.name == data['clinic_name']) | (Clinic.name_ar == data['clinic_name'])
        ).first()
        if not clinic:
            clinic = Clinic(
                name=data['clinic_name'], name_ar=data['clinic_name'],
                address='', address_ar='', wilaya_id=data['wilaya_id'],
                commune_id=commune.id if commune else None, phone='', is_active=True
            )
            db.session.add(clinic)
            db.session.flush()

    doctor = Doctor(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        first_name_ar=data.get('first_name_ar'),
        last_name_ar=data.get('last_name_ar'),
        specialty_id=data.get('specialty_id'),
        sub_specialty=data.get('sub_specialty'),
        experience_years=data.get('experience_years'),
        bio=data.get('bio'),
        bio_ar=data.get('bio_ar'),
        wilaya_id=data['wilaya_id'],
        commune_id=commune.id if commune else None,
        address=data.get('address'),
        address_ar=data.get('address_ar'),
        phone=data.get('phone'),
        phone_secondary=data.get('phone_secondary'),
        email=data.get('email'),
        clinic_id=clinic.id if clinic else None,
        accepts_new_patients=data.get('accepts_new_patients', True),
        is_verified=data.get('is_verified', True),
        is_featured=data.get('is_featured', False),
        is_published=True,
        is_approved=True,
        is_active=True,
    )
    doctor.slug = doctor.generate_slug()
    db.session.add(doctor)
    db.session.commit()

    from app.api.utils import serialize_doctor
    return jsonify({'message': 'تم إضافة الطبيب', 'doctor': serialize_doctor(doctor, full=True)}), 201


@api_bp.route('/admin/doctors/<int:id>', methods=['PUT'])
@jwt_required()
def admin_edit_doctor(id):
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({'error': 'الطبيب غير موجود'}), 404

    data = request.get_json() or {}

    for field in ['first_name', 'last_name', 'first_name_ar', 'last_name_ar',
                  'sub_specialty', 'bio', 'bio_ar', 'address', 'address_ar',
                  'phone', 'phone_secondary', 'email']:
        if field in data:
            setattr(doctor, field, data[field])

    if 'specialty_id' in data:
        doctor.specialty_id = data['specialty_id']
    if 'experience_years' in data:
        doctor.experience_years = data['experience_years']
    if 'accepts_new_patients' in data:
        doctor.accepts_new_patients = data['accepts_new_patients']
    if 'is_verified' in data:
        doctor.is_verified = data['is_verified']
    if 'is_featured' in data:
        doctor.is_featured = data['is_featured']
    if 'is_published' in data:
        doctor.is_published = data['is_published']

    doctor.slug = doctor.generate_slug()
    db.session.commit()

    from app.api.utils import serialize_doctor
    return jsonify({'message': 'تم التحديث', 'doctor': serialize_doctor(doctor, full=True)})


@api_bp.route('/admin/doctors/<int:id>/approve', methods=['POST'])
@jwt_required()
def admin_approve_doctor(id):
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({'error': 'الطبيب غير موجود'}), 404

    doctor.is_approved = True
    doctor.is_published = True
    db.session.commit()
    return jsonify({'message': 'تمت الموافقة'})


@api_bp.route('/admin/doctors/<int:id>/toggle-publish', methods=['POST'])
@jwt_required()
def admin_toggle_publish(id):
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({'error': 'الطبيب غير موجود'}), 404

    doctor.is_published = not doctor.is_published
    db.session.commit()
    return jsonify({'message': 'تم التحديث', 'is_published': doctor.is_published})


@api_bp.route('/admin/doctors/<int:id>', methods=['DELETE'])
@jwt_required()
def admin_delete_doctor(id):
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({'error': 'الطبيب غير موجود'}), 404

    db.session.delete(doctor)
    db.session.commit()
    return jsonify({'message': 'تم الحذف'})


# ============================================================
# CLINICS MANAGEMENT
# ============================================================

@api_bp.route('/admin/clinics', methods=['GET'])
@jwt_required()
def admin_list_clinics():
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    clinics = Clinic.query.order_by(Clinic.created_at.desc()).all()
    return jsonify([
        {
            'id': c.id,
            'name': c.name,
            'name_ar': c.name_ar,
            'phone': c.phone,
            'address': c.address_ar or c.address,
            'wilaya': c.wilaya_ref.name_ar if c.wilaya_ref else '',
            'doctors_count': c.doctors.count(),
        }
        for c in clinics
    ])


@api_bp.route('/admin/clinics/<int:id>', methods=['DELETE'])
@jwt_required()
def admin_delete_clinic(id):
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    clinic = Clinic.query.get(id)
    if not clinic:
        return jsonify({'error': 'العيادة غير موجودة'}), 404

    if clinic.doctors.count() > 0:
        return jsonify({'error': 'لا يمكن حذف عيادة مرتبطة بأطباء'}), 400

    db.session.delete(clinic)
    db.session.commit()
    return jsonify({'message': 'تم الحذف'})


# ============================================================
# SPECIALTIES
# ============================================================

@api_bp.route('/admin/specialties', methods=['GET'])
@jwt_required()
def admin_list_specialties():
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    items = Specialty.query.order_by(Specialty.name_ar).all()
    return jsonify([
        {
            'id': s.id,
            'name': s.name,
            'name_ar': s.name_ar,
            'icon': s.icon,
            'is_active': s.is_active,
            'doctors_count': s.doctors.filter_by(is_published=True).count(),
        }
        for s in items
    ])


@api_bp.route('/admin/specialties', methods=['POST'])
@jwt_required()
def admin_add_specialty():
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    data = request.get_json() or {}
    if not data.get('name') or not data.get('name_ar'):
        return jsonify({'error': 'الاسم مطلوب'}), 400

    if Specialty.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'التخصص موجود مسبقاً'}), 409

    specialty = Specialty(
        name=data['name'],
        name_ar=data['name_ar'],
        icon=data.get('icon', 'stethoscope'),
        is_active=True,
    )
    db.session.add(specialty)
    db.session.commit()
    return jsonify({'message': 'تمت الإضافة', 'id': specialty.id}), 201


@api_bp.route('/admin/specialties/<int:id>', methods=['DELETE'])
@jwt_required()
def admin_delete_specialty(id):
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    specialty = Specialty.query.get(id)
    if not specialty:
        return jsonify({'error': 'غير موجود'}), 404

    if specialty.doctors.filter_by(is_published=True).count() > 0:
        return jsonify({'error': 'مرتبط بأطباء'}), 400

    db.session.delete(specialty)
    db.session.commit()
    return jsonify({'message': 'تم الحذف'})


# ============================================================
# WILAYAS
# ============================================================

@api_bp.route('/admin/wilayas', methods=['GET'])
@jwt_required()
def admin_list_wilayas():
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    items = Wilaya.query.order_by(Wilaya.code).all()
    return jsonify([
        {
            'id': w.id,
            'code': w.code,
            'name': w.name,
            'name_ar': w.name_ar,
            'doctors_count': w.doctors.count(),
        }
        for w in items
    ])


# ============================================================
# REPORTS
# ============================================================

@api_bp.route('/admin/reports', methods=['GET'])
@jwt_required()
def admin_reports():
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    reports = Report.query.order_by(Report.created_at.desc()).all()
    return jsonify([
        {
            'id': r.id,
            'issue_type': r.issue_type,
            'description': r.description,
            'status': r.status,
            'reporter_name': r.reporter_name,
            'reporter_email': r.reporter_email,
            'created_at': r.created_at.isoformat() if r.created_at else None,
            'doctor': {
                'id': r.doctor.id,
                'name': r.doctor.full_name_ar or r.doctor.full_name,
            } if r.doctor else None,
        }
        for r in reports
    ])


@api_bp.route('/admin/reports/<int:id>', methods=['PUT'])
@jwt_required()
def admin_update_report(id):
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    report = Report.query.get(id)
    if not report:
        return jsonify({'error': 'البلاغ غير موجود'}), 404

    data = request.get_json() or {}
    if 'status' in data:
        report.status = data['status']
    if 'admin_notes' in data:
        report.admin_notes = data['admin_notes']

    db.session.commit()
    return jsonify({'message': 'تم التحديث'})


@api_bp.route('/admin/reports/<int:id>', methods=['DELETE'])
@jwt_required()
def admin_delete_report(id):
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    report = Report.query.get(id)
    if not report:
        return jsonify({'error': 'البلاغ غير موجود'}), 404

    db.session.delete(report)
    db.session.commit()
    return jsonify({'message': 'تم الحذف'})
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Doctor, Commune, Clinic
from app.api.blueprint import api_bp
from app.api.utils import serialize_doctor


@api_bp.route('/user/doctors', methods=['GET'])
@jwt_required()
def my_doctors():
    user_id = int(get_jwt_identity())
    doctors = (
        Doctor.query
        .filter_by(submitted_by=user_id)
        .order_by(Doctor.created_at.desc())
        .all()
    )
    return jsonify([serialize_doctor(d) for d in doctors])


@api_bp.route('/user/doctors', methods=['POST'])
@jwt_required()
def add_my_doctor():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    if not data.get('wilaya_id'):
        return jsonify({'error': 'الولاية مطلوبة'}), 400

    # إنشاء/إيجاد البلدية
    commune = None
    if data.get('commune_name'):
        commune = Commune.query.filter(
            Commune.wilaya_id == data['wilaya_id'],
            (Commune.name == data['commune_name']) |
            (Commune.name_ar == data['commune_name'])
        ).first()
        if not commune:
            commune = Commune(
                name=data['commune_name'],
                name_ar=data['commune_name'],
                wilaya_id=data['wilaya_id'],
            )
            db.session.add(commune)
            db.session.flush()

    # إنشاء/إيجاد العيادة
    clinic = None
    if data.get('clinic_name'):
        clinic = Clinic.query.filter(
            (Clinic.name == data['clinic_name']) |
            (Clinic.name_ar == data['clinic_name'])
        ).first()
        if not clinic:
            clinic = Clinic(
                name=data['clinic_name'],
                name_ar=data['clinic_name'],
                address='',
                address_ar='',
                wilaya_id=data['wilaya_id'],
                commune_id=commune.id if commune else None,
                phone='',
                is_active=True,
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
        is_verified=False,
        is_featured=False,
        is_published=False,
        is_approved=False,
        is_active=True,
        submitted_by=user_id,
    )
    doctor.slug = doctor.generate_slug()

    db.session.add(doctor)
    db.session.commit()

    return jsonify({
        'message': 'تم إرسال الطبيب للمراجعة',
        'doctor': serialize_doctor(doctor),
    }), 201
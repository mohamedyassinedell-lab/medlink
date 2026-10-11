from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import User, Doctor, Report, Clinic, Specialty
from app.api.blueprint import api_bp


def _check_admin():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or not user.is_admin:
        return None
    return user


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
    })


@api_bp.route('/admin/doctors/pending', methods=['GET'])
@jwt_required()
def admin_pending_doctors():
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    from app.api.utils import serialize_doctor
    doctors = Doctor.query.filter_by(is_approved=False).order_by(Doctor.created_at.desc()).all()
    return jsonify([serialize_doctor(d) for d in doctors])


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


@api_bp.route('/admin/doctors/<int:id>', methods=['DELETE'])
@jwt_required()
def admin_reject_doctor(id):
    if not _check_admin():
        return jsonify({'error': 'غير مصرح'}), 403

    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({'error': 'الطبيب غير موجود'}), 404

    db.session.delete(doctor)
    db.session.commit()
    return jsonify({'message': 'تم الحذف'})


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
            'created_at': r.created_at.isoformat() if r.created_at else None,
            'doctor': {
                'id': r.doctor.id,
                'name': r.doctor.full_name_ar or r.doctor.full_name,
            } if r.doctor else None,
        }
        for r in reports
    ])
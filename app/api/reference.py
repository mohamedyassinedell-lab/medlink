from flask import jsonify
from app.models import Specialty, Wilaya, Commune, Service
from app.api.blueprint import api_bp
from app.api.utils import serialize_wilaya, serialize_commune, serialize_specialty


@api_bp.route('/specialties', methods=['GET'])
def list_specialties():
    items = Specialty.query.filter_by(is_active=True).all()
    return jsonify([serialize_specialty(s) for s in items])


@api_bp.route('/wilayas', methods=['GET'])
def list_wilayas():
    items = Wilaya.query.order_by(Wilaya.code).all()
    return jsonify([serialize_wilaya(w) for w in items])


@api_bp.route('/wilayas/<int:wilaya_id>/communes', methods=['GET'])
def list_communes(wilaya_id):
    items = (
        Commune.query
        .filter_by(wilaya_id=wilaya_id)
        .order_by(Commune.name_ar)
        .all()
    )
    return jsonify([serialize_commune(c) for c in items])


@api_bp.route('/services', methods=['GET'])
def list_services():
    items = Service.query.filter_by(is_active=True).all()
    return jsonify([
        {
            'id': s.id,
            'name': s.name,
            'name_ar': s.name_ar,
            'description': s.description,
            'price': s.price,
        }
        for s in items
    ])
from flask import Blueprint, render_template, request, jsonify, abort
from ..extensions import db
from ..models import Doctor, Specialty, Wilaya, Clinic, Service
from ..services.status_service import StatusService
from sqlalchemy import or_, and_
import re

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    """Homepage"""
    doctors = Doctor.query.filter_by(is_published=True, is_active=True).limit(8).all()
    specialties = Specialty.query.filter_by(is_active=True).all()
    wilayas = Wilaya.query.all()
    
    # Get stats
    doctor_count = Doctor.query.filter_by(is_published=True, is_active=True).count()
    clinic_count = Clinic.query.filter_by(is_active=True).count()
    specialty_count = Specialty.query.filter_by(is_active=True).count()
    wilaya_count = Wilaya.query.count()
    
    return render_template('public/index.html',
                         doctors=doctors,
                         specialties=specialties,
                         wilayas=wilayas,
                         doctor_count=doctor_count,
                         clinic_count=clinic_count,
                         specialty_count=specialty_count,
                         wilaya_count=wilaya_count)

@public_bp.route('/doctors')
def doctors():
    """List all doctors with filters"""
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    query = Doctor.query.filter_by(is_published=True, is_active=True)
    
    # Filters
    search = request.args.get('search', '')
    specialty = request.args.get('specialty', '')
    wilaya = request.args.get('wilaya', '')
    commune = request.args.get('commune', '')
    available_now = request.args.get('available_now', '')
    accepts_new = request.args.get('accepts_new', '')
    
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
    
    if specialty:
        query = query.join(Specialty).filter(Specialty.name.ilike(f'%{specialty}%') | Specialty.name_ar.ilike(f'%{specialty}%'))
    
    if wilaya:
        query = query.join(Wilaya, Doctor.wilaya_id == Wilaya.id).filter(Wilaya.name.ilike(f'%{wilaya}%') | Wilaya.name_ar.ilike(f'%{wilaya}%'))
    
    if commune:
        query = query.join(Commune, Doctor.commune_id == Commune.id).filter(Commune.name.ilike(f'%{commune}%') | Commune.name_ar.ilike(f'%{commune}%'))
    
    if accepts_new == '1':
        query = query.filter_by(accepts_new_patients=True)
    
    # Order by featured first, then by creation date
    query = query.order_by(Doctor.is_featured.desc(), Doctor.created_at.desc())
    
    # Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    doctors = pagination.items
    
    # Get filter data for sidebar
    specialties = Specialty.query.filter_by(is_active=True).all()
    wilayas = Wilaya.query.all()
    
    return render_template('public/doctors.html',
                         doctors=doctors,
                         pagination=pagination,
                         specialties=specialties,
                         wilayas=wilayas,
                         search=search,
                         selected_specialty=specialty,
                         selected_wilaya=wilaya)

@public_bp.route('/doctors/<slug>')
def doctor_detail(slug):
    """Doctor profile page"""
    doctor = Doctor.query.filter_by(slug=slug, is_published=True, is_active=True).first_or_404()
    
    # Get status
    status = StatusService.get_status(doctor)
    
    # Get services
    services = doctor.services.all()
    
    # Get working hours
    working_hours = doctor.working_hours.all()
    
    return render_template('public/doctor_detail.html',
                         doctor=doctor,
                         status=status,
                         services=services,
                         working_hours=working_hours)

@public_bp.route('/api/search-doctors')
def search_doctors():
    """API endpoint for doctor search"""
    q = request.args.get('q', '')
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
    """About page"""
    return render_template('public/about.html')
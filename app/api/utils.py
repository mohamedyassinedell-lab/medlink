from app.services.status_service import StatusService


def serialize_doctor(doctor, full=False):
    if not doctor:
        return None

    data = {
        'id': doctor.id,
        'slug': doctor.slug,
        'first_name': doctor.first_name,
        'last_name': doctor.last_name,
        'first_name_ar': doctor.first_name_ar,
        'last_name_ar': doctor.last_name_ar,
        'full_name': doctor.full_name,
        'full_name_ar': doctor.full_name_ar,
        'specialty': {
            'id': doctor.specialty_ref.id,
            'name': doctor.specialty_ref.name,
            'name_ar': doctor.specialty_ref.name_ar,
            'icon': doctor.specialty_ref.icon,
        } if doctor.specialty_ref else None,
        'wilaya': {
            'id': doctor.wilaya_ref.id,
            'name': doctor.wilaya_ref.name,
            'name_ar': doctor.wilaya_ref.name_ar,
            'code': doctor.wilaya_ref.code,
        } if doctor.wilaya_ref else None,
        'commune': {
            'id': doctor.commune_ref.id,
            'name': doctor.commune_ref.name,
            'name_ar': doctor.commune_ref.name_ar,
        } if doctor.commune_ref else None,
        'phone': doctor.phone,
        'phone_secondary': doctor.phone_secondary,
        'profile_image': doctor.profile_image,
        'is_verified': doctor.is_verified,
        'is_featured': doctor.is_featured,
        'accepts_new_patients': doctor.accepts_new_patients,
        'experience_years': doctor.experience_years,
        'sub_specialty': doctor.sub_specialty,
    }

    if full:
        try:
            status = StatusService.get_status(doctor)
        except Exception:
            status = {'status': 'UNKNOWN', 'label': 'ℹ️'}

        data.update({
            'email': doctor.email,
            'bio': doctor.bio,
            'bio_ar': doctor.bio_ar,
            'address': doctor.address,
            'address_ar': doctor.address_ar,
            'status': status,
            'clinic': {
                'id': doctor.clinic_ref.id,
                'name': doctor.clinic_ref.name,
                'name_ar': doctor.clinic_ref.name_ar,
                'phone': doctor.clinic_ref.phone,
                'address': doctor.clinic_ref.address_ar or doctor.clinic_ref.address,
                'latitude': doctor.clinic_ref.latitude,
                'longitude': doctor.clinic_ref.longitude,
            } if doctor.clinic_ref else None,
            'working_hours': [
                {
                    'day_of_week': wh.day_of_week,
                    'day_name': wh.day_name,
                    'start_time': wh.start_time,
                    'end_time': wh.end_time,
                    'is_closed': wh.is_closed,
                }
                for wh in doctor.working_hours.all()
            ],
            'holidays': [
                {
                    'start_date': h.start_date.isoformat(),
                    'end_date': h.end_date.isoformat(),
                    'note': h.note_ar or h.note,
                }
                for h in doctor.holidays.all()
            ],
        })

    return data


def serialize_wilaya(w):
    return {'id': w.id, 'code': w.code, 'name': w.name, 'name_ar': w.name_ar}


def serialize_commune(c):
    return {'id': c.id, 'name': c.name, 'name_ar': c.name_ar, 'wilaya_id': c.wilaya_id}


def serialize_specialty(s):
    return {
        'id': s.id,
        'name': s.name,
        'name_ar': s.name_ar,
        'icon': s.icon,
        'doctors_count': s.doctors.filter_by(is_published=True).count(),
    }
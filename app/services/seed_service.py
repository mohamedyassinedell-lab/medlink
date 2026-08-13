from ..extensions import db
from ..models import User, Doctor, Clinic, Specialty, Wilaya, Commune, Service, WorkingHour, Holiday, PlatformSetting
from datetime import datetime, timedelta
import re

def seed_database():
    if User.query.first():
        return
    
    admin = User(
        username='admin',
        email='admin@medlink.com',
        is_admin=True,
        is_active=True
    )
    admin.set_password('Admin123!')
    db.session.add(admin)
    db.session.commit()
    
    wilayas_data = [
        {'code': '01', 'name': 'Adrar', 'name_ar': 'أدرار'},
        {'code': '02', 'name': 'Chlef', 'name_ar': 'الشلف'},
        {'code': '03', 'name': 'Laghouat', 'name_ar': 'الأغواط'},
        {'code': '16', 'name': 'Algiers', 'name_ar': 'الجزائر العاصمة'},
        {'code': '31', 'name': 'Oran', 'name_ar': 'وهران'},
        {'code': '25', 'name': 'Constantine', 'name_ar': 'قسنطينة'},
        {'code': '19', 'name': 'Setif', 'name_ar': 'سطيف'},
        {'code': '05', 'name': 'Batna', 'name_ar': 'باتنة'},
        {'code': '09', 'name': 'Blida', 'name_ar': 'البليدة'},
        {'code': '17', 'name': 'Djelfa', 'name_ar': 'الجلفة'},
        {'code': '29', 'name': 'Mascara', 'name_ar': 'معسكر'},
        {'code': '46', 'name': 'Tlemcen', 'name_ar': 'تلمسان'},
        {'code': '20', 'name': 'Saida', 'name_ar': 'سعيدة'},
        {'code': '39', 'name': 'El Oued', 'name_ar': 'الوادي'},
        {'code': '40', 'name': 'Khenchela', 'name_ar': 'خنشلة'},
    ]
    
    wilayas = {}
    for data in wilayas_data:
        wilaya = Wilaya(
            code=data['code'],
            name=data['name'],
            name_ar=data['name_ar']
        )
        db.session.add(wilaya)
        wilayas[data['code']] = wilaya
    db.session.commit()
    
    communes_data = [
        {'name': 'Algiers Centre', 'name_ar': 'الجزائر الوسطى', 'wilaya_code': '16'},
        {'name': 'Ben Aknoun', 'name_ar': 'بن عكنون', 'wilaya_code': '16'},
        {'name': 'Bouzaréah', 'name_ar': 'بوزريعة', 'wilaya_code': '16'},
        {'name': 'El Biar', 'name_ar': 'الأبيار', 'wilaya_code': '16'},
        {'name': 'Hussein Dey', 'name_ar': 'حسين داي', 'wilaya_code': '16'},
        {'name': 'Laghouat', 'name_ar': 'الأغواط', 'wilaya_code': '03'},
        {'name': 'Ain Madhi', 'name_ar': 'عين ماضي', 'wilaya_code': '03'},
        {'name': 'Oran Centre', 'name_ar': 'وهران الوسطى', 'wilaya_code': '31'},
        {'name': 'Bir El Djir', 'name_ar': 'بئر الجير', 'wilaya_code': '31'},
        {'name': 'Constantine', 'name_ar': 'قسنطينة', 'wilaya_code': '25'},
        {'name': 'Setif', 'name_ar': 'سطيف', 'wilaya_code': '19'},
        {'name': 'Batna', 'name_ar': 'باتنة', 'wilaya_code': '05'},
        {'name': 'Blida', 'name_ar': 'البليدة', 'wilaya_code': '09'},
        {'name': 'Djelfa', 'name_ar': 'الجلفة', 'wilaya_code': '17'},
        {'name': 'Mascara', 'name_ar': 'معسكر', 'wilaya_code': '29'},
        {'name': 'Tlemcen', 'name_ar': 'تلمسان', 'wilaya_code': '46'},
        {'name': 'Saida', 'name_ar': 'سعيدة', 'wilaya_code': '20'},
        {'name': 'El Oued', 'name_ar': 'الوادي', 'wilaya_code': '39'},
        {'name': 'Khenchela', 'name_ar': 'خنشلة', 'wilaya_code': '40'},
    ]
    
    communes = {}
    for data in communes_data:
        wilaya = Wilaya.query.filter_by(code=data['wilaya_code']).first()
        if wilaya:
            commune = Commune(
                name=data['name'],
                name_ar=data['name_ar'],
                wilaya_id=wilaya.id
            )
            db.session.add(commune)
            communes[data['name']] = commune
    db.session.commit()
    
    specialties_data = [
        {'name': 'General Medicine', 'name_ar': 'الطب العام', 'icon': 'stethoscope'},
        {'name': 'Dentistry', 'name_ar': 'طب الأسنان', 'icon': 'tooth'},
        {'name': 'Cardiology', 'name_ar': 'أمراض القلب', 'icon': 'heart'},
        {'name': 'Pediatrics', 'name_ar': 'طب الأطفال', 'icon': 'child'},
        {'name': 'Ophthalmology', 'name_ar': 'طب العيون', 'icon': 'eye'},
        {'name': 'Dermatology', 'name_ar': 'الأمراض الجلدية', 'icon': 'skin'},
        {'name': 'Gynecology', 'name_ar': 'أمراض النساء', 'icon': 'female'},
        {'name': 'Surgery', 'name_ar': 'الجراحة', 'icon': 'scalpel'},
        {'name': 'Orthopedics', 'name_ar': 'جراحة العظام', 'icon': 'bone'},
        {'name': 'Neurology', 'name_ar': 'طب الأعصاب', 'icon': 'brain'},
        {'name': 'Psychiatry', 'name_ar': 'الطب النفسي', 'icon': 'brain'},
        {'name': 'Radiology', 'name_ar': 'الأشعة', 'icon': 'x-ray'},
        {'name': 'Internal Medicine', 'name_ar': 'الطب الباطني', 'icon': 'stethoscope'},
        {'name': 'Endocrinology', 'name_ar': 'الغدد الصماء', 'icon': 'gland'},
        {'name': 'Emergency Medicine', 'name_ar': 'طب الطوارئ', 'icon': 'ambulance'},
    ]
    
    specialties = {}
    for data in specialties_data:
        specialty = Specialty(
            name=data['name'],
            name_ar=data['name_ar'],
            icon=data['icon'],
            is_active=True
        )
        db.session.add(specialty)
        specialties[data['name']] = specialty
    db.session.commit()
    
    services_data = [
        {'name': 'Consultation', 'name_ar': 'استشارة', 'description': 'Medical consultation'},
        {'name': 'Examination', 'name_ar': 'فحص طبي', 'description': 'Medical examination'},
        {'name': 'Dental Cleaning', 'name_ar': 'تنظيف الأسنان', 'description': 'Professional teeth cleaning'},
        {'name': 'Eye Examination', 'name_ar': 'فحص النظر', 'description': 'Comprehensive eye exam'},
        {'name': 'Treatment', 'name_ar': 'علاج', 'description': 'Medical treatment'},
        {'name': 'Surgery', 'name_ar': 'جراحة', 'description': 'Surgical procedure'},
        {'name': 'X-Ray', 'name_ar': 'أشعة', 'description': 'X-ray imaging'},
        {'name': 'Ultrasound', 'name_ar': 'تصوير بالموجات فوق الصوتية', 'description': 'Ultrasound imaging'},
        {'name': 'Blood Test', 'name_ar': 'فحص الدم', 'description': 'Blood analysis'},
        {'name': 'ECG', 'name_ar': 'تخطيط القلب', 'description': 'Electrocardiogram'},
    ]
    
    services = {}
    for data in services_data:
        service = Service(
            name=data['name'],
            name_ar=data['name_ar'],
            description=data['description'],
            is_active=True
        )
        db.session.add(service)
        services[data['name']] = service
    db.session.commit()
    
    clinics_data = [
        {
            'name': 'Elite Medical Center',
            'name_ar': 'مركز النخبة الطبي',
            'address': '123 Algiers Main Street',
            'address_ar': '123 شارع الجزائر الرئيسي',
            'wilaya': '16',
            'commune': 'Algiers Centre',
            'phone': '0555-123456',
            'email': 'info@elitemedical.dz',
            'description': 'Premier medical center in Algiers',
            'description_ar': 'مركز طبي متميز في الجزائر'
        },
        {
            'name': 'Laghouat Medical Clinic',
            'name_ar': 'العيادة الطبية للأغواط',
            'address': '45 Laghouat City Center',
            'address_ar': '45 وسط مدينة الأغواط',
            'wilaya': '03',
            'commune': 'Laghouat',
            'phone': '0555-789012',
            'email': 'info@laghouatclinic.dz',
            'description': 'Quality healthcare in Laghouat',
            'description_ar': 'رعاية صحية متميزة في الأغواط'
        }
    ]
    
    clinics = {}
    for data in clinics_data:
        wilaya = Wilaya.query.filter_by(code=data['wilaya']).first()
        commune = Commune.query.filter_by(name=data['commune']).first()
        if wilaya and commune:
            clinic = Clinic(
                name=data['name'],
                name_ar=data['name_ar'],
                address=data['address'],
                address_ar=data['address_ar'],
                wilaya_id=wilaya.id,
                commune_id=commune.id,
                phone=data['phone'],
                email=data.get('email'),
                description=data.get('description'),
                description_ar=data.get('description_ar'),
                is_active=True
            )
            db.session.add(clinic)
            clinics[data['name']] = clinic
    db.session.commit()
    
    doctors_data = [
        {
            'first_name': 'Ahmed',
            'last_name': 'Mohamed',
            'first_name_ar': 'أحمد',
            'last_name_ar': 'محمد',
            'specialty': 'Cardiology',
            'sub_specialty': 'Interventional Cardiology',
            'experience_years': 15,
            'bio': 'Experienced cardiologist',
            'bio_ar': 'طبيب قلب متمرس',
            'wilaya': '16',
            'commune': 'Algiers Centre',
            'address': '123 Algiers Main Street',
            'phone': '0555-123456',
            'email': 'dr.ahmed@example.dz',
            'clinic': 'Elite Medical Center',
            'accepts_new_patients': True,
            'is_verified': True,
            'is_featured': True,
            'is_published': True
        }
    ]
    
    for data in doctors_data:
        specialty = Specialty.query.filter_by(name=data['specialty']).first()
        wilaya = Wilaya.query.filter_by(code=data['wilaya']).first()
        commune = Commune.query.filter_by(name=data['commune']).first()
        clinic = Clinic.query.filter_by(name=data['clinic']).first()
        
        if specialty and wilaya and commune and clinic:
            doctor = Doctor(
                first_name=data['first_name'],
                last_name=data['last_name'],
                first_name_ar=data.get('first_name_ar'),
                last_name_ar=data.get('last_name_ar'),
                specialty_id=specialty.id,
                sub_specialty=data.get('sub_specialty'),
                experience_years=data.get('experience_years'),
                bio=data.get('bio'),
                bio_ar=data.get('bio_ar'),
                wilaya_id=wilaya.id,
                commune_id=commune.id,
                address=data.get('address'),
                phone=data['phone'],
                email=data.get('email'),
                clinic_id=clinic.id,
                accepts_new_patients=data.get('accepts_new_patients', True),
                is_verified=data.get('is_verified', False),
                is_featured=data.get('is_featured', False),
                is_published=data.get('is_published', True),
                is_active=True
            )
            doctor.slug = doctor.generate_slug()
            db.session.add(doctor)
            db.session.commit()
            
            for day in range(7):
                wh = WorkingHour(
                    doctor_id=doctor.id,
                    day_of_week=day,
                    start_time='08:00',
                    end_time='16:00',
                    is_closed=False
                )
                db.session.add(wh)
            db.session.commit()
    
    platform_settings = [
        {'key': 'platform_name', 'value': 'TabibDZ', 'category': 'general'},
        {'key': 'platform_description', 'value': 'دليل الأطباء والعيادات في الجزائر', 'category': 'general'},
        {'key': 'platform_email', 'value': 'contact@tabibdz.com', 'category': 'contact'},
        {'key': 'platform_phone', 'value': '0555-555555', 'category': 'contact'},
        {'key': 'platform_address', 'value': 'الجزائر العاصمة، الجزائر', 'category': 'contact'},
    ]
    
    for setting_data in platform_settings:
        setting = PlatformSetting(
            key=setting_data['key'],
            value=setting_data['value'],
            category=setting_data['category']
        )
        db.session.add(setting)
    db.session.commit()
    
    print("Database seeded successfully!")
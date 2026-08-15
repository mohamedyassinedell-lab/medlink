from ..extensions import db
from ..models import User, Doctor, Clinic, Specialty, Wilaya, Commune, Service, WorkingHour, PlatformSetting


def seed_database():

    # =========================================================
    # 1. إنشاء حساب الإدارة
    # =========================================================

    if not User.query.first():
        admin = User(
            username='admin',
            email='admin@medlink.com',
            is_admin=True,
            is_active=True
        )

        admin.set_password('Admin123!')

        db.session.add(admin)
        db.session.commit()


    # =========================================================
    # 2. الولايات الجزائرية
    # =========================================================

    wilayas_data = [
        {'code': '01', 'name': 'Adrar', 'name_ar': 'أدرار'},
        {'code': '02', 'name': 'Chlef', 'name_ar': 'الشلف'},
        {'code': '03', 'name': 'Laghouat', 'name_ar': 'الأغواط'},
        {'code': '04', 'name': 'Oum El Bouaghi', 'name_ar': 'أم البواقي'},
        {'code': '05', 'name': 'Batna', 'name_ar': 'باتنة'},
        {'code': '06', 'name': 'Bejaia', 'name_ar': 'بجاية'},
        {'code': '07', 'name': 'Biskra', 'name_ar': 'بسكرة'},
        {'code': '08', 'name': 'Bechar', 'name_ar': 'بشار'},
        {'code': '09', 'name': 'Blida', 'name_ar': 'البليدة'},
        {'code': '10', 'name': 'Bouira', 'name_ar': 'البويرة'},
        {'code': '11', 'name': 'Tamanrasset', 'name_ar': 'تمنراست'},
        {'code': '12', 'name': 'Tebessa', 'name_ar': 'تبسة'},
        {'code': '13', 'name': 'Tlemcen', 'name_ar': 'تلمسان'},
        {'code': '14', 'name': 'Tiaret', 'name_ar': 'تيارت'},
        {'code': '15', 'name': 'Tizi Ouzou', 'name_ar': 'تيزي وزو'},
        {'code': '16', 'name': 'Algiers', 'name_ar': 'الجزائر'},
        {'code': '17', 'name': 'Djelfa', 'name_ar': 'الجلفة'},
        {'code': '18', 'name': 'Jijel', 'name_ar': 'جيجل'},
        {'code': '19', 'name': 'Setif', 'name_ar': 'سطيف'},
        {'code': '20', 'name': 'Saida', 'name_ar': 'سعيدة'},
        {'code': '21', 'name': 'Skikda', 'name_ar': 'سكيكدة'},
        {'code': '22', 'name': 'Sidi Bel Abbes', 'name_ar': 'سيدي بلعباس'},
        {'code': '23', 'name': 'Annaba', 'name_ar': 'عنابة'},
        {'code': '24', 'name': 'Guelma', 'name_ar': 'قالمة'},
        {'code': '25', 'name': 'Constantine', 'name_ar': 'قسنطينة'},
        {'code': '26', 'name': 'Medea', 'name_ar': 'المدية'},
        {'code': '27', 'name': 'Mostaganem', 'name_ar': 'مستغانم'},
        {'code': '28', 'name': "M'Sila", 'name_ar': 'المسيلة'},
        {'code': '29', 'name': 'Mascara', 'name_ar': 'معسكر'},
        {'code': '30', 'name': 'Ouargla', 'name_ar': 'ورقلة'},
        {'code': '31', 'name': 'Oran', 'name_ar': 'وهران'},
        {'code': '32', 'name': 'El Bayadh', 'name_ar': 'البيض'},
        {'code': '33', 'name': 'Illizi', 'name_ar': 'إليزي'},
        {'code': '34', 'name': 'Bordj Bou Arreridj', 'name_ar': 'برج بوعريريج'},
        {'code': '35', 'name': 'Boumerdes', 'name_ar': 'بومرداس'},
        {'code': '36', 'name': 'El Tarf', 'name_ar': 'الطارف'},
        {'code': '37', 'name': 'Tindouf', 'name_ar': 'تندوف'},
        {'code': '38', 'name': 'Tissemsilt', 'name_ar': 'تيسمسيلت'},
        {'code': '39', 'name': 'El Oued', 'name_ar': 'الوادي'},
        {'code': '40', 'name': 'Khenchela', 'name_ar': 'خنشلة'},
        {'code': '41', 'name': 'Souk Ahras', 'name_ar': 'سوق أهراس'},
        {'code': '42', 'name': 'Tipaza', 'name_ar': 'تيبازة'},
        {'code': '43', 'name': 'Mila', 'name_ar': 'ميلة'},
        {'code': '44', 'name': 'Ain Defla', 'name_ar': 'عين الدفلى'},
        {'code': '45', 'name': 'Naama', 'name_ar': 'النعامة'},
        {'code': '46', 'name': 'Ain Temouchent', 'name_ar': 'عين تموشنت'},
        {'code': '47', 'name': 'Ghardaia', 'name_ar': 'غرداية'},
        {'code': '48', 'name': 'Relizane', 'name_ar': 'غليزان'},
        {'code': '49', 'name': 'Timimoun', 'name_ar': 'تيميمون'},
        {'code': '50', 'name': 'Bordj Badji Mokhtar', 'name_ar': 'برج باجي مختار'},
        {'code': '51', 'name': 'Ouled Djellal', 'name_ar': 'أولاد جلال'},
        {'code': '52', 'name': 'Beni Abbes', 'name_ar': 'بني عباس'},
        {'code': '53', 'name': 'In Salah', 'name_ar': 'عين صالح'},
        {'code': '54', 'name': 'In Guezzam', 'name_ar': 'عين قزام'},
        {'code': '55', 'name': 'Touggourt', 'name_ar': 'تقرت'},
        {'code': '56', 'name': 'Djanet', 'name_ar': 'جانت'},
        {'code': '57', 'name': 'El Meghaier', 'name_ar': 'المغير'},
        {'code': '58', 'name': 'El Meniaa', 'name_ar': 'المنيعة'},
    ]


    # إضافة الولايات إذا لم تكن موجودة
    for data in wilayas_data:

        wilaya = Wilaya.query.filter_by(
            code=data['code']
        ).first()

        if not wilaya:
            wilaya = Wilaya(
                code=data['code'],
                name=data['name'],
                name_ar=data['name_ar']
            )

            db.session.add(wilaya)


    db.session.commit()


    # =========================================================
    # 3. التخصصات الطبية
    # =========================================================

    specialties_data = [
        {
            'name': 'General Medicine',
            'name_ar': 'الطب العام',
            'icon': 'stethoscope'
        },
        {
            'name': 'Dentistry',
            'name_ar': 'طب الأسنان',
            'icon': 'tooth'
        },
        {
            'name': 'Cardiology',
            'name_ar': 'أمراض القلب',
            'icon': 'heart'
        },
        {
            'name': 'Pediatrics',
            'name_ar': 'طب الأطفال',
            'icon': 'child'
        },
        {
            'name': 'Ophthalmology',
            'name_ar': 'طب العيون',
            'icon': 'eye'
        },
        {
            'name': 'Dermatology',
            'name_ar': 'الأمراض الجلدية',
            'icon': 'skin'
        },
        {
            'name': 'Gynecology',
            'name_ar': 'أمراض النساء',
            'icon': 'female'
        },
        {
            'name': 'Surgery',
            'name_ar': 'الجراحة',
            'icon': 'scalpel'
        },
        {
            'name': 'Orthopedics',
            'name_ar': 'جراحة العظام',
            'icon': 'bone'
        },
        {
            'name': 'Neurology',
            'name_ar': 'طب الأعصاب',
            'icon': 'brain'
        },
        {
            'name': 'Psychiatry',
            'name_ar': 'الطب النفسي',
            'icon': 'brain'
        },
        {
            'name': 'Radiology',
            'name_ar': 'الأشعة',
            'icon': 'x-ray'
        },
        {
            'name': 'Internal Medicine',
            'name_ar': 'الطب الباطني',
            'icon': 'stethoscope'
        },
        {
            'name': 'Endocrinology',
            'name_ar': 'الغدد الصماء',
            'icon': 'gland'
        },
        {
            'name': 'Emergency Medicine',
            'name_ar': 'طب الطوارئ',
            'icon': 'ambulance'
        },
    ]


    for data in specialties_data:

        specialty = Specialty.query.filter_by(
            name=data['name']
        ).first()

        if not specialty:

            specialty = Specialty(
                name=data['name'],
                name_ar=data['name_ar'],
                icon=data['icon'],
                is_active=True
            )

            db.session.add(specialty)


    db.session.commit()


    # =========================================================
    # 4. العيادات والأطباء التجريبيون
    # =========================================================

    doctors_data = [
        {
            'first_name': 'Amina',
            'last_name': 'Ben Ali',
            'first_name_ar': 'أمينة',
            'last_name_ar': 'بن علي',
            'specialty': 'Cardiology',
            'wilaya': '16',
            'commune': 'Rouiba',
            'commune_ar': 'الرويبة',
            'clinic': 'Clinique Chifa Spécialisée',
            'clinic_ar': 'عيادة الشفاء التخصصية',
            'phone': '0555123456'
        },
        {
            'first_name': 'Yassine',
            'last_name': 'Merah',
            'first_name_ar': 'ياسين',
            'last_name_ar': 'مراح',
            'specialty': 'Pediatrics',
            'wilaya': '31',
            'commune': 'Es Senia',
            'commune_ar': 'السانيا',
            'clinic': 'Centre Médical Oran',
            'clinic_ar': 'المركز الطبي وهران',
            'phone': '0770987654'
        },
        {
            'first_name': 'Sara',
            'last_name': 'Touati',
            'first_name_ar': 'سارة',
            'last_name_ar': 'تواتي',
            'specialty': 'Dermatology',
            'wilaya': '25',
            'commune': 'El Khroub',
            'commune_ar': 'الخروب',
            'clinic': 'Clinique Ennour de Dermatologie',
            'clinic_ar': 'عيادة النور للأمراض الجلدية',
            'phone': '0661234567'
        },
        {
            'first_name': 'Mohamed',
            'last_name': 'Reda',
            'first_name_ar': 'محمد',
            'last_name_ar': 'رضا',
            'specialty': 'Orthopedics',
            'wilaya': '19',
            'commune': 'El Eulma',
            'commune_ar': 'العلمة',
            'clinic': 'Clinique Les Hauts Plateaux',
            'clinic_ar': 'عيادة الهضاب الطبية',
            'phone': '0550112233'
        },
        {
            'first_name': 'Leila',
            'last_name': 'Mansouri',
            'first_name_ar': 'ليلى',
            'last_name_ar': 'منصوري',
            'specialty': 'Gynecology',
            'wilaya': '23',
            'commune': 'El Bouni',
            'commune_ar': 'البوني',
            'clinic': 'Clinique El Yasmine Maternité',
            'clinic_ar': 'عيادة الياسمين للأمومة',
            'phone': '0772445566'
        },
        {
            'first_name': 'Karim',
            'last_name': 'Bouzid',
            'first_name_ar': 'كريم',
            'last_name_ar': 'بوزيد',
            'specialty': 'Ophthalmology',
            'wilaya': '15',
            'commune': 'Azazga',
            'commune_ar': 'عزازقة',
            'clinic': 'Centre Vision Médical',
            'clinic_ar': 'مركز الرؤية الطبي',
            'phone': '0663778899'
        }
    ]

    # إضافة البلديات المطلوبة إذا لم تكن موجودة
    for data in doctors_data:
        wilaya = Wilaya.query.filter_by(code=data['wilaya']).first()

        if wilaya:
            commune = Commune.query.filter_by(
                name=data['commune'],
                wilaya_id=wilaya.id
            ).first()

            if not commune:
                commune = Commune(
                    name=data['commune'],
                    name_ar=data['commune_ar'],
                    wilaya_id=wilaya.id
                )
                db.session.add(commune)

    db.session.commit()

    # إضافة العيادات المطلوبة إذا لم تكن موجودة
    for data in doctors_data:
        wilaya = Wilaya.query.filter_by(code=data['wilaya']).first()
        commune = Commune.query.filter_by(
            name=data['commune'],
            wilaya_id=wilaya.id
        ).first() if wilaya else None

        if wilaya and commune:
            clinic = Clinic.query.filter_by(name=data['clinic']).first()

            if not clinic:
                clinic = Clinic(
                    name=data['clinic'],
                    name_ar=data['clinic_ar'],
                    address=data['commune'],
                    address_ar=data['commune_ar'],
                    wilaya_id=wilaya.id,
                    commune_id=commune.id,
                    phone=data['phone'],
                    is_active=True
                )
                db.session.add(clinic)

    db.session.commit()

    # إضافة الأطباء
    for data in doctors_data:
        specialty = Specialty.query.filter_by(name=data['specialty']).first()
        wilaya = Wilaya.query.filter_by(code=data['wilaya']).first()
        commune = Commune.query.filter_by(
            name=data['commune'],
            wilaya_id=wilaya.id
        ).first() if wilaya else None
        clinic = Clinic.query.filter_by(name=data['clinic']).first()

        # منع التكرار إذا كان الطبيب موجوداً مسبقاً
        existing_doctor = Doctor.query.filter_by(
            first_name=data['first_name'],
            last_name=data['last_name']
        ).first()

        if specialty and wilaya and commune and clinic and not existing_doctor:
            doctor = Doctor(
                first_name=data['first_name'],
                last_name=data['last_name'],
                first_name_ar=data['first_name_ar'],
                last_name_ar=data['last_name_ar'],
                specialty_id=specialty.id,
                wilaya_id=wilaya.id,
                commune_id=commune.id,
                phone=data['phone'],
                clinic_id=clinic.id,
                accepts_new_patients=True,
                is_verified=True,
                is_featured=False,
                is_published=True,
                is_active=True
            )

            doctor.slug = doctor.generate_slug()
            db.session.add(doctor)
            db.session.commit()

            # أوقات العمل: 08:00 - 16:00 طوال أيام الأسبوع
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

    # =========================================================
    # 5. الخدمات الطبية
    # =========================================================

    services_data = [
        {
            'name': 'Consultation',
            'name_ar': 'استشارة',
            'description': 'Medical consultation'
        },
        {
            'name': 'Examination',
            'name_ar': 'فحص طبي',
            'description': 'Medical examination'
        },
        {
            'name': 'Dental Cleaning',
            'name_ar': 'تنظيف الأسنان',
            'description': 'Professional teeth cleaning'
        },
        {
            'name': 'Eye Examination',
            'name_ar': 'فحص النظر',
            'description': 'Comprehensive eye exam'
        },
        {
            'name': 'Treatment',
            'name_ar': 'علاج',
            'description': 'Medical treatment'
        },
        {
            'name': 'Surgery',
            'name_ar': 'جراحة',
            'description': 'Surgical procedure'
        },
        {
            'name': 'X-Ray',
            'name_ar': 'أشعة',
            'description': 'X-ray imaging'
        },
        {
            'name': 'Ultrasound',
            'name_ar': 'تصوير بالموجات فوق الصوتية',
            'description': 'Ultrasound imaging'
        },
        {
            'name': 'Blood Test',
            'name_ar': 'فحص الدم',
            'description': 'Blood analysis'
        },
        {
            'name': 'ECG',
            'name_ar': 'تخطيط القلب',
            'description': 'Electrocardiogram'
        },
    ]


    for data in services_data:

        service = Service.query.filter_by(
            name=data['name']
        ).first()

        if not service:

            service = Service(
                name=data['name'],
                name_ar=data['name_ar'],
                description=data['description'],
                is_active=True
            )

            db.session.add(service)


    db.session.commit()


    # =========================================================
    # 6. إعدادات المنصة
    # =========================================================

    platform_settings = [
        {
            'key': 'platform_name',
            'value': 'MedLink',
            'category': 'general'
        },
        {
            'key': 'platform_description',
            'value': 'دليل الأطباء والعيادات في الجزائر',
            'category': 'general'
        },
        {
            'key': 'platform_email',
            'value': 'contact@medlink.dz',
            'category': 'contact'
        },
        {
            'key': 'platform_phone',
            'value': '0698766662',
            'category': 'contact'
        },
        {
            'key': 'platform_address',
            'value': 'الجزائر العاصمة، الجزائر',
            'category': 'contact'
        },
    ]


    for setting_data in platform_settings:

        setting = PlatformSetting.query.filter_by(
            key=setting_data['key']
        ).first()

        if not setting:

            setting = PlatformSetting(
                key=setting_data['key'],
                value=setting_data['value'],
                category=setting_data['category']
            )

            db.session.add(setting)


    db.session.commit()


    print("Database seeded successfully!")
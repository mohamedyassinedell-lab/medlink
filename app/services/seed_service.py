from ..extensions import db
from ..models import (
    User,
    Doctor,
    Clinic,
    Specialty,
    Wilaya,
    Commune,
    Service,
    WorkingHour,
    PlatformSetting
)


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
    # 4. الأطباء الحقيقيون الموثقون من مصادر علنية
    # =========================================================

    DOCTORS_DATA = [

        # =====================================================
        # CARDIOLOGY - ALGER
        # =====================================================

        {
            'first_name': 'Nadia',
            'last_name': 'Mouhouche',
            'first_name_ar': 'نادية',
            'last_name_ar': 'محوش',
            'specialty': 'Cardiology',
            'wilaya': '16',
            'commune': 'Rouiba',
            'commune_ar': 'الرويبة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '023854896'
        },

        {
            'first_name': 'Younes',
            'last_name': 'Moualek',
            'first_name_ar': 'يونس',
            'last_name_ar': 'مولك',
            'specialty': 'Cardiology',
            'wilaya': '16',
            'commune': 'Rouiba',
            'commune_ar': 'الرويبة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '023860014'
        },

        {
            'first_name': 'Soulef',
            'last_name': 'Moudjebeur',
            'first_name_ar': 'سولاف',
            'last_name_ar': 'موجبر',
            'specialty': 'Cardiology',
            'wilaya': '16',
            'commune': 'Rouiba',
            'commune_ar': 'الرويبة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0560904368'
        },

        {
            'first_name': 'Bennamane',
            'last_name': '',
            'first_name_ar': 'بن نمان',
            'last_name_ar': '',
            'specialty': 'Cardiology',
            'wilaya': '16',
            'commune': 'Rouiba',
            'commune_ar': 'الرويبة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '023715619'
        },

        {
            'first_name': 'Hamrouni',
            'last_name': '',
            'first_name_ar': 'حمروني',
            'last_name_ar': '',
            'specialty': 'Cardiology',
            'wilaya': '16',
            'commune': 'Sidi Moussa',
            'commune_ar': 'سيدي موسى',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0779441064'
        },

        {
            'first_name': 'Nabil',
            'last_name': 'Nemmar',
            'first_name_ar': 'نبيل',
            'last_name_ar': 'نعمار',
            'specialty': 'Cardiology',
            'wilaya': '09',
            'commune': 'Ouled Yaich',
            'commune_ar': 'أولاد يعيش',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0541108218'
        },

        {
            'first_name': 'Khaled',
            'last_name': 'Bouasria',
            'first_name_ar': 'خالد',
            'last_name_ar': 'بوعصرية',
            'specialty': 'Cardiology',
            'wilaya': '16',
            'commune': 'Bab Ezzouar',
            'commune_ar': 'باب الزوار',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0656247620'
        },

        {
            'first_name': 'Mohamed',
            'last_name': 'Bakhti',
            'first_name_ar': 'محمد',
            'last_name_ar': 'باختي',
            'specialty': 'Cardiology',
            'wilaya': '28',
            'commune': "M'Sila",
            'commune_ar': 'المسيلة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0654832724'
        },

        {
            'first_name': 'Mounir',
            'last_name': 'Bouame',
            'first_name_ar': 'منير',
            'last_name_ar': 'بوعم',
            'specialty': 'Cardiology',
            'wilaya': '09',
            'commune': 'Blida',
            'commune_ar': 'البليدة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0556895609'
        },

        # =====================================================
        # PEDIATRICS
        # =====================================================

        {
            'first_name': 'Medjdoub',
            'last_name': 'Gheffari',
            'first_name_ar': 'مجذوب',
            'last_name_ar': 'غفاري',
            'specialty': 'Pediatrics',
            'wilaya': '45',
            'commune': 'Mecheria',
            'commune_ar': 'المشرية',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0661260093'
        },

        {
            'first_name': 'Mustapha',
            'last_name': 'Ogbi',
            'first_name_ar': 'مصطفى',
            'last_name_ar': 'أوقبي',
            'specialty': 'Pediatrics',
            'wilaya': '16',
            'commune': 'Ain Benian',
            'commune_ar': 'عين بنيان',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0542936089'
        },

        {
            'first_name': 'Abderraouf',
            'last_name': 'Belayel',
            'first_name_ar': 'عبد الرؤوف',
            'last_name_ar': 'بلايل',
            'specialty': 'Pediatrics',
            'wilaya': '16',
            'commune': 'Bir Mourad Rais',
            'commune_ar': 'بئر مراد رايس',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0542131958'
        },

        {
            'first_name': 'Walid',
            'last_name': 'Noui',
            'first_name_ar': 'وليد',
            'last_name_ar': 'نوي',
            'specialty': 'Pediatrics',
            'wilaya': '16',
            'commune': 'Reghaia',
            'commune_ar': 'الرويبة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0676114202'
        },

        {
            'first_name': 'Larbi',
            'last_name': 'Mariche',
            'first_name_ar': 'العربي',
            'last_name_ar': 'مريش',
            'specialty': 'Pediatrics',
            'wilaya': '16',
            'commune': 'Baraki',
            'commune_ar': 'براقي',
            'clinic': None,
            'clinic_ar': None,
            'phone': '023911488'
        },

        {
            'first_name': 'Wassila',
            'last_name': 'Afroune',
            'first_name_ar': 'وسيلة',
            'last_name_ar': 'عفرون',
            'specialty': 'Pediatrics',
            'wilaya': '16',
            'commune': 'Birkhadem',
            'commune_ar': 'بئر خادم',
            'clinic': None,
            'clinic_ar': None,
            'phone': '023453393'
        },

        {
            'first_name': 'Imane',
            'last_name': 'Mokrani',
            'first_name_ar': 'إيمان',
            'last_name_ar': 'مقراني',
            'specialty': 'Pediatrics',
            'wilaya': '35',
            'commune': 'Ouled Moussa',
            'commune_ar': 'أولاد موسى',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0556188209'
        },

        {
            'first_name': 'Mourad',
            'last_name': 'Yahiaoui',
            'first_name_ar': 'مراد',
            'last_name_ar': 'يحياوي',
            'specialty': 'Pediatrics',
            'wilaya': '17',
            'commune': 'Djelfa',
            'commune_ar': 'الجلفة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0542713104'
        },

        {
            'first_name': 'Mohamed',
            'last_name': 'Mizat',
            'first_name_ar': 'محمد',
            'last_name_ar': 'ميزا',
            'specialty': 'Pediatrics',
            'wilaya': '17',
            'commune': 'Djelfa',
            'commune_ar': 'الجلفة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0657578000'
        },

        {
            'first_name': 'Beldjerd',
            'last_name': '',
            'first_name_ar': 'بلجرد',
            'last_name_ar': '',
            'specialty': 'Pediatrics',
            'wilaya': '48',
            'commune': 'Relizane',
            'commune_ar': 'غليزان',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0664848011'
        },

        # =====================================================
        # OPHTHALMOLOGY
        # =====================================================

        {
            'first_name': 'Hakim',
            'last_name': 'Benchaouch',
            'first_name_ar': 'حكيم',
            'last_name_ar': 'بن شعوش',
            'specialty': 'Ophthalmology',
            'wilaya': '06',
            'commune': 'Oued Ghir',
            'commune_ar': 'وادي غير',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0781584508'
        },

        {
            'first_name': 'Said',
            'last_name': 'Belguerche',
            'first_name_ar': 'سعيد',
            'last_name_ar': 'بلقارش',
            'specialty': 'Ophthalmology',
            'wilaya': '16',
            'commune': 'Bab El Oued',
            'commune_ar': 'باب الوادي',
            'clinic': None,
            'clinic_ar': None,
            'phone': '023170081'
        },

        {
            'first_name': 'Mhamed',
            'last_name': 'Zouadi',
            'first_name_ar': 'محمد',
            'last_name_ar': 'زوادي',
            'specialty': 'Ophthalmology',
            'wilaya': '44',
            'commune': 'Khemis Miliana',
            'commune_ar': 'خميس مليانة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '027661254'
        },

        {
            'first_name': 'Sonia',
            'last_name': 'Mehdid',
            'first_name_ar': 'سونيا',
            'last_name_ar': 'محديد',
            'specialty': 'Ophthalmology',
            'wilaya': '18',
            'commune': 'Jijel',
            'commune_ar': 'جيجل',
            'clinic': None,
            'clinic_ar': None,
            'phone': '034473304'
        },

        {
            'first_name': 'Khaled',
            'last_name': 'Megaiz',
            'first_name_ar': 'خالد',
            'last_name_ar': 'مقيز',
            'specialty': 'Ophthalmology',
            'wilaya': '48',
            'commune': 'Relizane',
            'commune_ar': 'غليزان',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0775410067'
        },

        {
            'first_name': 'Kasdi',
            'last_name': '',
            'first_name_ar': 'قاسدي',
            'last_name_ar': '',
            'specialty': 'Ophthalmology',
            'wilaya': '14',
            'commune': 'Tiaret',
            'commune_ar': 'تيارت',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0779510664'
        },

        {
            'first_name': 'Yacine',
            'last_name': 'Amrane',
            'first_name_ar': 'ياسين',
            'last_name_ar': 'عمران',
            'specialty': 'Ophthalmology',
            'wilaya': '15',
            'commune': 'Freha',
            'commune_ar': 'فريحة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '026456766'
        },

        {
            'first_name': 'Hamida',
            'last_name': 'Taharount',
            'first_name_ar': 'حميدة',
            'last_name_ar': 'طاهرونت',
            'specialty': 'Ophthalmology',
            'wilaya': '15',
            'commune': 'Tizi Gheniff',
            'commune_ar': 'تيزي غنيف',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0675334509'
        },

        {
            'first_name': 'Nina',
            'last_name': 'Aboubakra',
            'first_name_ar': 'نينا',
            'last_name_ar': 'أبوبكرى',
            'specialty': 'Ophthalmology',
            'wilaya': '16',
            'commune': 'Reghaia',
            'commune_ar': 'الرويبة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0661766073'
        },

        {
            'first_name': 'Mourad',
            'last_name': 'Ladgham',
            'first_name_ar': 'مراد',
            'last_name_ar': 'لذغام',
            'specialty': 'Ophthalmology',
            'wilaya': '28',
            'commune': 'Bou Saada',
            'commune_ar': 'بوسعادة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '035433454'
        },

        {
            'first_name': 'Iles',
            'last_name': '',
            'first_name_ar': 'إليس',
            'last_name_ar': '',
            'specialty': 'Ophthalmology',
            'wilaya': '46',
            'commune': 'Ain Temouchent',
            'commune_ar': 'عين تموشنت',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0561552773'
        },

        {
            'first_name': 'Garidi',
            'last_name': '',
            'first_name_ar': 'قريدي',
            'last_name_ar': '',
            'specialty': 'Ophthalmology',
            'wilaya': '16',
            'commune': 'Bab El Oued',
            'commune_ar': 'باب الوادي',
            'clinic': None,
            'clinic_ar': None,
            'phone': '023152754'
        },

        {
            'first_name': 'Soufi',
            'last_name': '',
            'first_name_ar': 'صوفي',
            'last_name_ar': '',
            'specialty': 'Ophthalmology',
            'wilaya': '16',
            'commune': 'El Hammamet',
            'commune_ar': 'الحمامات',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0771118389'
        },

        # =====================================================
        # DERMATOLOGY
        # =====================================================

        {
            'first_name': 'Mars',
            'last_name': '',
            'first_name_ar': 'مارس',
            'last_name_ar': '',
            'specialty': 'Dermatology',
            'wilaya': '16',
            'commune': 'Draria',
            'commune_ar': 'الدرارية',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0558415395'
        },

        {
            'first_name': 'Nassima',
            'last_name': 'Ammar',
            'first_name_ar': 'نسيمة',
            'last_name_ar': 'عمار',
            'specialty': 'Dermatology',
            'wilaya': '31',
            'commune': 'Sidi Chami',
            'commune_ar': 'سيدي الشحمي',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0794473129'
        },

        {
            'first_name': 'Okba',
            'last_name': 'Bouzaher',
            'first_name_ar': 'عقبة',
            'last_name_ar': 'بوزاهر',
            'specialty': 'Dermatology',
            'wilaya': '35',
            'commune': 'Boumerdes',
            'commune_ar': 'بومرداس',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0799199094'
        },

        {
            'first_name': 'Touati',
            'last_name': 'A',
            'first_name_ar': 'تواتي',
            'last_name_ar': 'أ',
            'specialty': 'Dermatology',
            'wilaya': '03',
            'commune': 'Laghouat',
            'commune_ar': 'الأغواط',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0658213436'
        },

        {
            'first_name': 'Lachkhem',
            'last_name': '',
            'first_name_ar': 'لشخم',
            'last_name_ar': '',
            'specialty': 'Dermatology',
            'wilaya': '03',
            'commune': 'Laghouat',
            'commune_ar': 'الأغواط',
            'clinic': None,
            'clinic_ar': None,
            'phone': '029926590'
        },

        {
            'first_name': 'Youcef',
            'last_name': 'Lebel',
            'first_name_ar': 'يوسف',
            'last_name_ar': 'لبال',
            'specialty': 'Dermatology',
            'wilaya': '26',
            'commune': 'Medea',
            'commune_ar': 'المدية',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0676025854'
        },

        {
            'first_name': 'Hafida',
            'last_name': 'Nechem',
            'first_name_ar': 'حفيظة',
            'last_name_ar': 'نشام',
            'specialty': 'Dermatology',
            'wilaya': '09',
            'commune': 'Blida',
            'commune_ar': 'البليدة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0779818521'
        },

        {
            'first_name': 'Amina',
            'last_name': 'Touati',
            'first_name_ar': 'أمينة',
            'last_name_ar': 'تواتي',
            'specialty': 'Dermatology',
            'wilaya': '09',
            'commune': 'Blida',
            'commune_ar': 'البليدة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0675106970'
        },

        {
            'first_name': 'Dalila',
            'last_name': 'Alouache',
            'first_name_ar': 'دليلة',
            'last_name_ar': 'علواش',
            'specialty': 'Dermatology',
            'wilaya': '35',
            'commune': 'Boudouaou',
            'commune_ar': 'بودواو',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0550102935'
        },

        {
            'first_name': 'Sairi',
            'last_name': '',
            'first_name_ar': 'سايري',
            'last_name_ar': '',
            'specialty': 'Dermatology',
            'wilaya': '15',
            'commune': 'Azazga',
            'commune_ar': 'عزازقة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0657483536'
        },

        {
            'first_name': 'Akli',
            'last_name': '',
            'first_name_ar': 'أقلي',
            'last_name_ar': '',
            'specialty': 'Dermatology',
            'wilaya': '15',
            'commune': 'Tizi Ouzou',
            'commune_ar': 'تيزي وزو',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0794822012'
        },

        {
            'first_name': 'Talaa',
            'last_name': '',
            'first_name_ar': 'طلعة',
            'last_name_ar': '',
            'specialty': 'Dermatology',
            'wilaya': '16',
            'commune': 'Djasr Kasentina',
            'commune_ar': 'جسر قسنطينة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0791060001'
        },

        {
            'first_name': 'Djellali',
            'last_name': '',
            'first_name_ar': 'جلالي',
            'last_name_ar': '',
            'specialty': 'Dermatology',
            'wilaya': '16',
            'commune': 'Zeralda',
            'commune_ar': 'زرالدة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0554230536'
        },

        {
            'first_name': 'Rouabah',
            'last_name': '',
            'first_name_ar': 'روابح',
            'last_name_ar': '',
            'specialty': 'Dermatology',
            'wilaya': '16',
            'commune': 'Bordj El Bahri',
            'commune_ar': 'برج البحري',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0771989962'
        },

        {
            'first_name': 'Mostefai',
            'last_name': 'R',
            'first_name_ar': 'مصطفاي',
            'last_name_ar': 'ر',
            'specialty': 'Dermatology',
            'wilaya': '16',
            'commune': 'Draria',
            'commune_ar': 'الدرارية',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0551401804'
        },

        {
            'first_name': 'Messafer',
            'last_name': '',
            'first_name_ar': 'مسافر',
            'last_name_ar': '',
            'specialty': 'Dermatology',
            'wilaya': '16',
            'commune': 'Dely Ibrahim',
            'commune_ar': 'دالي إبراهيم',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0556883019'
        },

        {
            'first_name': 'Guerroumi',
            'last_name': '',
            'first_name_ar': 'قرومي',
            'last_name_ar': '',
            'specialty': 'Dermatology',
            'wilaya': '16',
            'commune': 'Hussein Dey',
            'commune_ar': 'حسين داي',
            'clinic': None,
            'clinic_ar': None,
            'phone': None
        },

        # =====================================================
        # PSYCHIATRY
        # =====================================================

        {
            'first_name': 'Riyad',
            'last_name': 'Kadri',
            'first_name_ar': 'رياض',
            'last_name_ar': 'قدري',
            'specialty': 'Psychiatry',
            'wilaya': '13',
            'commune': 'Maghnia',
            'commune_ar': 'مغنية',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0550117055'
        },

        {
            'first_name': 'Amina',
            'last_name': 'Bouzid',
            'first_name_ar': 'أمينة',
            'last_name_ar': 'بوزيد',
            'specialty': 'Psychiatry',
            'wilaya': '16',
            'commune': 'Les Eucalyptus',
            'commune_ar': 'الكاليتوس',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0797843703'
        },

        {
            'first_name': 'Fatiha',
            'last_name': 'Belhadj',
            'first_name_ar': 'فتيحة',
            'last_name_ar': 'بلحاج',
            'specialty': 'Psychiatry',
            'wilaya': '31',
            'commune': 'Es Senia',
            'commune_ar': 'السانية',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0793926887'
        },

        {
            'first_name': 'Abderrahim',
            'last_name': 'Mahieddine',
            'first_name_ar': 'عبد الرحيم',
            'last_name_ar': 'محي الدين',
            'specialty': 'Psychiatry',
            'wilaya': '46',
            'commune': 'Ain Temouchent',
            'commune_ar': 'عين تموشنت',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0771158759'
        },

        {
            'first_name': 'Belkacem',
            'last_name': 'Medjahdi',
            'first_name_ar': 'بلقاسم',
            'last_name_ar': 'مدجاهدي',
            'specialty': 'Psychiatry',
            'wilaya': '09',
            'commune': 'Blida',
            'commune_ar': 'البليدة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '025200360'
        },

        {
            'first_name': 'Salim',
            'last_name': 'Selmi',
            'first_name_ar': 'سليم',
            'last_name_ar': 'سالمي',
            'specialty': 'Psychiatry',
            'wilaya': '16',
            'commune': 'Bachdjerrah',
            'commune_ar': 'باش جراح',
            'clinic': None,
            'clinic_ar': None,
            'phone': None
        },

        {
            'first_name': 'Boumediene',
            'last_name': 'Boudaoud',
            'first_name_ar': 'بومدين',
            'last_name_ar': 'بوداود',
            'specialty': 'Psychiatry',
            'wilaya': '06',
            'commune': 'Bejaia',
            'commune_ar': 'بجاية',
            'clinic': None,
            'clinic_ar': None,
            'phone': '034227118'
        },

        {
            'first_name': 'Hocine',
            'last_name': 'Irmouli',
            'first_name_ar': 'حسين',
            'last_name_ar': 'إيرمولي',
            'specialty': 'Psychiatry',
            'wilaya': '15',
            'commune': 'Azazga',
            'commune_ar': 'عزازقة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0790663250'
        },

        {
            'first_name': 'Boureni',
            'last_name': '',
            'first_name_ar': 'بوريني',
            'last_name_ar': '',
            'specialty': 'Psychiatry',
            'wilaya': '15',
            'commune': 'Tizi Ouzou',
            'commune_ar': 'تيزي وزو',
            'clinic': None,
            'clinic_ar': None,
            'phone': '026119800'
        },

        {
            'first_name': 'Toufik',
            'last_name': 'Azzoug',
            'first_name_ar': 'توفيق',
            'last_name_ar': 'عزوق',
            'specialty': 'Psychiatry',
            'wilaya': '06',
            'commune': 'El Kseur',
            'commune_ar': 'القصر',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0782914507'
        },

        {
            'first_name': 'Youcef',
            'last_name': 'Hebboul',
            'first_name_ar': 'يوسف',
            'last_name_ar': 'هبول',
            'specialty': 'Psychiatry',
            'wilaya': '05',
            'commune': 'Barika',
            'commune_ar': 'بريكة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0672831184'
        },

        {
            'first_name': 'Fazia',
            'last_name': 'Bourouf Hameche',
            'first_name_ar': 'فازية',
            'last_name_ar': 'بوروڨ حماش',
            'specialty': 'Psychiatry',
            'wilaya': '06',
            'commune': 'El Kseur',
            'commune_ar': 'القصر',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0559841809'
        },

        {
            'first_name': 'Abderrahim',
            'last_name': 'Addou Khiereddine',
            'first_name_ar': 'عبد الرحيم',
            'last_name_ar': 'عدو خير الدين',
            'specialty': 'Psychiatry',
            'wilaya': '13',
            'commune': 'Tlemcen',
            'commune_ar': 'تلمسان',
            'clinic': None,
            'clinic_ar': None,
            'phone': '043277382'
        },

        {
            'first_name': 'Semaoune',
            'last_name': '',
            'first_name_ar': 'سماعون',
            'last_name_ar': '',
            'specialty': 'Psychiatry',
            'wilaya': '16',
            'commune': 'Kouba',
            'commune_ar': 'القبة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0552155647'
        },

        # =====================================================
        # ORTHOPEDICS
        # =====================================================

        {
            'first_name': 'Lyes',
            'last_name': 'Boutra',
            'first_name_ar': 'إلياس',
            'last_name_ar': 'بوطرا',
            'specialty': 'Orthopedics',
            'wilaya': '10',
            'commune': 'Bouira',
            'commune_ar': 'البويرة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0550424645'
        },

        # =====================================================
        # DENTISTRY
        # =====================================================

        {
            'first_name': 'Abdelkader Djilani',
            'last_name': 'Miri',
            'first_name_ar': 'عبد القادر جيلاني',
            'last_name_ar': 'ميري',
            'specialty': 'Dentistry',
            'wilaya': '09',
            'commune': 'Blida',
            'commune_ar': 'البليدة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0557081933'
        },

        {
            'first_name': 'Arab',
            'last_name': 'Djerroud',
            'first_name_ar': 'عرب',
            'last_name_ar': 'جراود',
            'specialty': 'Dentistry',
            'wilaya': '16',
            'commune': 'Rouiba',
            'commune_ar': 'الرويبة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0663205878'
        },

        # =====================================================
        # GYNECOLOGY
        # =====================================================

        {
            'first_name': 'Abdeldjalil',
            'last_name': 'Amokrane',
            'first_name_ar': 'عبد الجليل',
            'last_name_ar': 'عمقران',
            'specialty': 'Gynecology',
            'wilaya': '31',
            'commune': 'Bir El Djir',
            'commune_ar': 'بئر الجير',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0771932330'
        },

        # =====================================================
        # MAXILLOFACIAL
        # =====================================================

        {
            'first_name': 'Asmahen',
            'last_name': 'Ahriz',
            'first_name_ar': 'أسمهان',
            'last_name_ar': 'أحريز',
            'specialty': 'Surgery',
            'wilaya': '25',
            'commune': 'El Khroub',
            'commune_ar': 'الخروب',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0562119016'
        },

        # =====================================================
        # AESTHETIC / PLASTIC SURGERY
        # =====================================================

        {
            'first_name': 'Ali',
            'last_name': 'Benyelles',
            'first_name_ar': 'علي',
            'last_name_ar': 'بن يلس',
            'specialty': 'Surgery',
            'wilaya': '31',
            'commune': 'Oran',
            'commune_ar': 'وهران',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0540671593'
        },

        {
            'first_name': 'Hakim',
            'last_name': 'Rahmani',
            'first_name_ar': 'حكيم',
            'last_name_ar': 'رحماني',
            'specialty': 'Surgery',
            'wilaya': '16',
            'commune': 'Birtouta',
            'commune_ar': 'بئر توتة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0553418486'
        },

        {
            'first_name': 'Sadi',
            'last_name': '',
            'first_name_ar': 'سعدي',
            'last_name_ar': '',
            'specialty': 'Surgery',
            'wilaya': '16',
            'commune': 'Cheraga',
            'commune_ar': 'الشراقة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0554126080'
        },

        {
            'first_name': 'Dounia',
            'last_name': 'Slimani',
            'first_name_ar': 'دنيا',
            'last_name_ar': 'سليماني',
            'specialty': 'Surgery',
            'wilaya': '16',
            'commune': 'Kouba',
            'commune_ar': 'القبة',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0554687290'
        },

        {
            'first_name': 'Takieddine',
            'last_name': 'Mehdi',
            'first_name_ar': 'تقي الدين',
            'last_name_ar': 'مهدي',
            'specialty': 'Surgery',
            'wilaya': '14',
            'commune': 'Tiaret',
            'commune_ar': 'تيارت',
            'clinic': None,
            'clinic_ar': None,
            'phone': '0776244446'
        },

    ]


    # =========================================================
    # 5. إضافة البلديات
    # =========================================================

    for data in DOCTORS_DATA:

        wilaya = Wilaya.query.filter_by(
            code=data['wilaya']
        ).first()

        if not wilaya:
            print(
                f"WARNING: Wilaya {data['wilaya']} "
                f"not found for {data['first_name']} {data['last_name']}"
            )
            continue

        # البحث عن البلدية
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


    # =========================================================
    # 6. إضافة الأطباء (مع التعديلات الجديدة)
    # =========================================================

    added_count = 0
    skipped_count = 0

    for data in DOCTORS_DATA:

        # البحث عن التخصص
        specialty = Specialty.query.filter_by(
            name=data['specialty']
        ).first()

        if not specialty:
            print(
                f"WARNING: Specialty not found: "
                f"{data['specialty']} "
                f"for {data['first_name']} {data['last_name']}"
            )
            skipped_count += 1
            continue

        # البحث عن الولاية
        wilaya = Wilaya.query.filter_by(
            code=data['wilaya']
        ).first()

        if not wilaya:
            print(
                f"WARNING: Wilaya not found: "
                f"{data['wilaya']}"
            )
            skipped_count += 1
            continue

        # البحث عن البلدية
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
            db.session.flush()

        # منع تكرار الطبيب (محسّن)
        existing_doctor = Doctor.query.filter(
            Doctor.first_name == data['first_name'],
            Doctor.last_name == data['last_name'],
            Doctor.specialty_id == specialty.id,
            Doctor.wilaya_id == wilaya.id
        ).first()

        if existing_doctor:
            print(
                f"SKIP: Doctor already exists -> "
                f"{data['first_name']} {data['last_name']}"
            )
            skipped_count += 1
            continue

        # إنشاء العيادة فقط إذا كانت موجودة في البيانات
        clinic = None

        if data.get('clinic') and data['clinic'].strip():
            clinic = Clinic.query.filter_by(
                name=data['clinic']
            ).first()

            if not clinic:
                clinic = Clinic(
                    name=data['clinic'],
                    name_ar=data.get('clinic_ar'),
                    address=data.get('commune', ''),
                    address_ar=data.get('commune_ar', ''),
                    wilaya_id=wilaya.id,
                    commune_id=commune.id if commune else None,
                    phone=data.get('phone') or '',
                    is_active=True
                )
                db.session.add(clinic)
                db.session.flush()

        # إنشاء الطبيب (مع phone اختياري و clinic_id اختياري)
        doctor = Doctor(
            first_name=data['first_name'],
            last_name=data['last_name'],
            first_name_ar=data.get('first_name_ar'),
            last_name_ar=data.get('last_name_ar'),
            specialty_id=specialty.id,
            wilaya_id=wilaya.id,
            commune_id=commune.id if commune else None,
            phone=data.get('phone'),  # أصبح nullable=True
            clinic_id=clinic.id if clinic else None,
            accepts_new_patients=True,
            is_verified=True,
            is_featured=False,
            is_published=True,
            is_active=True
        )

        # إنشاء slug
        try:
            doctor.slug = doctor.generate_slug()
        except Exception:
            pass

        db.session.add(doctor)
        db.session.flush()

        # أوقات العمل
        existing_hours = WorkingHour.query.filter_by(
            doctor_id=doctor.id
        ).count()

        if existing_hours == 0:
            for day in range(7):
                working_hour = WorkingHour(
                    doctor_id=doctor.id,
                    day_of_week=day,
                    start_time='08:00',
                    end_time='16:00',
                    is_closed=False
                )
                db.session.add(working_hour)

        added_count += 1

        print(
            f"ADDED: {data['first_name']} "
            f"{data['last_name']} "
            f"- {data['specialty']} "
            f"- {data['commune']}"
        )

    db.session.commit()


    # =========================================================
    # 7. الخدمات الطبية
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
    # 8. إعدادات المنصة
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


    # =========================================================
    # 9. النتيجة
    # =========================================================

    print("=" * 60)
    print("Database seeded successfully!")
    print(f"Doctors added   : {added_count}")
    print(f"Doctors skipped : {skipped_count}")
    print("=" * 60)
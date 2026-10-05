from app import create_app
from app.extensions import db
from app.models import PlatformSetting

app = create_app()

with app.app_context():
    # تحديث اسم المنصة
    setting = PlatformSetting.query.filter_by(key='platform_name').first()
    if setting:
        print(f"القيمة القديمة: {setting.value}")
        setting.value = 'TebGuide'
        db.session.commit()
        print(f"✅ القيمة الجديدة: {setting.value}")
    else:
        print("❌ لم يتم العثور على إعداد platform_name")
        # أنشئه إذا لم يكن موجوداً
        new_setting = PlatformSetting(
            key='platform_name',
            value='TebGuide',
            category='general'
        )
        db.session.add(new_setting)
        db.session.commit()
        print("✅ تم إنشاء الإعداد: TebGuide")
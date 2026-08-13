from app import create_app
from app.extensions import db
from app.models import User, Doctor, Clinic, Specialty, Wilaya, Commune, Service, WorkingHour, Holiday, Report, PlatformSetting
from app.services.seed_service import seed_database

app = create_app()

# ⚡ إنشاء البيانات الأولية وحساب الأدمن تلقائياً في قاعدة البيانات
with app.app_context():
    seed_database()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Doctor': Doctor,
        'Clinic': Clinic,
        'Specialty': Specialty,
        'Wilaya': Wilaya,
        'Commune': Commune,
        'Service': Service,
        'WorkingHour': WorkingHour,
        'Holiday': Holiday,
        'Report': Report,
        'PlatformSetting': PlatformSetting
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
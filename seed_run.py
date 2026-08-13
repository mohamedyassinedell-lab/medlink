from app import create_app
from app.services.seed_service import seed_database

app = create_app()
with app.app_context():
    seed_database()
    print("✅ Database seeded successfully!")
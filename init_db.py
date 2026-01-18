import datetime
from backend.database import db
from backend.models import User, Doctor, Appointment
from flask import Flask

# Setup temporary app for seeding / initial DB creation
app = Flask(__name__)

# Use SAME DB as main application
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    print("🔄 Creating database and tables...")

    # Optional: Clear old tables (remove if you want to keep data)
    # db.drop_all()

    db.create_all()

    print("✅ Inserting dummy data...")

    # Create user
    user = User(
        fullName="admin",
        email="admin@gmail.com",
        age=30,
        phone="1234567890",
        address="123 Main Street",
        password="1234567890",  # Note: hash in production
        type="admin"
    )

    # Create doctor
    doctor = Doctor(
        full_name="doctor1",
        email="doctor1@gmail.com",
        phone="9876543210",
        specialty="Cardiology",
        password="1234567890",
        status="approved",
        age=40,
        address="456 Clinic Ave",
        clinic_status="open"
    )

    # Add and persist to generate IDs
    db.session.add(user)
    db.session.add(doctor)
    db.session.commit()

    # Create appointment using auto-assigned IDs
    appointment = Appointment(
        user_id=user.id,
        doctor_id=doctor.id,
        appointment_date=datetime.date.today(),
        appointment_time="10:30 AM",
        symptoms="Chest pain & shortness of breath",
        status="pending",
        token_number="A001"
    )

    db.session.add(appointment)
    db.session.commit()

    print("🎉 Dummy data inserted successfully!")

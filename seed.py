# faker.py
from models import db, User, Client, HealthProgram, Enrollment  # Adjust if your models are elsewhere
from faker import Faker
from datetime import datetime, timedelta, timezone
import random

fake = Faker()

def clear_tables():
    """Clear the database tables before seeding new data."""
    print("Clearing existing data...")
    Enrollment.query.delete()
    Client.query.delete()
    HealthProgram.query.delete()
    User.query.delete()
    db.session.commit()
    print("Tables cleared.")

def seed_users(n=5):
    users = []
    for _ in range(n):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            role=random.choice(['DOCTOR', 'ADMIN'])  # Ensure roles are uppercase
        )
        user.set_password('password123')  # default password for all
        users.append(user)
        db.session.add(user)
    db.session.commit()
    return users

def seed_health_programs(users, n=5):
    programs = []
    for _ in range(n):
        program = HealthProgram(
            name=fake.catch_phrase(),
            created_by=random.choice(users).id
        )
        programs.append(program)
        db.session.add(program)
    db.session.commit()
    return programs

def seed_clients(n=10):
    clients = []
    for _ in range(n):
        dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
        client = Client(
            full_name=fake.name(),
            phone=fake.msisdn()[:15],
            address=fake.address(),
            date_of_birth=dob,
            gender=random.choice(['Male', 'Female', 'Other']),
            created_at=fake.date_time_this_year(tzinfo=timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        clients.append(client)
        db.session.add(client)
    db.session.commit()
    return clients

def seed_enrollments(clients, programs):
    for client in clients:
        num_programs = random.randint(1, 3)  # Enroll each client in 1-3 programs
        enrolled_programs = random.sample(programs, num_programs)
        for program in enrolled_programs:
            enrollment = Enrollment(
                client_id=client.id,
                program_id=program.id,
                enrolled_at=fake.date_time_this_year(tzinfo=timezone.utc),
                status=random.choice(['active', 'completed', 'dropped'])
            )
            db.session.add(enrollment)
    db.session.commit()

def run_seeders():
    clear_tables()  # Clear the tables first
    print("Seeding database...")
    users = seed_users()
    programs = seed_health_programs(users)
    clients = seed_clients()
    seed_enrollments(clients, programs)
    print("Done seeding!")

if __name__ == "__main__":
    from app import app  # assuming your Flask app is in app.py

    with app.app_context():
        run_seeders()

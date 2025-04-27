import re
from flask_sqlalchemy import SQLAlchemy;
from sqlalchemy_serializer import SerializerMixin;
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
import enum
from datetime import datetime, date, timezone
db = SQLAlchemy()
bcrypt = Bcrypt()

class UserRole(enum.Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable = False, unique = True)
    email = db.Column(db.String(120), nullable = False, unique = True)
    password_hash = db.Column(db.String, nullable = False)
    role = db.Column(db.Enum(UserRole), nullable = False)
    
    # Hash the password before saving it to the database
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    # Check if the given password matches the stored password hash
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        return email

    @validates('password_hash')
    def validate_password(self, key, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return password

    
    def __repr__(self):
        return f"<User {self.username} {self.email}>"
    
    
# HealthProgram Model
class HealthProgram(db.Model, SerializerMixin):
    __tablename__ = 'health_programs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    creator = db.relationship('User', backref='programs')
    enrollments = db.relationship('Enrollment', back_populates='program', lazy=True)
    
    # exclude creator.programs to avoid recursion depth
    serialize_rules = ('-creator.programs', '-creator.password_hash', '-creator.role',)
    
    @validates('name')
    def validate_name(self, key, name):
        if not name.strip():
            raise ValueError("Program name cannot be empty")
        return name
    

# Client Model
class Client(db.Model, SerializerMixin):
    __tablename__ = "clients"
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    enrollments = db.relationship('Enrollment', back_populates='client', lazy=True)

    serialize_rules = ('-enrollments',)

    @hybrid_property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    @validates('gender')
    def validate_gender(self, key, gender):
        allowed = ['Male', 'Female', 'Other']
        if gender not in allowed:
            raise ValueError(f"Gender must be one of {allowed}")
        return gender

    @validates('date_of_birth')
    def validate_date_of_birth(self, key, dob):
        if dob >= date.today():
            raise ValueError("Date of birth must be in the past")
        return dob

    @validates('full_name')
    def validate_full_name(self, key, full_name):
        if len(full_name.strip()) < 3:
            raise ValueError("Full name must be at least 3 characters long")
        if len(full_name.strip()) > 120:
            raise ValueError("Full name cannot be longer than 120 characters")
        return full_name
    
    @validates('address')
    def validate_address(self, key, address):
        if address and len(address.strip()) > 255:
            raise ValueError("Address cannot be longer than 255 characters")
        return address

    @validates('phone')
    def validate_phone(self, key, phone):
        if phone and not re.match(r"^\+?\d{1,3}?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$", phone):
            raise ValueError("Phone number format is invalid. Include country code.")
        if phone and (len(phone) < 10 or len(phone) > 15):
            raise ValueError("Phone number must be between 10 and 15 digits")
        return phone
    
    
class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('health_programs.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='active')  # active, completed, dropped

    client = db.relationship('Client', back_populates='enrollments')
    program = db.relationship('HealthProgram', back_populates='enrollments')
    
    serialize_rules = ('-client.enrollments', '-program.enrollments',)
    
    @validates('status')
    def validate_status(self, key, status):
        allowed_statuses = ['active', 'completed', 'dropped']
        if status not in allowed_statuses:
            raise ValueError(f"Status must be one of {allowed_statuses}")
        return status

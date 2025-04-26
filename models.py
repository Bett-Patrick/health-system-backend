from flask_sqlalchemy import SQLAlchemy;
from sqlalchemy_serializer import SerializerMixin;
from flask_bcrypt import Bcrypt
import enum

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

    
    def __repr__(self):
        return f"<User {self.username} {self.email}>"
    
    
# HealthProgram Model
class HealthProgram(db.Model, SerializerMixin):
    __tablename__ = 'health_programs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    creator = db.relationship('User', backref='programs')
    
    # exclude creator.programs to avoid recursion depth
    serialize_rules = ('-creator.programs', '-creator.password_hash', '-creator.role',)
    
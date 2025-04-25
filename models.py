from flask_sqlalchemy import SQLAlchemy;
from sqlalchemy_serializer import SerializerMixin;
import enum

db = SQLAlchemy();

class UserRole(enum.Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable = False, unique = True)
    email = db.Column(db.String, nullable = False, unique = True)
    role = db.Column(db.Enum(UserRole), nullable = False)
    password = db.Column(db.String, nullable = False)

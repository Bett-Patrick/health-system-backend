from flask import Flask, request, make_response ;
from flask_migrate import Migrate
from flask_restful import Resource,Api
from models import db, bcrypt, User, UserRole
from dotenv import load_dotenv
import os
import jwt
import datetime
from functools import wraps

# Load environment variables
load_dotenv()

# flask app configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize the database and bcrypt
migrate = Migrate(app, db)
db.init_app(app)
bcrypt.init_app(app)
api = Api(app)



# Decorator to check if the user is authenticated
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return make_response({"error": "Token is missing!"}, 401)
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
        except Exception as e:
            return make_response({"error": str(e)}, 401)
        
        return f(current_user, *args, **kwargs)
    
    return decorated



# Routes

# Home Resource
@app.route("/")
def index():
    return make_response("<h1>Welcome to Health Information System(HIS) API</h1>", 200)

# RegisterAdmin Resource
class RegisterAdmin(Resource):
    def post(self):
        if User.query.first():
            return make_response({"error":"Admin already exists"}, 403)
        
        data = request.json
        # Extract data from the request
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        
        if not all([username, email, password]):
            return make_response({"error" : "Missing required fields"}, 400)
        
        user = User(
            username = username,
            email = email,
            role = UserRole.ADMIN
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            return make_response({"message" : "Admin registered successfully"}, 200)
        except Exception as e:
            db.session.rollback()
            return make_response({"error" : str(e)}, 500)
        
        

# Login Resource
class Login(Resource):
    def post(self):
        data = request.json
        
        # Extract data from the request
        email = data.get("email")
        password = data.get("password")
        
        if not all([email, password]):
            return make_response({"error" : "Email and password are required"}, 400)
        
        user = User.query.filter_by(email = email).first()
        
        if not user or not user.check_password(password):
            return make_response({"error" : "Invalid credentials"}, 401)
        
        # Generate JWT token
        token = jwt.encode({
            "user_id": user.id,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        # Return the token in the response
        return make_response({
            "message" : "Login successful",
            "token" : token,
            "user" : {
                "id" : user.id,
                "username" : user.username,
                "email" : user.email,
                "role" : user.role.value
            }
        }, 200)
        
        

# RegisterDoctor Resource
class RegisterDoctor(Resource):
    @token_required
    def post(current_user, self):
        data = request.json
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not all([username, email, password]):
            return make_response({"error": "Missing required fields"}, 400)

        if User.query.filter_by(email=email).first():
            return make_response({"error": "Email already exists"}, 400)

        doctor = User(
            username=username,
            email=email,
            role=UserRole.DOCTOR
        )
        doctor.set_password(password)

        db.session.add(doctor)
        db.session.commit()

        return make_response({
            "message": "Doctor registered successfully",
            "doctor": {
                "id": doctor.id,
                "username": doctor.username,
                "email": doctor.email,
                "role": doctor.role.value
            }
        }, 201)

        
        
        
api.add_resource(RegisterAdmin, "/register-admin")
api.add_resource(Login, "/login")
api.add_resource(RegisterDoctor, "/register-doctor")
        
    
    

if __name__ == '__main__':
    app.run(port = 5555, debug=True)
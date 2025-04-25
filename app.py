from flask import Flask, request, make_response ;
from flask_migrate import Migrate
from flask_restful import Resource,Api
from models import db, bcrypt, User, UserRole


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)
bcrypt.init_app(app)
api = Api(app)


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
        
        return make_response({
            "message" : "Login successful",
            "user" : {
                "id" : user.id,
                "username" : user.username,
                "email" : user.email,
                "role" : user.role.value
            }
        }, 200)
        
        

# RegisterDoctor Resource
class RegisterDoctor(Resource):
    def post(self):
        # Assuming user is already logged in, this part should be handled by authentication middleware
        # For simplicity, we're assuming the admin is already identified (e.g., using token in header)
        
        data = request.json
        admin_email = "admin@example.com"  # Admin email for now, could be retrieved from token

        # Check if the logged-in user is an admin (dummy check for now)
        user = User.query.filter_by(email=admin_email).first()
        if not user or user.role != UserRole.ADMIN:
            return make_response({"error": "Only an admin can register a doctor"}, 403)
        
        # Extract doctor details from the request
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        
        if not all([username, email, password]):
            return make_response({"error": "Missing required fields"}, 400)

        # Check if the email already exists
        if User.query.filter_by(email=email).first():
            return make_response({"error": "Email already exists"}, 400)
        
        # Create the new doctor user
        doctor = User(
            username=username,
            email=email,
            role=UserRole.DOCTOR
        )
        doctor.set_password(password)

        # Add the new doctor to the database
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
from flask import Flask, request, make_response ;
from flask_migrate import Migrate
from flask_restful import Resource,Api
from models import db, bcrypt, User, UserRole, HealthProgram, Client, Enrollment
from dotenv import load_dotenv
import os
import jwt
import datetime
from functools import wraps
from flask_cors import CORS

# Load environment variables
load_dotenv()

# flask app configuration
app = Flask(__name__, static_url_path='')
CORS(app, origins=["http://localhost:3000", "https://yourfrontend.com"])

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.json.compact = False

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
            # Decode the token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            
            # Check if the user exists
            if current_user is None:
                return make_response({"error": "User not found!"}, 404)
        
        except jwt.ExpiredSignatureError:
            return make_response({"error": "Token expired!"}, 401)
        except jwt.InvalidTokenError:
            return make_response({"error": "Invalid token!"}, 401)
        except Exception as e:
            return make_response({"error": str(e)}, 401)
        
        # Pass current_user as a keyword argument
        return f(*args, current_user=current_user, **kwargs)
    
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
            return make_response({"message" : "Admin registered successfully"}, 201)
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
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
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
    def post(self, current_user):
        if current_user.role != UserRole.ADMIN:
            return make_response({"error": "Only admin can register doctors"}, 403)
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


# Health Programs Resource
class Programs(Resource):
    # POST a health program
    @token_required
    def post(self,current_user):
        if current_user.role != UserRole.DOCTOR:
            return make_response({"error": "Only doctors can create health programs"}, 403)
        
        data = request.json
        name = data.get('name')
        
        if not name:
            return make_response({"error" : "Program name required !!"}, 400)
        
        if HealthProgram.query.filter_by(name=name).first():
            return make_response({"error" : "Program name already exists"}, 400)
        
        program = HealthProgram(
            name = name,
            created_by = current_user.id
        )
        
        db.session.add(program)
        db.session.commit()
        
        return make_response({
            "message" : "Health program created successfully",
            "program" : program.to_dict()
        }, 201)
       
    # GET all health programs
    @token_required
    def get(self, current_user):
        if current_user.role != UserRole.DOCTOR:
            return make_response({"error" : "Only doctors can view health programs"}, 403)
        
        programs = HealthProgram.query.all()
        if not programs:
            return make_response({"error" : "No health programs availlable yet"}, 404)
        
        programs_list = [program.to_dict() for program in programs]
        return make_response(programs_list, 200)
    
# Clients Resource
class Clients(Resource):
    @token_required
    def post(self, current_user):
        if current_user.role != UserRole.DOCTOR:
            return make_response({"error": "Only doctors can create clients"}, 403)
        
        data = request.json
        full_name = data.get('full_name')
        gender = data.get('gender')
        phone = data.get('phone')
        address = data.get('address')
        date_of_birth = data.get('date_of_birth')
        
        # Validate required fields
        if not all([full_name, gender, phone, date_of_birth]):
            return make_response({"error": "Missing required fields"}, 400)
        
        try:
            # Parse the date_of_birth field into a datetime.date object
            date_of_birth = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        except ValueError:
            return make_response({"error": "Invalid date format. Expected format: YYYY-MM-DD"}, 400)
        
        try:
            # create new client
            client = Client(
                full_name=full_name,
                phone=phone,
                address=address,
                date_of_birth=date_of_birth,
                gender=gender
            )
            
            db.session.add(client)
            db.session.commit()
            
            return make_response({
                "message": "Patient created successfully",
                "client": client.to_dict()
            }, 201)
        
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400

    # GET all clients
    @token_required
    def get(self, current_user):
        if current_user.role != UserRole.DOCTOR:
            return make_response({"error": "Only doctors can view clients"}, 403)
        
        # Fetch all clients
        clients = Client.query.all()
        if not clients:
            return make_response({"error": "No clients available yet"}, 404)
        
        # Include enrollments in the response
        clients_data = []
        for client in clients:
            client_data = client.to_dict()
            client_data['enrollments'] = [enrollment.to_dict() for enrollment in client.enrollments]
            clients_data.append(client_data)
        
        return make_response(clients_data, 200)
   
                
                
class ClientsById(Resource):
    def get(self, id):
        if id is None:
            return make_response({"error": "Client ID is required"}, 400)
        # Fetch client by ID
        client = Client.query.get(id)
        if not client:
            return make_response({"error": f"Client with ID {id} not registered"}, 404)
        
        client_data = client.to_dict()
        client_data['enrollments'] = [enrollment.to_dict() for enrollment in client.enrollments]
        return make_response(client_data, 200) 

# EnrollClient Resource
class EnrollClient(Resource):
    @token_required
    def post(self, current_user):
        # Ensure only doctors can enroll clients
        if current_user.role != UserRole.DOCTOR:
            return make_response({"error": "Only doctors can enroll clients in programs"}, 403)
        
        data = request.json
        client_id = data.get('client_id')
        program_ids = data.get('program_ids')

        if not client_id or not program_ids:
            return make_response({"error": "Client ID and Program IDs are required"}, 400)

        # Fetch the client
        client = Client.query.get(client_id)
        if not client:
            return make_response({"error": "Client not found"}, 404)

        # Enroll the client in the specified programs
        for program_id in program_ids:
            program = HealthProgram.query.get(program_id)
            if not program:
                return make_response({"error": f"Program with ID {program_id} not found"}, 404)

            # Check if the client is already enrolled in the program
            existing_enrollment = Enrollment.query.filter_by(client_id=client_id, program_id=program_id).first()
            if existing_enrollment:
                # Skip if already enrolled
                continue  

            # Create a new enrollment
            enrollment = Enrollment(client_id=client_id, program_id=program_id)
            db.session.add(enrollment)

        # Commit the changes
        db.session.commit()

        return make_response({"message": "Client enrolled in programs successfully"}, 201)
        
        
        
api.add_resource(RegisterAdmin, "/register-admin")
api.add_resource(Login, "/login")
api.add_resource(RegisterDoctor, "/register-doctor")
api.add_resource(Programs, "/programs")
api.add_resource(Clients, "/clients")
api.add_resource(ClientsById, "/clients/<int:id>")
api.add_resource(EnrollClient, "/enroll-client")
        
    
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
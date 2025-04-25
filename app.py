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
        
api.add_resource(RegisterAdmin, "/register-admin")
        
    
    

if __name__ == '__main__':
    app.run(port = 5555, debug=True)
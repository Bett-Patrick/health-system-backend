from flask import Flask ;
from flask_migrate import Migrate
from flask_restful import Resource,Api
from models import db


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)


# Routes
@app.route("/")
def index():
    return "<h1>Welcome to Health Information System(HIS) API</h1>"

if __name__ == '__main__':
    app.run(port = 5555, debug=True)
from flask import Flask
from flask_restful import Api
import os
from flask_jwt_extended import JWTManager

from resources.car import CarList, Car
from resources.driver import Driver
from resources.assign import AssignDriverToCar
from resources.fleet import FleetList, Fleet
from resources.car_fleet import CarFleet
from resources.register import UserRegister
from resources.user import User
from resources.auth import Auth
from db import db

# we have to import the models so that they are created
# when the app is initialized
from models.car import CarModel
from models.driver import DriverModel
from models.fleet import FleetModel
from models.car_fleet import CarFleetLink
from models.user import UserModel

app = Flask(__name__)
api = Api(app)
db_path = os.path.join(os.path.dirname(__file__), 'database.db')

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
# initialize the app with the extension
db.init_app(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# this is the new syntax for creating the tables
with app.app_context():
  print('Creating database tables...')
  db.create_all()


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
  print('user_identity_lookup')
  print(user)
  return user.id


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
  print('user_lookup_callback')
  identity = jwt_data["sub"]
  return UserModel.find_by_id(identity) or None


api.add_resource(CarList, '/cars')
api.add_resource(Car, '/car/<string:plate>')
api.add_resource(Driver, '/driver')
api.add_resource(AssignDriverToCar, '/assign')
api.add_resource(FleetList, '/fleets')
api.add_resource(Fleet, '/fleet/<string:name>')
api.add_resource(CarFleet, '/car_fleet')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user')
api.add_resource(Auth, '/auth')

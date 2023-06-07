from flask import Flask
from flask_restful import Api
import os

from resources.car import CarList, Car
from resources.driver import Driver
from resources.assign import AssignDriverToCar
from resources.fleet import FleetList, Fleet
from resources.car_fleet import CarFleet
from db import db

# we have to import the models so that they are created
# when the app is initialized
from models.car import CarModel
from models.driver import DriverModel
from models.fleet import FleetModel
from models.car_fleet import CarFleetLink

app = Flask(__name__)
api = Api(app)
db_path = os.path.join(os.path.dirname(__file__), 'database.db')

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
# initialize the app with the extension
db.init_app(app)

# this is the new syntax for creating the tables
with app.app_context():
  print('Creating database tables...')
  db.create_all()

api.add_resource(CarList, '/cars')
api.add_resource(Car, '/car/<string:plate>')
api.add_resource(Driver, '/driver')
api.add_resource(AssignDriverToCar, '/assign')
api.add_resource(FleetList, '/fleets')
api.add_resource(Fleet, '/fleet/<string:name>')
api.add_resource(CarFleet, '/car_fleet')

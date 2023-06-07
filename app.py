from flask import Flask
from flask_restful import Api
import os

from resources.car import CarList, Car
from db import db

# we have to import the models so that they are created
# when the app is initialized
from models.car import CarModel
from models.driver import DriverModel

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

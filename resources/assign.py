from flask_restful import reqparse, Resource
from models.driver import DriverModel
from models.car import CarModel
from db import db


class AssignDriverToCar(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('driver_id',
                      type=int,
                      required=True,
                      help="This field cannot be left blank!")
  parser.add_argument('car_id',
                      type=int,
                      required=True,
                      help="This field cannot be left blank!")

  def post(self):
    data = AssignDriverToCar.parser.parse_args()
    driver = DriverModel.find_by_id(data['driver_id'])
    if not driver:
      return {'message': 'Driver not found'}, 404
    car = CarModel.find_by_id(data['car_id'])
    if not car:
      return {'message': 'Car not found'}, 404

    if car.driver_id == driver.id:
      return {
          'message':
          f'Driver {driver.name} is already assigned to car {car.license_plate}'
      }, 400

    # if the car has another driver... one driver can not drive two cars at the same time
    other_driver = db.session.query(CarModel).filter(
        CarModel.driver_id == driver.id).first()

    if other_driver:
      return {
          'message':
          f'Driver {driver.name} is already assigned to car {other_driver.license_plate}'
      }, 400

    if car.driver_id is not None:
      return {'message': f'car already has a driver'}, 400

    # if the code reaches this point, it means that the car is not assigned to any driver
    # and the driver is not assigned to any car
    # so we can assign the driver to the car
    car.driver_id = driver.id
    db.session.commit()

    return {
        'message':
        f'Driver {driver.name} was assigned to car {car.license_plate}'
    }, 201

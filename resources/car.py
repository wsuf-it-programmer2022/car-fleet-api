from flask_restful import Resource, reqparse
from models.car import CarModel


class Car(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('type',
                      type=str,
                      required=True,
                      help="This field cannot be left blank!")

  def post(self, plate):
    car = CarModel.find_by_license_plate(plate)
    # the same line of code can be written as:
    # car = CarModel.query.filter_by(license_plate=plate).first()
    if car:
      return {
          'message': f'A car with license plate {plate} already exists'
      }, 400
    # the dequest data is a dictionary with the data that was sent by the client
    data = Car.parser.parse_args()
    car = CarModel(plate, data['type'])
    car.save_to_db()
    return {'message': 'Car created successfully'}, 201

  def delete(self, plate):
    car = CarModel.find_by_license_plate(plate)
    if car:
      car.delete_from_db()
      # if we don't create a method for deletion, we could just do:
      # db.session.delete(car)
      # db.session.commit()
      return {'message': 'Car deleted'}
    return {'message': 'Car not found'}, 404

  def put(self, plate):
    data = Car.parser.parse_args()
    car = CarModel.find_by_license_plate(plate)
    if car:
      car.type = data['type']
      car.save_to_db()
    else:
      return {'message': 'Car not found'}, 404
    return car.json()


class CarList(Resource):

  def get(self):
    # without list comprehension, the code would look like this:
    # carModels = CarModel.query.all()
    # cars = []
    # for car in carModels:
    #   cars.append(car.json())
    # return {'cars': cars}

    return {'cars': [car.json() for car in CarModel.query.all()]}

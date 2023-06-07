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
    if car:
      return {
          'message': f'A car with license plate {plate} already exists'
      }, 400
    # the dequest data is a dictionary with the data that was sent by the client
    data = Car.parser.parse_args()
    car = CarModel(plate, data['type'])
    car.save_to_db()
    return {'message': 'Car created successfully'}, 201


class CarList(Resource):

  def get(self):
    # without list comprehension, the code would look like this:
    # carModels = CarModel.query.all()
    # cars = []
    # for car in carModels:
    #   cars.append(car.json())
    # return {'cars': cars}

    return {'cars': [car.json() for car in CarModel.query.all()]}

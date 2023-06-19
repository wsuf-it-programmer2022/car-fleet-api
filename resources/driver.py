from flask_restful import reqparse, Resource
from models.driver import DriverModel


class Driver(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('name',
                      type=str,
                      required=True,
                      help="This field cannot be left blank!")

  def post(self):
    data = Driver.parser.parse_args()
    if data['name'] == "":
      return {'message': 'Driver name cannot be empty'}, 400
    driver = DriverModel(data['name'])
    driver.save_to_db()
    return {'message': 'Driver created successfully'}, 201

  def get(self):
    return {"drivers": [driver.json() for driver in DriverModel.query.all()]}

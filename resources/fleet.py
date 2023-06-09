from flask_restful import Resource
from models.fleet import FleetModel


class Fleet(Resource):

  def post(self, name):
    if FleetModel.find_by_name(name):
      return {'message': f'Fleet {name} already exists'}, 400

    fleet = FleetModel(name)
    fleet.save_to_db()
    return {'message': f'Fleet {name} created successfully'}, 201

  def get(self, name):
    fleet = FleetModel.find_by_name(name)
    if fleet:
      return fleet.json()
    return {'message': 'Fleet not found'}, 404

  def delete(self, name):
    fleet = FleetModel.find_by_name(name)
    if fleet:
      fleet.delete_from_db()
      return {'message': 'Fleet deleted'}
    return {'message': 'Fleet not found'}, 404


class FleetList(Resource):

  def get(self):
    return {'fleets': [fleet.json() for fleet in FleetModel.query.all()]}

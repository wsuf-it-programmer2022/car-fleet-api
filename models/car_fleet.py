from db import BaseModel
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from models.mixin import MixinModel


class CarFleetLink(BaseModel, MixinModel):
  __tablename__ = 'car_fleet'
  car_id = mapped_column(Integer, ForeignKey('cars.id'), primary_key=True)
  fleet_id = mapped_column(Integer, ForeignKey('fleets.id'), primary_key=True)

  def __init__(self, car_id, fleet_id):
    self.car_id = car_id
    self.fleet_id = fleet_id

  # we need a method to check if a link between a car and a fleet already exists
  @classmethod
  def link_exists(cls, car_id, fleet_id):
    return cls.query.filter_by(car_id=car_id, fleet_id=fleet_id).first()

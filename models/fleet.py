from db import BaseModel
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String
from models.mixin import MixinModel


class FleetModel(BaseModel, MixinModel):
  __tablename__ = 'fleets'
  id = mapped_column(Integer, primary_key=True)
  name = mapped_column(String(50))

  # many-to-many relationship: one fleet can have many cars, and one car can
  cars = relationship('CarModel',
                      secondary='car_fleet',
                      back_populates='fleets')

  def __init__(self, name):
    self.name = name

  def json(self):
    return {'name': self.name, 'id': self.id}

  @classmethod
  def find_by_id(cls, id):
    return cls.query.filter_by(id=id).first()

  @classmethod
  def find_by_name(cls, name):
    return cls.query.filter_by(name=name).first()

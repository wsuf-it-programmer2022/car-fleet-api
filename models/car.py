from db import BaseModel
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from models.mixin import MixinModel


class CarModel(BaseModel, MixinModel):
  __tablename__ = 'cars'
  # these lines will be converted to columns in the database
  id = mapped_column(Integer, primary_key=True)
  license_plate = mapped_column(String(7), unique=True)
  type = mapped_column(String(50))
  driver_id = mapped_column(Integer, ForeignKey('drivers.id'))

  # these are the relationships between the tables
  # this is a one-to-one relationship: one car has one driver
  # https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#one-to-one
  driver = relationship('DriverModel', back_populates='car', uselist=False)

  # many-to-many relationship: one car can be in many fleets, and many fleets
  # can have many cars
  # https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many
  fleets = relationship('FleetModel',
                        secondary='car_fleet',
                        back_populates='cars')

  # whenever we create a new instance of this class, we are actually
  # creating a new row in the database
  def __init__(self, license_plate, type):
    self.license_plate = license_plate
    self.type = type

  @classmethod
  def find_by_license_plate(cls, license_plate):
    return cls.query.filter_by(license_plate=license_plate).first()

  @classmethod
  def find_by_id(cls, id):
    return cls.query.filter_by(id=id).first()

  def json(self):
    return {'license_plate': self.license_plate, 'type': self.type}

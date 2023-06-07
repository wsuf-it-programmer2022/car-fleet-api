from db import BaseModel
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey


class DriverModel(BaseModel):
  __tablename__ = 'drivers'
  id = mapped_column(Integer, primary_key=True)
  name = mapped_column(String(50))

  # relationship with the CarModel
  # this is a one-to-one relationship: one driver has one car
  car = relationship('CarModel', back_populates='driver', uselist=False)

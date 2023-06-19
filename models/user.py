from db import BaseModel
from models.mixin import MixinModel
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String


class UserModel(BaseModel, MixinModel):
  __tablename__ = 'users'
  id = mapped_column(Integer, primary_key=True)
  username = mapped_column(String(80), unique=True)
  password = mapped_column(String(80))

  def __init__(self, username, password):
    self.username = username
    self.password = password

  def json(self):
    print('inside json')
    return {'name': self.username, 'id': self.id}

  @classmethod
  def find_by_username(cls, username):
    return cls.query.filter_by(username=username).first()

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()

  @classmethod
  def get_all(cls):
    return cls.query.all()

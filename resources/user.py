from flask_restful import Resource
from hmac import compare_digest
from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from models.user import UserModel


class User(Resource):

  @jwt_required()
  def get(self):
    print('current token is valid for {}'.format(current_user.json()))
    # current_user is User class instance
    return {"user": current_user.json()}, 200

  def authenticate(username, password):
    user = UserModel.find_by_id(username)
    if user and compare_digest(user.password, password):
      access_token = create_access_token(identity=user)
      return {"access_token": access_token}, 200
    return {"message": "Wrong username or password"}, 401

from hmac import compare_digest
from flask_jwt_extended import create_access_token
from datetime import timedelta
from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha512

from models.user import UserModel


class Auth(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('username',
                      type=str,
                      required=True,
                      help="This field cannot be blank.")
  parser.add_argument('password',
                      type=str,
                      required=True,
                      help="This field cannot be blank.")

  def post(self):
    data = Auth.parser.parse_args()
    print(data)
    user = UserModel.find_by_username(username=data.username)
    print(UserModel.get_all())
    if user and pbkdf2_sha512.verify(data.password, user.password):
      access_token = create_access_token(identity=user,
                                         expires_delta=timedelta(days=30))
      return {"access_token": access_token}, 200
    return {"message": "Wrong username or password"}, 401

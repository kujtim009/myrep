from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    fresh_jwt_required,
    get_jwt_claims,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)
from blacklist import BLACKLIST


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

_user_parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

_user_parser.add_argument('access_level',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )


class UserRegister(Resource):
    @fresh_jwt_required
    def post(self):
        if not UserModel.is_admin():
            return {'message': 'Admin privileges required'}
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'], data['access_level'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):
    @fresh_jwt_required
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}
        return user.json()

    @fresh_jwt_required
    def delete(self, user_id):
        if not UserModel.is_admin():
            return {'message': 'Admin privileges required'}
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}, 200


class UsersList(Resource):
    @fresh_jwt_required
    def get(self):
        return {'Users': list(map(lambda x: x.json(), UserModel.query.all()))}


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200

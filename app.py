from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin
from blacklist import BLACKLIST
import urllib
from resources.user import (
        UserRegister, 
        User, 
        UsersList, 
        UserLogin, 
        TokenRefresh, 
        UserLogout, 
        Add_allowed_fields,
        TestAPI)
from models.user import UserModel
import models.parameters as prm
from resources.records import (
        Record_by_license,
        RecordList,
        Record_by_state,
        Record_by_Individual_name,
        Record_by_license_and_state_prof,
        Record_by_company_name,
        getCurUserFields,
        getProfessions)


app = Flask(__name__)
CORS(app)
quoted = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=192.168.2.198\ITPLF;UID=" + prm.sql_username + ";PWD=" + prm.sql_password + ";DATABASE=InsertTool;Trusted_Connection=no;")
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect={}".format(quoted)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = prm.jwt_secret_key_stored
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

api = Api(app)
print("Username: {} and Password: {}".format(prm.sql_username, prm.sql_password))
@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)  # /auth


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    user = UserModel.find_by_id(identity)
    access_level = user.access_level
    return access_level


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


api.add_resource(TestAPI, '/test')
api.add_resource(Record_by_license, '/licence/<int:license>')
api.add_resource(Record_by_state, '/state/<string:state>')
api.add_resource(Record_by_Individual_name, '/full_name')
api.add_resource(RecordList, '/all_records')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UsersList, '/users')
api.add_resource(UserLogin, '/auth')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')
api.add_resource(Record_by_license_and_state_prof, '/lic_state')
api.add_resource(Record_by_company_name, '/company_name/<string:company>')
api.add_resource(getCurUserFields, '/usersField')
api.add_resource(Add_allowed_fields, '/addUserFields')
api.add_resource(getProfessions, '/professions')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    app.run(port=5000, debug=True)

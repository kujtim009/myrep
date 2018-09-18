from db import db
from flask_jwt_extended import get_jwt_claims, get_jwt_identity


class UserModel(db.Model):
    __tablename__ = 'api_fgx_Users'

    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    access_level = db.Column(db.String(80))
    

    def __init__(self, username, password, access_level):
        self.username = username
        self.password = password
        self.access_level = access_level

    def json(self):
        return {
            'id': self.ID,
            'username': self.username,
            'access_level': self.access_level
            }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(ID=_id).first()

    @classmethod
    def is_admin(cls):
        access = int(get_jwt_claims())
        if access == 1:
            return True
        return False

    
class Userinfo(db.Model):
    __tablename__ = 'api_fgx_Users_info'

    ID = db.Column(db.Integer, primary_key=True)
    User_id = db.Column(db.Integer, db.ForeignKey('api_fgx_Users.ID'))
    File_id = db.Column(db.Integer)
    File_name = db.Column(db.String(100))
    Field_name = db.Column(db.String(100))
    rlFields = db.relationship('UserModel', backref='user')

    def __init__(self, User_id, File_id, File_name, Field_name):
        self.User_id = User_id
        self.File_id = File_id
        self.File_name = File_name
        self.Field_name = Field_name

    def json(self):
        return {
            'ID': self.ID,
            'User_id': self.User_id,
            'File_id': self.File_id,
            'File_name': self.File_name,
            'Field_name': self.Field_name
            }

    @classmethod
    def get_user_fields(cls, userid):
        return cls.query.filter_by(User_id=userid).all()

    @classmethod
    def fieldExist_in_user(cls, fieldname):
        current_user_id = get_jwt_identity()
        record = cls.query.filter_by(User_id=current_user_id, Field_name=fieldname).count()
        if record >= 1:
            return True
        return False

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
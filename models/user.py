from db import db
from flask_jwt_extended import get_jwt_claims

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    access_level = db.Column(db.String(80))

    def __init__(self, username, password, access_level):
        self.username = username
        self.password = password
        self.access_level = access_level

    def json(self):
        return {
            'id': self.id,
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
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def is_admin(cls):
        access = int(get_jwt_claims())
        if access == 1:
            return True
        return False

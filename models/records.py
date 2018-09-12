from db import db, ma
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models.user import Userinfo

class ItemModel(db.Model):
    __tablename__ = 'test_master_licence'


    RecordID = db.Column(db.Integer, primary_key=True)
    Company_name = db.Column(db.String(80))
    Individual_name = db.Column(db.String(80))
    Professional_license_number = db.Column(db.String(40))
    Business_address_1 = db.Column(db.String(80))
    Business_state = db.Column(db.String(20))
    Business_phone = db.Column(db.String(20))


class RecordSchema(ma.ModelSchema):
       
    class Meta():
        model = ItemModel
        # fields = fieldlist

    @staticmethod
    def get_user_fields():
        userID = get_jwt_identity()
        record = Userinfo.get_user_fields(userID)
        if record:
            jsonRec = {'User_fields': [field.json() for field in record]}
        else:
            jsonRec = {'User_fields': []}
        
        # jsonRec = {'User_fields': '[]'} 
        mylist = [rec["Field_name"] for rec in jsonRec["User_fields"]]   
        return mylist  


    @classmethod
    def find_by_licence(cls, license):
        result = ItemModel.query.filter_by(Professional_license_number=license).all()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def find_by_licence_and_state(cls, license, state):
        if license is None and state is None:
            return jsonify({'Records': 'Search input is missing!'})

        if license is not None and state is None:
            result = ItemModel.query.filter_by(Professional_license_number=license).all()
        elif license is None and state is not None:
            result = ItemModel.query.filter_by(Business_state=state).all()
        else:
            result = ItemModel.query.filter_by(Professional_license_number=license, Business_state=state).all()

        # fields = cls.get_user_fields()
        
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def find_by_state(cls, state):
        result = ItemModel.query.filter_by(Business_state=state).all()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def get_all_records(cls):
        result = ItemModel.query.all()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def find_by_individual(cls, individual):
        result = ItemModel.query.filter(ItemModel.Individual_name.contains(individual)).all()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def find_by_compnay(cls, company):
        result = ItemModel.query.filter(ItemModel.Company_name.contains(company)).all()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

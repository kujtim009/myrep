from db import db, ma
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models.user import Userinfo

class ItemModel(db.Model):
    __tablename__ = 'Master_Layout'


    Record_id = db.Column(db.Integer, primary_key=True)
    Company_name = db.Column(db.String(80))
    First_name = db.Column(db.String(80))
    Middle_Initial = db.Column(db.String(80))
    Last_name = db.Column(db.String(80))
    License_Number = db.Column(db.String(40))
    Business_address_1 = db.Column(db.String(80))
    Business_state = db.Column(db.String(20))
    Business_phone = db.Column(db.String(20))
    License_type = db.Column(db.String(20))
    Profession = db.Column(db.String(200))
    Business_city = db.Column(db.String(200))
    Business_zip_5 = db.Column(db.String(200))
    Business_zip_4 = db.Column(db.String(200))

class RecordSchema(ma.ModelSchema):
    record_output = 100   
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
        result = ItemModel.query.filter_by(License_Number=license).limit(cls.record_output).all()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def find_by_licence_and_state(cls, license, state, prof):

        if license is None and state is None and prof is None:
            return jsonify({'Records': 'Search input is missing!'})

        if license is not None and state is not None and prof is not None:
            result = ItemModel.query.filter_by(License_Number=license, Business_state=state, Profession=prof).limit(cls.record_output).all()

        elif license is not None and state is None and prof is None:
            result = ItemModel.query.filter_by(License_Number=license).limit(cls.record_output).all()    

        elif license is None and state is not None and prof is None:
            result = ItemModel.query.filter_by(Business_state=state).limit(cls.record_output).all()

        elif license is None and state is not None and prof is not None:
            result = ItemModel.query.filter_by(Business_state=state, Profession=prof).limit(cls.record_output).all()

        elif license is not None and state is None and prof is not None:
            result = ItemModel.query.filter_by(License_Number=license, Profession=prof).limit(cls.record_output).all()    
        
        elif license is None and state is None and prof is not None:
            result = ItemModel.query.filter_by(Profession=prof).limit(cls.record_output).all()

        else:
            return jsonify({'Records': 'Search input is missing!'})

        fields = cls.get_user_fields()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def find_by_state(cls, state):
        result = ItemModel.query.filter_by(Business_state=state).limit(cls.record_output).all()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def get_all_records(cls):
        result = ItemModel.query.limit(cls.record_output).all()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def find_by_individual(cls, firstName, middleName, lastName):
        if firstName is None and middleName is None and lastName is None:
            return jsonify({'Records': 'Search input is missing!'})

        if firstName is not None and middleName is not None and lastName is not None:
            result = ItemModel.query.filter_by(First_name=firstName, Middle_Initial=middleName, Last_name=lastName).limit(cls.record_output).all()

        elif firstName is not None and middleName is None and lastName is None:
            result = ItemModel.query.filter_by(First_name=firstName).limit(cls.record_output).all()    

        elif firstName is None and middleName is not None and lastName is None:
            result = ItemModel.query.filter_by(Middle_Initial=middleName).limit(cls.record_output).all()

        elif firstName is None and middleName is not None and lastName is not None:
            result = ItemModel.query.filter_by(Middle_Initial=middleName, Last_name=lastName).limit(cls.record_output).all()

        elif firstName is not None and middleName is None and lastName is not None:
            result = ItemModel.query.filter_by(First_name=firstName, Last_name=lastName).limit(cls.record_output).all()    
        
        elif firstName is None and middleName is None and lastName is not None:
            result = ItemModel.query.filter_by(Last_name=lastName).limit(cls.record_output).all()

        else:
            return jsonify({'Records': 'Search input is missing!'})

        fields = cls.get_user_fields()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})


    @classmethod
    def find_by_compnay(cls, company):
        # result = ItemModel.query.filter(ItemModel.Company_name.contains(company)).limit(cls.record_output).all()
        result = ItemModel.query.filter(Business_state = company).limit(cls.record_output).all()
        record_schema = RecordSchema(many=True, only=cls.get_user_fields())
        output = record_schema.dump(result)
        return jsonify({'Records': output})

    @classmethod
    def getProfessions(cls):
        result = db.session.query(ItemModel.Profession, db.func.count(ItemModel.Profession)).group_by(ItemModel.Profession).all()
        # record_schema = RecordSchema(many=True)
        # output = record_schema.dump(result)
        # return jsonify({'Records': output})
        
            
        return result
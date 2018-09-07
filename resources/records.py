from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    fresh_jwt_required,
    get_jwt_identity)
from models.records import RecordSchema


class Record_by_license(Resource):
    @jwt_required
    def get(self, license):
        record = RecordSchema.find_by_licence(license)
        if record:
            return record
        return {'message': 'record not found'}, 404


class Record_by_license_and_state(Resource):
    @jwt_required
    def get(self):
        license = request.args.get('license', None)
        state = request.args.get('state', None)

        record = RecordSchema.find_by_licence_and_state(license, state)
        if record:
            return record
        return {'message': 'record not found'}, 404


class RecordList(Resource):
    @jwt_required
    def get(self):
        record = RecordSchema.get_all_records()
        if record:
            return record
        return {'message': 'records not found'}, 404


class Record_by_state(Resource):
    @jwt_required
    def get(self, state):
        record = RecordSchema.find_by_state(state)
        if record:
            return record
        return {'message': 'record not found'}, 404


class Record_by_Individual_name(Resource):
    @jwt_required
    def get(self, individual):
        record = RecordSchema.find_by_individual(individual)
        if record:
            return record
        return {'message': 'record not found'}, 404


class Record_by_company_name(Resource):
    @jwt_required
    def get(self, company):
        record = RecordSchema.find_by_compnay(company)
        if record:
            return record
        return {'message': 'record not found'}, 404

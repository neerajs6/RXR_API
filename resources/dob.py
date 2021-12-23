from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus

from webargs import fields
from webargs.flaskparser import use_kwargs
from schemas.dob import DobSchema, DobPaginationSchema

from models.dob import Dob
from schemas.dob import DobSchema

dob_schema = DobSchema()
dob_list_schema = DobSchema()

dob_pagination_schema = DobPaginationSchema()


class Index(Resource):
    @use_kwargs({'page': fields.Int(missing=1),
                 'per_page': fields.Int(missing=20)})
    def get(self, page=1):
        paginated_dob = Dob.get_all().paginate(page, 1).items
        return dob_pagination_schema.dump(paginated_dob), HTTPStatus.OK


class Products(Resource):
    def get(self,page=1):
        products = Dob.query.paginate(page, 10).items
        res = {}
        for product in products:
            res[product.id] = {
                'BBL': product.BBL,
                'year': product.year,
                'LATITUDE': product.LATITUDE
            }
        return jsonify(res)


class Random(Resource):
    def get(self):
        @use_kwargs({'page': fields.Int(missing=1),
                     'per_page': fields.Int(missing=20)})
        def get(self, year, page, per_page):
            paginated_recipes = Dob.get_by_year(year, page, per_page)
            return dob_pagination_schema.dump(paginated_recipes).data, HTTPStatus.OK


class DobListResource(Resource):
    @use_kwargs({'page': fields.Int(missing=1),
                 'per_page': fields.Int(missing=20)})
    def get(self, page, per_page):
        paginated_dob = Dob.get_all(page, per_page)
        return dob_pagination_schema.dump(paginated_dob), HTTPStatus.OK

    def post(self):
        json_data = request.get_json()
        data, errors = dob_schema.load(data=json_data)
        if errors:
            return {'message': 'Validation errors', 'errors': errors},HTTPStatus.BAD_REQUEST
        dob = Dob(**data)
        dob.save()
        return dob_schema.dump(dob).data, HTTPStatus.CREATED

class DobResource(Resource):
    def get(self, year):
        dob = Dob.get_by_year(year=year)
        if dob is None:
            return {'message': 'not found'}, HTTPStatus.NOT_FOUND
        data = dob_schema.dump(dob).data

        return data, HTTPStatus.OK

    def put(self, element_id):
        data = request.get_json()

        element = next((element for element in dob_list if element.id ==
                        element_id), None)
        if element is None:
            return {'message': 'not found'}, HTTPStatus.NOT_FOUND

        element.name = data['name']
        element.description = data['description']
        element.BOROUGH = data['BOROUGH']
        element.Job_Type = data['Job_Type']
        element.Block = data['Block']
        element.Lot = data['Lot']
        element.Zip_Code = data['Zip_Code']
        element.Work_Type = data['Work_Type']
        element.Permit_Status = data['Permit_Status']
        element.Filing_Status = data['Filing_Status']
        element.Permit_Type = data['Permit_Type']
        element.Permit_Subtype = data['Permit_Subtype']
        element.Issuance_Date = data['Issuance_Date']
        element.Expiration_Date = data['Expiration_Date']
        element.Job_Start_Date = data['Job_Start_Date']
        element.LATITUDE = data['LATITUDE']
        element.LONGITUDE = data['LONGITUDE']
        element.COUNCIL_DISTRICT = data['COUNCIL_DISTRICT']
        element.CENSUS_TRACT = data['CENSUS_TRACT']
        element.NTA_NAME = data['NTA_NAME']
        element.year = data['year']
        element.BBL = data['BBL']

        return element.data, HTTPStatus.OK
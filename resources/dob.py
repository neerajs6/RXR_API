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
    def get(self):
        page = request.args.get("page", 1, type=int)
        pageSize = request.args.get("pageSize", 10, type=int)

        results= Dob.get_by_year(2020).paginate(page, pageSize)
        res ={}

        res = {
            "results": [{r.id: {
                'ID': r.id,
                'BBL': r.BBL,
                'LATITUDE': r.LATITUDE,
                'LONGITUDE': r.LONGITUDE,
                'Job_Type': r.Job_Type
            }} for r in results.items],
        }
        return res

class Index2(Resource):
    @use_kwargs({'q': fields.Str(missing=''),
                'page': fields.Int(missing=1),
                'per_page': fields.Int(missing=10),
                'sort': fields.Str(missing='year'),
                'order': fields.Str(missing='desc')})
    def get(self, q, page, per_page, sort, order):
        if sort not in ['year', 'BBL']:
            sort = 'year'
        if order not in ['asc', 'desc']:
            order = 'desc'
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        results= Dob.get_all(q,page,per_page,sort,order).paginate(page=page, per_page=per_page)
        res ={}

        res = {
            "results": [{r.id: {
                'ID': r.id,
                'BBL': r.BBL,
                'LATITUDE': r.LATITUDE,
                'LONGITUDE': r.LONGITUDE,
                'Job_Type': r.Job_Type
            }} for r in results.items],
        }
        return res

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
        res = Dob.query.filter_by(year='2020').distinct()
        res_text = ''
        for r in res:
            res_text += r.Job_Type + ', '
        return res_text


class DobListResource(Resource):
    @use_kwargs({'page': fields.Int(missing=1),
                 'per_page': fields.Int(missing=20)})
    def get(self, page, per_page):
        paginated_dob = Dob.get_all(page, per_page)
        return dob_pagination_schema.dump(paginated_dob).data, HTTPStatus.OK

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

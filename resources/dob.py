from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus

from webargs import fields
from webargs.flaskparser import use_kwargs

from models.dob import Dob



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

class Year(Resource):
    @use_kwargs({'q': fields.Int(missing=0),
                'page': fields.Int(missing=1),
                'per_page': fields.Int(missing=10)
                },location='query')
    def get(self, q, page, per_page):
        results= Dob.get_all(q,page,per_page)
        res ={}

        res = {
            "results": [{r.id: {
                'year': r.year,
                'BBL': r.BBL,
                'LATITUDE': r.LATITUDE,
                'LONGITUDE': r.LONGITUDE,
                'Job_Type': r.Job_Type
            }} for r in results.items],
        }
        return res

class BBL(Resource):
    @use_kwargs({'q': fields.Int(missing=0),
                'page': fields.Int(missing=1),
                'per_page': fields.Int(missing=10)
                },location='query')
    def get(self, q, page, per_page):
        results= Dob.get_all(q,page,per_page)
        res ={}

        res = {
            "results": [{r.id: {
                'year': r.year,
                'BBL': r.BBL,
                'LATITUDE': r.LATITUDE,
                'LONGITUDE': r.LONGITUDE,
                'Job_Type': r.Job_Type
            }} for r in results.items],
        }
        return res

class yearBBL(Resource):
    @use_kwargs({'year': fields.Int(missing=0),
                 'BBL': fields.Int(missing=0),
                'page': fields.Int(missing=1),
                'per_page': fields.Int(missing=10)},
                location='query')
    def get(self, year,BBL, page, per_page):

        results= Dob.get_all2(year,BBL,page,per_page)
        res ={}

        res = {
            "results": [{r.id: {
                'year': r.year,
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

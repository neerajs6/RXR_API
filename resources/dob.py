from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus

from webargs import fields
from webargs.flaskparser import use_kwargs

from models.dob import Dob

class Year(Resource):
    @use_kwargs({'year': fields.Int(missing=0),
                'page': fields.Int(missing=1),
                'per_page': fields.Int(missing=10)
                },location='query')
    def get(self, year, page, per_page):
        results= Dob.get_all(year,page,per_page)
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
    @use_kwargs({'BBL': fields.Int(missing=0),
                'page': fields.Int(missing=1),
                'per_page': fields.Int(missing=10)
                },location='query')
    def get(self, BBL, page, per_page):
        results= Dob.get_all(BBL,page,per_page)
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




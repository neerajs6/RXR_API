from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus

from webargs import fields
from webargs.flaskparser import use_kwargs

from models.cleaned_311 import Cleaned_311




class Cleaned_311(Resource):
    @use_kwargs({'q': fields.Int(missing=''),
                'page': fields.Int(missing=1),
                'per_page': fields.Int(missing=10)
                },location='query')
    def get(self, q, page, per_page):
        results= Cleaned_311.get_all(q,page,per_page)
        res ={}

        res = {
            "results": [{r.UNIQUE_KEY: {
                'year': r.YEAR,
                'BBL': r.BBL,
                'LATITUDE': r.LATITUDE,
                'LONGITUDE': r.LONGITUDE,
                'STATUS': r.STATUS,
                'CTYPE': r.CTYPE
            }} for r in results.items],
        }
        return res


class Cleaned311YearBBL(Resource):
    @use_kwargs({'year': fields.Int(missing=0),
                 'BBL': fields.Int(missing=0),
                'page': fields.Int(missing=1),
                'per_page': fields.Int(missing=10)},
                location='query')
    def get(self, year,BBL, page, per_page):

        results= Cleaned_311.get_all2(year,BBL,page,per_page)
        res ={}

        res = {
            "results": [{r.UNIQUE_KEY: {
                'year': r.YEAR,
                'BBL': r.BBL,
                'LATITUDE': r.LATITUDE,
                'LONGITUDE': r.LONGITUDE,
                'STATUS': r.STATUS,
                'CTYPE': r.CTYPE
            }} for r in results.items],
        }
        return res




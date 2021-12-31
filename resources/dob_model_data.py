from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus

from webargs import fields
from webargs.flaskparser import use_kwargs

from models.dob_model_data import Dob_Model_Data


class Dob_Model(Resource):
    @use_kwargs({'q': fields.Int(missing=2020),
                'page': fields.Int(missing=1),
                'per_page': fields.Int(missing=10)
                },location='query')
    def get(self, q, page, per_page):
        q=2000
        results= Dob_Model_Data.get_all(q,page,per_page)
        res ={}

        res = {
            "results": [{r.unique_ID: {
                'year': r.year,
                'BBL': r.BBL,
                'A1_AL' : r.A1_AL,
                'A1_EQ': r.A1_EQ,
                'A1_FO': r.A1_FO,
                'A1_FP': r.A1_FP,
                'A1_PL' : r.A1_PL,
                'A1_SD': r.A1_SD,
                'A1_SP': r.A1_SP
            }} for r in results.items],
        }
        return res





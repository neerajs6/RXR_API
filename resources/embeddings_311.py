from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus

from webargs import fields
from webargs.flaskparser import use_kwargs

from models.embeddings_311 import Embeddings_311


class Embeddings(Resource):
    @use_kwargs({'q': fields.Int(missing=''),
                'page': fields.Int(missing=1),
                'per_page': fields.Int(missing=10)
                },location='query')
    def get(self, q, page, per_page):
        results= Embeddings_311.get_all(q,page,per_page)
        res ={}

        res = {
            "results": [{r.CTYPE_LOWER: {
                'Cluster': r.CLUSTER,
                'EMBEDDING': r.EMBEDDING
            }} for r in results.items],
        }
        return res

# Uncomment to implement search by CTYPE_LOWER & EMVEDDING
'''class Search2(Resource):
    @use_kwargs({'CTYPE_LOWER': fields.String(missing=''),
                 'EMBEDDING': fields.String(missing=''),
                'page': fields.Int(missing=1),
                'per_page': fields.Int(missing=10)},
                location='query')
    def get(self, CTYPE_LOWER,EMBEDDING, page, per_page):

        results= Embedddings_311.get_all2(CTYPE_LOWER,EMBEDDING,page,per_page)
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
        return res'''




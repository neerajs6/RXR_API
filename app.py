from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db
from models.dob import Dob
from resources.dob import Index, Random, Products, Year, BBL, yearBBL, Dobs


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app,db)

def register_resources(app):
    api = Api(app)

    api.add_resource(Index,'/index')
    api.add_resource(Random, '/rand')
    api.add_resource(Products,'/products/<int:page>')
    api.add_resource(Year, '/year')
    api.add_resource(BBL, '/BBL')
    api.add_resource(yearBBL, '/YearAndBBL')


if __name__ == '__main__':
    app = create_app()
    app.run()

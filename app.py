from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db
from models.dob import Dob

# Dob data
from resources.dob import Year, BBL, yearBBL
from resources.dob_model_data import Dob_Model

# 311 data
from resources.cleaned_311 import Cleaned_311,Cleaned311YearBBL
from resources.embeddings_311 import Embeddings


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

    # cleaned dob resources
    api.add_resource(Year, '/year')
    api.add_resource(BBL, '/BBL')
    api.add_resource(yearBBL, '/YearAndBBL')

    # dob model data
    api.add_resource(Dob_Model,'/dob_model')

    # cleaned 311 resources
    api.add_resource(Cleaned_311,'/311')

    # 311 embeddings resources
    api.add_resource(Embeddings,'/embeddings')

app = create_app()
if __name__ == '__main__':

    app.run()

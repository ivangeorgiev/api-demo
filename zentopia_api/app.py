
import importlib
from flask import Flask
from flask_restplus import Api

def home():
    return "Hello world!"

def create_app():
    # from zentopia_product_api import ns as product_ns

    app = Flask(__name__)

    api = Api(app, version='0.1', title='Zentopia API',
              description='Zentopia backend API')

    app.config.from_object('settings')

    app.add_url_rule('/', endpoint=None, view_func=home)

    from zentopia.db import db
    db.init_app(app)
    app.db = db

    for service_name in set(app.config['SERVICES']):
        service_module = importlib.import_module(service_name)
        api.add_namespace(service_module.ns)

    app.app_context().push()
    app.db.create_all()
    return app

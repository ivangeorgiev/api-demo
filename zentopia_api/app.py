
from flask import Flask
from flask_restplus import Api

def home():
    return "Hello world!"

def create_app():
    from .apis.product import ns as product_ns

    app = Flask(__name__)

    api = Api(app, version='0.1', title='Zentopia API',
              description='Zentopia backend API')

    app.config.from_object('settings')

    app.add_url_rule('/', endpoint=None, view_func=home)

    from .db import db
    db.init_app(app)
    app.db = db

    api.add_namespace(product_ns)

    app.app_context().push()
    app.db.create_all()
    return app

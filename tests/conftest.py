import pytest
from zentopia_api.app import create_app
from zentopia_api.db import Product

@pytest.fixture(scope='function')
def app():
    app = create_app()

    app.app_context().push()
    # Initialise the DB
    # app.db.drop_all()
    app.db.create_all()
    Product.query.delete()

    yield app

@pytest.fixture
def test_app(app):
    banana = Product(name='banana', slug='banana-01', price=100)
    app.db.session.add(banana)
    app.db.session.commit()
    yield app

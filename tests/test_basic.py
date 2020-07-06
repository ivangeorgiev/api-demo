import http.client
from flask_sqlalchemy import SQLAlchemy
from zentopia_api.db import Product

def test_home(client:http.client):
    """Test can read home"""
    response = client.get('/')
    assert response.status_code == 200

def test_db(app):
    """Test application datbase is initialized."""
    assert hasattr(app, 'db')
    assert isinstance(app.db, SQLAlchemy)

def test_product_table_exists(app):
    """Test product table exists"""
    assert Product.query.all() == []

def test_can_insert__retrieve_product(app):
    """Test can insert and retrieve product into/from database"""
    banana_info = { 'name': 'banana', 'slug':'banana-01', 'price': 100}
    banana = Product(**banana_info)
    app.db.session.add(banana)
    app.db.session.commit()

    assert banana.id == 1, "ID is set"
    actual = Product.query.filter(Product.id==1).first()
    assert actual.id == 1, "Retrieved product with correct ID"
    assert actual.name == banana_info['name']

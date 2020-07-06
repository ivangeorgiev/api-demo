import pytest
import http.client
from flask_sqlalchemy import SQLAlchemy
from zentopia import db

class BasicTestItem(db.Model):
    """Test table to be created and used in basic tests."""
    __tablename__ = 'test_items'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False, )


@pytest.fixture
def basic_app(app):
    def basic_test_view():
        return "Hello world!"

    app.db.create_all()
    app.add_url_rule('/basic_test_home', endpoint=None, view_func=basic_test_view)
    yield app

def test_flask_endpoint(basic_app, client):
    """Test can read home"""

    response = client.get('/basic_test_home')
    assert response.status_code == 200

def test_db(app):
    """Test application datbase is initialized."""
    assert hasattr(app, 'db')
    assert isinstance(app.db, SQLAlchemy)

def test_product_table_exists(app):
    """Test product table exists"""
    assert BasicTestItem.query.all() == []

def test_can_insert_retrieve_item(basic_app):
    """Test can insert and retrieve item into/from database"""
    item_info = {'name':'cat'}
    item = BasicTestItem(**item_info)
    basic_app.db.session.add(item)
    basic_app.db.session.commit()

    assert item.id == 1, "ID is set"
    actual = BasicTestItem.query.filter(BasicTestItem.id==1).first()
    assert actual.id == 1, "Retrieved item with correct ID"
    assert actual.name == item_info['name']

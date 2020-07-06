import operator
import pytest
from zentopia_api.products import *

def test_list_products_returns_empty_list(client):
    result = client.get('/product', follow_redirects=True)
    assert result.status_code == 200
    assert result.json == []

def test_list_products_returns_list(test_app, client):
    result = client.get('/product', follow_redirects=True)
    assert result.status_code == 200
    assert len(result.json) >= 1
    assert isinstance(result.json, list)
    sorted_products = sorted(result.json, key=lambda r: r['id'])
    banana = sorted_products[0]
    assert banana['id'] == 1
    assert banana['name'] == 'banana'

def test_create_product(app, client):
    pear_info = {"name":"pear", "slug":"pear01", "price":50}
    result = client.post('/product/', json=pear_info)
    assert result.status_code == 200
    assert result.json['id'] == 1, 'Create product returns product info with ID'
    actual = get_product(1)
    assert actual.name == 'pear', 'Created product is in the database'

def test_api_create_duplicate_product(test_app, client):
    banana_info = {"name":"banana", "slug":"banana02", "price":100}
    result = client.post('/product/', json=banana_info)
    assert result.status_code == 400
    assert result.json['message'] == 'Product name must be unique.'
    

def test_update_existing_product(test_app, client):
    banana_info = {"id":1, "name":"banana updated", "slug":"banana02", "price":100}
    result = client.put('/product/1/', json=banana_info)
    assert result.status_code == 200
    assert result.json['name'] == 'banana updated'
    actual = get_product(1)
    assert actual.name == 'banana updated'

def test_update_missing_product(test_app, client):
    pear_info = {"name":"pear", "slug":"pear01", "price":50}
    result = client.put('/product/200/', json=pear_info)
    assert result.status_code == 404
    assert "id=200 doesn't exist" in result.json['message']

def test_get_existing_product(test_app, client):
    result = client.get('/product/1/')
    assert result.status_code == 200
    assert result.json['name'] == 'banana'

def test_get_missing_product(test_app, client):
    result = client.get('/product/200/')
    assert result.status_code == 404
    assert "id=200 doesn't exist" in result.json['message']

def test_delete_exisitng_product(test_app, client):
    result = client.delete('/product/1/')
    assert result.status_code == 200
    assert result.json['result'] == True
    with pytest.raises(ProductNotFoundError):
        get_product(1)

def test_delete_missing_product(test_app, client):
    result = client.delete('/product/200/')
    assert result.status_code == 404


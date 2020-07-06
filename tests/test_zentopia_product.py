import pytest
from zentopia_product import *
# from zentopia_api.products import *

def test_get_product_throws_error_not_exists(app):
    with pytest.raises(ProductNotFoundError) as excinfo:
        actual = get_product(id=1)
        print(actual)
    assert 'id=1 doesn\'t exist' in str(excinfo.value)

def test_get_product_returns_product_exists(test_app):
    actual = get_product(id=1)
    assert actual.id == 1
    assert actual.name == 'banana'

def test_delete_product_by_id_deletes_existing(test_app):
    assert delete_product(1), "Delete existing product returns True"
    with pytest.raises(ProductNotFoundError) as excinfo:
        actual = get_product(id=1)

def test_delete_product_by_object_deletes_existing(test_app):
    banana = get_product(1)
    assert delete_product(banana), "Delete existing product returns True"
    with pytest.raises(ProductNotFoundError) as excinfo:
        actual = get_product(id=1)

def test_delete_missing_product_raises_error(test_app):
    with pytest.raises(ProductNotFoundError) as exc:
        delete_product(-1) == False


def test_create_product(app):
    pear = Product(name='pear', slug='pear-01', price=50)
    actual = create_product(pear)
    assert isinstance(actual, Product)
    assert actual.id == 1, "ID attribute is set"

    fetched = get_product(1)
    assert fetched.name == 'pear'
    assert fetched.added_at != None, 'Added date/time is set'
    assert fetched.updated_at == None, 'New product is not updated'
    

def test_update_product(test_app):
    banana = get_product(1)
    banana.name = 'Banana Mama'
    result = update_product(banana)
    assert result is banana

    actual = get_product(1)
    assert actual.name == 'Banana Mama', 'Name is updated'
    assert actual.updated_at != None, 'Updated date/time is set'

def test_update_non_existent_product_raises_error(test_app):
    banana = get_product(1)
    delete_product(banana)
    with pytest.raises(Exception) as excinfo:
        update_product(banana)
    assert 'has been deleted' in str(excinfo.value)

def test_list_products(test_app):
    pl = list_products()
    assert isinstance(pl, list)
    assert len(pl) > 0
    pl_sorted = sorted(pl, key=lambda x: x.id)
    actual_product = pl_sorted[0]
    assert actual_product.name == 'banana'

    
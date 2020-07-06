from zentopia import db
from zentopia_product.models import Product
from typing import List

class ProductError(Exception):
    pass

class ProductNotFoundError(Exception):
    pass


def list_products()->List[Product]:
    return Product.query.all()

def get_product(id)->Product:
    product = Product.query.filter(Product.id==id).first()
    if product:
        return product
    raise ProductNotFoundError("Product with id={} doesn't exist.".format(id))

def create_product(product)->Product:
    try:
        db.session.add(product)
        db.session.commit()
        return product
    except Exception as exc:
        try:
            db.session.rollback()
        finally:
            pass
        raise exc

def update_product(product)->Product:
    try:
        db.session.add(product)
        db.session.commit()
    except Exception as excinfo:
        try:
            db.session.rollback()
        finally:
            pass
        raise excinfo
    return product

def delete_product(product)->bool:
    if isinstance(product, Product):
        id = product.id
    elif isinstance(product, int):
        id = product
    else:
        raise TypeError('product must be int or Product not {}'.format(type(product)))

    product = get_product(id)

    try:
        db.session.delete(product)
        db.session.commit()
    except Exception as excinfo:
        try:
            db.session.rollback()
        finally:
            pass
        raise excinfo
    return True

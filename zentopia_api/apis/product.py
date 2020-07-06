from flask import request
from werkzeug.exceptions import BadRequest, NotFound
from flask_restplus import Namespace, Resource, fields
from ..products import *

ns = Namespace('product', 'Product related operations.', path='/product')

product_model = ns.model('ProductRecord', {
    'id': fields.Integer(required=True, description='Product identifier'),
    'name': fields.String(required=True, description='Product name'),
    'slug': fields.String(required=True, description='Product slug'),
    'price': fields.Integer(required=True, description='Product price'),
    'image': fields.String(description='Product image'),
    'added_at': fields.DateTime(description='UTC Date/Time the produce is added'),
    'updated_at': fields.DateTime(description='UTC Date/Time of the last product update'),
})

product_info_model = ns.model('ProductInfo', {
    'name': fields.String(required=True, description='Product name'),
    'slug': fields.String(required=True, description='Product slug'),
    'price': fields.Integer(required=True, description='Product price'),
    'image': fields.String(description='Product image'),
})



@ns.route('/')
class ProductsApi(Resource):
    """Operations on product records list"""
    
    @ns.marshal_list_with(product_model)
    def get(self):
        "List all product records"
        return list_products()

    @ns.expect(product_info_model)
    @ns.marshal_with(product_model)
    def post(self):
        "Create new product record"
        try:
            data = request.json
            product = Product(**data)
            return create_product(product)
        except Exception as exc:
            msg = str(exc)
            if 'UNIQUE constraint failed: products.product_name' in msg:
                msg = 'Product name must be unique.'
            raise BadRequest(msg)

@ns.route('/<int:product_id>/')
class ProductApi(Resource):
    """Operations on product record."""

    @ns.marshal_with(product_model)
    def get(self, product_id):
        "Get product record"
        try:
            product = get_product(product_id)
            return product
        except ProductNotFoundError as exc:
            raise NotFound(str(exc))

    @ns.expect(product_info_model)
    @ns.marshal_with(product_model)
    def put(self, product_id):
        "Update product record"
        data = request.json
        try:
            product = get_product(product_id)
            product.name = data['name']
            product.slug = data['slug']
            product.price = data['price']
            product.image = data.get('image', None)
            return update_product(product)
        except ProductNotFoundError as exc:
            raise NotFound(str(exc))

    def delete(self, product_id):
        "Delete product record"
        try:
            delete_product(product_id)
            return {'result': True}
        except ProductNotFoundError as exc:
            raise NotFound(str(exc))



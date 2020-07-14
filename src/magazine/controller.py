from flask import render_template, Blueprint, request
from src.magazine.model import get_products_list
from bson.json_util import dumps

magazine_app = Blueprint('magazine', __name__, template_folder='views')


@magazine_app.route('/products', methods=['GET'])
def get_products_view():
    return render_template('product_list.html')


@magazine_app.route('/api/v1/products', methods=['GET'])
def get_products_data():
    return dumps(get_products_list())


@magazine_app.route('/api/v1/products/search')
def get_products_by_code():
    sku = request.args.get('sku')
    ean = request.args.get('ean')


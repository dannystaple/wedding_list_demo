from flask import (Blueprint, render_template, abort, jsonify,
    request)
from .models.gifts import GiftList
from .models.products import ProductList

gift_list_bp = Blueprint('gift_list', __name__, 
    template_folder='templates', static_folder='static')

@gift_list_bp.route('/')
def index():
    return render_template('index.html')

@gift_list_bp.route("/add_gift.html")
def add_a_gift():
    return render_template('add_gift.html')


def serialise_product_to_json(prod_bson):
    """Serialise a single product (note - json ready, not json)"""
    json_data = {key: value for key, value in prod_bson.items() if key != "price"}
    json_data['price'] = str(prod_bson['price'])
    return json_data

def serialise_product_list_to_json(prod_items):
    """Serialise a product list (note - json ready, not json)"""
    return [serialise_product_to_json(item) for item in prod_items]


@gift_list_bp.route('/products/')
def products():
    products = ProductList().find()
    return jsonify(serialise_product_list_to_json(products))


def serialise_gift_to_json(gift_bson):
    gift_data = {key: value for key, value in gift_bson.items() if key not in ["price", "_id"]}
    gift_data['product'] = serialise_product_to_json(gift_bson['product'])
    gift_data['_id'] = str(gift_bson['_id'])
    return gift_data

def serialise_gift_list_to_json(gift_items):
    return [serialise_gift_to_json(item) for item in gift_items]


@gift_list_bp.route('/gifts/', methods=['POST', 'GET'])
def gifts():
    gl = GiftList()
    if request.method == 'POST':
        data = request.get_json()
        gl.add(product_id=data['product_id'])

    items = gl.find()
    return jsonify(serialise_gift_list_to_json(items))


@gift_list_bp.route('/gifts/<product_id>/', methods=['DELETE', 'PATCH'])
def modify_gift(product_id):
    gl = GiftList()
    product_id = int(product_id)
    if request.method == 'DELETE':
        gl.remove(product_id)
    if request.method == 'PATCH':
        data = request.get_json()
        if data['purchase']:
            gl.purchase(product_id)
    items = gl.find()
    return jsonify({'result': 'ok'})


@gift_list_bp.route('/gift_report.html')
def gift_report():
    gl = GiftList()
    purchased = gl.find(purchased=True)
    not_purchased = gl.find(purchased=False)
    return render_template('gift_report.html',
        purchased=purchased,
        not_purchased=not_purchased)

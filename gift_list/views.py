from flask import Blueprint, render_template, abort, jsonify
from .models.gifts import GiftList
from .models.products import ProductList

gift_list = Blueprint('gift_list', __name__, 
    template_folder='templates', static_folder='static')

@gift_list.route('/')
def page():
    return render_template('index.html')


def serialise_product_to_json(prod_bson):
    """Serialise a single product (note - json ready, not json)"""
    json_data = {key: value for key, value in prod_bson.items() if key != "price"}
    json_data['price'] = str(prod_bson['price'])
    return json_data

def serialise_product_list_to_json(prod_items):
    """Serialise a product list (note - json ready, not json)"""
    return [serialise_product_to_json(item) for item in prod_items]


@gift_list.route('/products/')
def products():
    products = ProductList().find()
    return jsonify(serialise_product_list_to_json(products))


def serialise_gift_to_json(gift_bson):
    gift_data = {key: value for key, value in gift_bson.items() if key not in ["price", "_id"]}
    gift_data['product'] = serialise_product_to_json(gift_bson['product'])
    gift_data['_id'] = str(gift_bson['_id'])
    return gift_data

def serialist_gift_list_to_json(gift_items):
    return [serialise_gift_to_json(item) for item in gift_items]


@gift_list.route('/gifts/')
def gifts():
    items = GiftList().find()
    return jsonify(serialist_gift_list_to_json(items))

import unittest
import json
from bson.decimal128 import Decimal128
from gift_list import views
from gift_list.models import gifts
from gift_list.models import products
from flask import Flask


class TestProductSerialising(unittest.TestCase):
    def test_serialising_one_product(self):
        """It should output json compatible dict, converting the price"""
        # setup
        product = products.Product.from_bson({
            "_id": 9,
            "name": "Polka Bedding Set, King, Silver",
            "brand": "BEAU LIVING",
            "price": Decimal128("105.00"),
            "in_stock_quantity": 5
        })
        # test
        json_data = views.serialise_product_to_json(product)
        # assert
        self.assertDictContainsSubset(
            {
                "_id": 9,
                "name": "Polka Bedding Set, King, Silver",
                "brand": "BEAU LIVING",
                "price": "105.00",
                "in_stock_quantity": 5
            },
            json_data
        )
    
    def test_serialising_list(self):
        # setup
        product_list = [products.Product.from_bson(item) for item in [
            {
                "_id": 9,
                "name": "Polka Bedding Set, King, Silver",
                "brand": "BEAU LIVING",
                "price": Decimal128("105.00"),
                "in_stock_quantity": 5
            },
            {
                "_id": 8,
                "name": "50's Style Stand Mixer, Black",
                "brand": "SMEG SMALL APPLIANCES",
                "price": Decimal128("449.99"),
                "in_stock_quantity": 1
            }
        ]]
        # test
        json_data = views.serialise_product_list_to_json(product_list)
        # assert
        self.assertEqual(json_data[0]['price'], "105.00")
        self.assertEqual(json_data[1]['price'], "449.99")


class TestProductsView(unittest.TestCase):
    def setUp(self):
        self.maxDiff = 1000
        self.pl = products.ProductList()

    def setup_test_client(self):
        app = Flask(__name__)
        app.register_blueprint(views.gift_list_bp, url_prefix='')
        return app.test_client()

    def test_it_should_list_products(self):
        # setup - products already present
        with self.setup_test_client() as c:
            # test
            response = c.get('/products/')
            # assert
            self.assertEqual(response.status_code, 200, response.data)
            got_json = response.get_json()
            self.assertEqual(len(got_json), 20)
            self.assertEqual(got_json[0]['name'], "Tea pot")
            self.assertEqual(got_json[3]['brand'],"KITCHENAID")
            self.assertEqual(got_json[5]['_id'], 7)
            self.assertEqual(got_json[7]['price'], "105.00")

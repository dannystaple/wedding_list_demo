import unittest
import json

from unittest import mock

from gift_list import views
from gift_list.models import gifts
from gift_list.models import products
from flask import Flask



class TestProductSerialising(unittest.TestCase):
    def test_serialising_one_product(self):
        """It should output json compatible dict, converting the price"""
        # setup
        product=mock.Mock(
            item_id=23,
            brand="Household Goods Ltd",
            price="228.49",
            in_stock_quantity=17
        )
        product.name = "Mixer with bling"
        # test
        json_data = views.serialise_product_to_json(product)
        # assert
        self.assertDictContainsSubset(
            {
                "_id": 23,
                "name": "Mixer with bling",
                "brand": "Household Goods Ltd",
                "price": "228.49",
                "in_stock_quantity": 17
            },
            json_data
        )
    
    def test_serialising_list(self):
        # setup
        product_1 = mock.Mock(
            item_id=5,
            brand="Shiny Things Co",
            price="28.95",
            in_stock_quantity=42
        )
        product_1.name = "Sparkly wedding thing"
        product_2 = mock.Mock(
            item_id=23,
            brand="Household Goods Ltd",
            price="228.49",
            in_stock_quantity=17
        )
        product_2.name = "Mixer with bling"
        product_list = [product_1, product_2]
        # test
        json_data = views.serialise_product_list_to_json(product_list)
        # assert
        self.assertEqual(json_data[0]['price'], "28.95")
        self.assertEqual(json_data[1]['price'], "228.49")


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

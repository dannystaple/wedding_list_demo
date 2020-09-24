import unittest
import json
from bson.decimal128 import Decimal128
from gift_list import views


class TestProductSerialising(unittest.TestCase):
    def test_serialising_one_product(self):
        """It should output json compatible dict, converting the price"""
        # setup
        product = {
            "_id": 9,
            "name": "Polka Bedding Set, King, Silver",
            "brand": "BEAU LIVING",
            "price": Decimal128("105.00"),
            "in_stock_quantity": 5
        }
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
        products = [
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
        ]
        # test
        json_data = views.serialise_product_list_to_json(products)
        # assert
        self.assertEqual(json_data[0]['price'], "105.00")
        self.assertEqual(json_data[1]['price'], "449.99")

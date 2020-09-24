import unittest
import json
from bson.decimal128 import Decimal128
from bson.objectid import ObjectId
from gift_list import views

class TestGiftSerialising(unittest.TestCase):
    def test_serialising_one_gift(self):
        """It should outp[ut json compatible dict with the product"""
        # setup
        product = {
            "_id": 9,
            "name": "Polka Bedding Set, King, Silver",
            "brand": "BEAU LIVING",
            "price": Decimal128("105.00"),
            "in_stock_quantity": 5
        }
        gift = {
            "_id": ObjectId(),
            "product": product,
            "purchased": False
        }
        # test
        gift_data = views.serialise_gift_to_json(gift)
        # assert
        self.assertDictEqual(
            gift_data,
            {
                "_id": str(gift['_id']),
                "product": {
                    "_id": 9,
                    "name": "Polka Bedding Set, King, Silver",
                    "brand": "BEAU LIVING",
                    "price": "105.00",
                    "in_stock_quantity": 5
                },
                "purchased": False
            }
        )

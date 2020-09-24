import unittest
import json
from bson.decimal128 import Decimal128
from bson.objectid import ObjectId
from gift_list import views
from gift_list.models import gifts
from flask import Flask


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


class TestGiftsView(unittest.TestCase):
    def setUp(self):
        self.maxDiff = 1000
        self.gl = gifts.GiftList()
        self.gl.col.drop()

    def tearDown(self):
        self.gl.col.drop()

    def setup_test_client(self):
        app = Flask(__name__)
        app.register_blueprint(views.gift_list_bp, url_prefix='')
        return app.test_client()

    def test_it_should_get_gifts_list(self):
        # Setup - Add a few gifts
        self.gl.add(product_id=9)
        self.gl.add(product_id=13)
        self.gl.add(product_id=19)
        # Test - Now retrieve with test client
        with self.setup_test_client() as c:
            response = c.get('/gifts/')
            got_json = response.get_json()
            # assert - did we get something reasonable?
            self.assertEqual(len(got_json), 3)
            self.assertEqual(
                got_json[0]['product']['name'], "Polka Bedding Set, King, Silver"
            )
            self.assertEqual(
                got_json[1]['product']['name'], "Falcon T2 Square Parasol, 2.7m, Taupe"
            )
            self.assertEqual(
                got_json[2]['product']['name'], "Sea Green Honeycomb Glass Lamp"
            )

    def test_it_should_be_able_to_add_gift_by_posting(self):
        # Setup - Add a few gifts
        self.gl.add(product_id=9)
        self.gl.add(product_id=13)
        new_product = 15
        # Test - make the post
        with self.setup_test_client() as c:
            response = c.post('/gifts/', json={
                'product_id': new_product
            })
            self.assertEqual(response.status_code, 200, response.data)
            # Assert
            gifts = list(self.gl.find())
            self.assertEqual(len(gifts), 3)
            self.assertEqual(gifts[-1]['product']['_id'], 15)

    def test_it_should_be_able_to_remove_a_gift_with_delete(self):
        self.gl.add(product_id=9)
        self.gl.add(product_id=13)
        # test - make the delete request
        with self.setup_test_client() as c:
            #   delete by the product ID
            response = c.delete('/gifts/13/')
            self.assertEqual(response.status_code, 200, response.data)
            # Assert
            gifts = list(self.gl.find())
            self.assertEqual(len(gifts), 1)

    def test_it_should_be_able_to_buy_a_product_with_patch(self):
        self.gl.add(product_id=9)
        self.gl.add(product_id=13)
        # test - make the patch purchsae request
        with self.setup_test_client() as c:
            # patch the product
            response = c.patch('/gifts/13/', json={
                'purchase': True
            })
            self.assertEqual(response.status_code, 200, response.data)
            # Assert
            gifts = list(self.gl.find())
            self.assertTrue(gifts[1]['purchased'])

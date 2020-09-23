import unittest
from bson.decimal128 import Decimal128
from gift_list.models.products import ProductList
from gift_list.models.gifts import GiftList

class TestGiftList(unittest.TestCase):
    def setUp(self):
        self.gl = GiftList()
        self.gl.col.drop()

    def tearDown(self):
        self.gl.col.drop()


    def test_it_should_add_a_gift_to_the_list(self):
        """With an empty gift list,
        we should be able to add 1.
        and show the count is 1.
        """
        # setup 
        pl = ProductList()
        prod = pl.get(9)
        # test
        self.gl.add(product_id=9)
        # assert
        self.assertEqual(self.gl.count, 1)

    def test_list_added_gifts(self):
        # setup 
        pl = ProductList()
        prod = pl.get(9)
        #   Add a few gifts
        self.gl.add(product_id=9)
        self.gl.add(product_id=13)
        self.gl.add(product_id=19)
        # Test - get this list
        gifts = list(self.gl.find())
        self.assertListEqual(
            gifts,
            [
                {
                    "_id": 0,
                    "product": {
                        "_id": 9,
                        "name": "Polka Bedding Set, King, Silver",
                        "brand": "BEAU LIVING",
                        "price": Decimal128("105.00"),
                        "in_stock_quantity": 5
                    },
                    "purchased": False
                },
                {
                    "_id": 1,
                    "product": {
                        "_id": 13,
                        "name": "Falcon T2 Square Parasol, 2.7m, Taupe",
                        "brand": "GARDENSTORE",
                        "price": Decimal128("344.99"),
                        "in_stock_quantity": 5
                    },
                    "purchased": False
                },
                {
                    "_id": 2,
                    "product": {
                        "_id": 19,
                        "name": "Sea Green Honeycomb Glass Lamp",
                        "brand": "GRAHAM & GREEN",
                        "price": Decimal128("95.00"),
                        "in_stock_quantity": 4
                    },
                    "purchased": False
                }
            ]
        )

    
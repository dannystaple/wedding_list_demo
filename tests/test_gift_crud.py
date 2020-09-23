import unittest
from bson.decimal128 import Decimal128
from gift_list.models.gifts import GiftList, GiftAddedTwiceError, GiftNotInListError

class TestGiftList(unittest.TestCase):
    def setUp(self):
        self.maxDiff = 1000
        self.gl = GiftList()
        self.gl.col.drop()

    def tearDown(self):
        self.gl.col.drop()

    def test_it_should_add_a_gift_to_the_list(self):
        """With an empty gift list,
        we should be able to add 1.
        and show the count is 1.
        """
        # test
        self.gl.add(product_id=9)
        # assert
        self.assertEqual(self.gl.count, 1)

    def test_it_should_reject_a_gift_already_added(self):
        # test
        self.gl.add(product_id=15)
        with self.assertRaises(GiftAddedTwiceError):
            self.gl.add(product_id=15)

    def add_test_gifts(self):
        #   Add a few gifts
        self.id1=self.gl.add(product_id=9)
        self.id2=self.gl.add(product_id=13)
        self.id3=self.gl.add(product_id=19)

    def test_buying_a_gift_in_list_should_set_flag(self):
        # Setup
        self.add_test_gifts()
        # Test

        self.gl.purchase(13)
        # Assert


    def test_list_added_gifts(self):

        #   Add a few gifts
        self.add_test_gifts()
        # Test - get this list
        gifts = list(self.gl.find())
        self.assertListEqual(
            gifts,
            [
                {
                    "_id": self.id1,
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
                    "_id": self.id2,
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
                    "_id": self.id3,
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

    def test_buying_a_gift_in_list_should_set_flag(self):
        # Setup
        self.add_test_gifts()
        # Test

        self.gl.purchase(13)
        # Assert
        gifts = list(self.gl.find())
        self.assertDictEqual(
            gifts[1],
            {
                "_id": self.id2,
                "product": {
                    "_id": 13,
                    "name": "Falcon T2 Square Parasol, 2.7m, Taupe",
                    "brand": "GARDENSTORE",
                    "price": Decimal128("344.99"),
                    "in_stock_quantity": 5
                },
                "purchased": True
            },
        )

    def test_it_should_reject_buying_a_gift_not_in_list(self):
        # Setup
        self.add_test_gifts()
        # Test
        with self.assertRaises(GiftNotInListError):
            self.gl.purchase(17)
        
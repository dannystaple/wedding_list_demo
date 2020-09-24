import unittest

import mongo_mock_helper

from gift_list.models.gifts import GiftList, GiftAddedTwiceError, GiftNotInListError, GiftAlreadyPurchasedError


class TestGiftList(unittest.TestCase):
    def setUp(self):
        self.db, _ = mongo_mock_helper.get_mongo_mock_with_populated_products()

        self.gifts_collection = self.db['gifts']
        self.maxDiff = 1000
        self.gl = GiftList(self.db)

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


    def test_list_added_gifts(self):

        #   Add a few gifts
        self.add_test_gifts()
        # Test - get this list
        gifts = list(self.gl.find())
        self.assertEqual(len(gifts), 3)
        self.assertEqual(gifts[0].item_id, str(self.id1))
        self.assertEqual(gifts[0].product.name, "Polka Bedding Set, King, Silver")
        self.assertEqual(gifts[0].product.brand, "BEAU LIVING")
        self.assertEqual(gifts[0].product.price, "105.00")
        self.assertEqual(gifts[0].product.in_stock_quantity, 5)
        self.assertEqual(gifts[0].product.item_id, 9)
        self.assertEqual(gifts[1].product.item_id, 13)
        self.assertEqual(gifts[2].product.item_id, 19)

    def test_buying_a_gift_in_list_should_set_flag(self):
        # Setup
        self.add_test_gifts()
        # Test

        self.gl.purchase(13)
        # Assert
        gifts = list(self.gl.find())
        self.assertEqual(gifts[1].product.item_id, 13)
        self.assertTrue(gifts[1].purchased)

    def test_it_should_reject_buying_a_gift_not_in_list(self):
        # Setup
        self.add_test_gifts()
        # Test
        with self.assertRaises(GiftNotInListError):
            self.gl.purchase(17)
    
    def test_it_should_reject_buying_a_gift_twice(self):
        # setup
        self.add_test_gifts()
        self.gl.purchase(13)
        # test
        with self.assertRaises(GiftAlreadyPurchasedError):
            self.gl.purchase(13)

    def test_it_should_filter_by_purchased_gifts(self):
        # setup
        self.add_test_gifts()
        self.gl.add(17)
        # test
        self.gl.purchase(13)
        self.gl.purchase(17)
        # assert
        gifts = list(self.gl.find(purchased=True))
        self.assertEqual(len(gifts), 2)
        self.assertEqual(gifts[0].product.item_id, 13)
        self.assertTrue(gifts[0].purchased)
        self.assertEqual(gifts[1].product.item_id, 17)
        self.assertTrue(gifts[1].purchased)

    def test_it_should_filter_by_not_purchased_gifts(self):
        # setup
        self.add_test_gifts()
        self.gl.add(17)
        # test
        self.gl.purchase(13)
        self.gl.purchase(17)
        # assert
        gifts = list(self.gl.find(purchased=False))
        self.assertEqual(len(gifts), 2)
        self.assertEqual(gifts[0].product.item_id, 9)
        self.assertFalse(gifts[0].purchased)
        self.assertEqual(gifts[1].product.item_id, 19)
        self.assertFalse(gifts[1].purchased)

    def test_removing_a_gift_from_a_list(self):
        # setup
        self.add_test_gifts()
        # test
        self.gl.remove(19)
        # assert
        gifts = list(self.gl.find())
        self.assertEqual(len(gifts), 2)
        self.assertEqual(gifts[0].product.item_id, 9)
        self.assertEqual(gifts[1].product.item_id, 13)

    def test_removing_something_already_removed_should_raise_error(self):
        # test
        with self.assertRaises(GiftNotInListError):
            self.gl.remove(17)

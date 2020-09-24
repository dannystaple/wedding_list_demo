import unittest

import mongo_mock_helper

from gift_list.models.products import ProductList


class TestProductList(unittest.TestCase):
    """Don't need to test add, just look up"""
    def setUp(self):
        self.db, self.prod_collection = mongo_mock_helper.get_mongo_mock_with_populated_products()

    def test_finding_product_by_id(self):
        pl = ProductList(self.db)
        product = pl.get(9)
        self.assertEqual(product.name, "Polka Bedding Set, King, Silver")
        self.assertEqual(product.item_id, 9)
        self.assertEqual(product.brand, "BEAU LIVING")
        self.assertEqual(product.price, "105.00")
        self.assertEqual(product.in_stock_quantity, 5)

    def test_finding_by_text_product(self):
        """We shouldn't make customer choose brand, 
        or product - just text that may be either"""
        pl = ProductList(self.db)
        products = pl.find(text="Bedd")
        as_list = list(products)
        self.assertEqual(len(as_list), 2)
        self.assertEqual(as_list[0].name, "Polka Bedding Set, King, Silver")
        self.assertEqual(as_list[0].item_id, 9)
        self.assertEqual(as_list[0].brand, "BEAU LIVING")
        self.assertEqual(as_list[0].price, "105.00")
        self.assertEqual(as_list[0].in_stock_quantity, 5)

    def test_finding_products_by_text_brand(self):
        pl = ProductList(self.db)
        products = pl.find(text='SME')
        as_list = list(products)
        self.assertEqual(len(as_list), 2)
        self.assertEqual(as_list[0].name, "50's Style Stand Mixer, Full-Colour White")
        self.assertEqual(as_list[0].item_id, 7)
        self.assertEqual(as_list[0].brand, "SMEG SMALL APPLIANCES")
        self.assertEqual(as_list[0].price, "449.00")
        self.assertEqual(as_list[0].in_stock_quantity, 0)

    def test_show_all(self):
        pl = ProductList(self.db)
        products = pl.find()
        as_list = list(products)
        self.assertEqual(len(as_list), 20)

    def test_filtering_by_in_stock(self):
        pl = ProductList(self.db)
        products = pl.find(in_stock=True)
        as_list = list(products)
        self.assertEqual(len(as_list), 16)

    def test_combine_text_and_in_stock(self):
        pl = ProductList(self.db)
        products = pl.find(text="SME", in_stock=True)
        as_list = list(products)
        self.assertEqual(len(as_list), 1)
        self.assertEqual(as_list[0].name, "50's Style Stand Mixer, Black")
        self.assertEqual(as_list[0].item_id, 8)
        self.assertEqual(as_list[0].brand, "SMEG SMALL APPLIANCES")
        self.assertEqual(as_list[0].price, "449.99")
        self.assertEqual(as_list[0].in_stock_quantity, 1)

    # Skipping these - not required currently, and mongomock does not support lt/gt and Decimal128 types.
    # def test_price_less_than(self):
    #     pl = ProductList(self.db)
    #     products = pl.find(price_lt=100)
    #     as_list = list(products)
    #     self.assertEqual(len(as_list), 9)

    # def test_price_greater_than(self):
    #     pl = ProductList(self.db)
    #     products = pl.find(price_gt=150)
    #     as_list = list(products)
    #     self.assertEqual(len(as_list), 8)

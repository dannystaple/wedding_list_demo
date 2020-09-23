import unittest
from bson.decimal128 import Decimal128
from gift_list.models.products import ProductList

class TestProductList(unittest.TestCase):
    """Don't need to test add, just look up"""
    def test_finding_product_by_id(self):
        pl = ProductList()
        product = pl.get(9)
        self.assertEqual(product['name'], "Polka Bedding Set, King, Silver")
        self.assertDictContainsSubset(
            {
                "_id": 9,
                "name": "Polka Bedding Set, King, Silver",
                "brand": "BEAU LIVING",
                "price": Decimal128("105.00"),
                "in_stock_quantity": 5
            },
            product
        )

    def test_finding_by_text_product(self):
        """We shouldn't make customer choose brand, 
        or product - just text that may be either"""
        pl = ProductList()
        products = pl.find(text="Bedd")
        as_list = list(products)
        self.assertEqual(len(as_list), 2)
        self.assertDictContainsSubset(
            {
                "_id": 9,
                "name": "Polka Bedding Set, King, Silver",
                "brand": "BEAU LIVING",
                "price": Decimal128("105.00"),
                "in_stock_quantity": 5
            },
            as_list[0]
        )

    def test_finding_products_by_text_brand(self):
        pl = ProductList()
        products = pl.find(text='SME')
        as_list = list(products)
        self.assertEqual(len(as_list), 2)
        self.assertDictContainsSubset(
            {
                "_id": 7,
                "name": "50's Style Stand Mixer, Full-Colour White",
                "brand": "SMEG SMALL APPLIANCES",
                "price": Decimal128("449.00"),
                "in_stock_quantity": 0
            },
            as_list[0]
        )

    def test_show_all(self):
        pl = ProductList()
        products = pl.find()
        as_list = list(products)
        self.assertEqual(len(as_list), 20)

    def test_filtering_by_in_stock(self):
        pl = ProductList()
        products = pl.find(in_stock=True)
        as_list = list(products)
        self.assertEqual(len(as_list), 16)

    def test_combine_text_and_in_stock(self):
        pl = ProductList()
        products = pl.find(text="SME", in_stock=True)
        as_list = list(products)
        self.assertEqual(len(as_list), 1)
        self.assertDictContainsSubset(
            {
                "_id": 8,
                "name": "50's Style Stand Mixer, Black",
                "brand": "SMEG SMALL APPLIANCES",
                "price": Decimal128("449.99"),
                "in_stock_quantity": 1
            },
            as_list[0]
        )

    def test_price_less_than(self):
        pl = ProductList()
        products = pl.find(price_lt=100)
        as_list = list(products)
        self.assertEqual(len(as_list), 9)

    def test_price_greater_than(self):
        pl = ProductList()
        products = pl.find(price_gt=150)
        as_list = list(products)
        self.assertEqual(len(as_list), 8)
        


import unittest
from models.products import ProductList

class TestGiftList(unittest.TestCase):
    """Don't need to test add, just look up"""
    def test_finding_product_by_id(self):
        product = ProductList.get(prod_id=9)
        self.assertEqual(product['name'], "Polka Bedding Set, King, Silver")
        self.assertDictContainsSubset(
            {
                "id": 9,
                "name": "Polka Bedding Set, King, Silver",
                "brand": "BEAU LIVING",
                "price": "105.00GBP",
                "in_stock_quantity": 5
            },
            product
        )
    
    def test_finding_products_by_partial_name(self):
        products = ProductList.find(name_contains="Bedd")
        self.assertEqual(len(products), 2)
        self.assertDictContainsSubset(
            {
                "id": 9,
                "name": "Polka Bedding Set, King, Silver",
                "brand": "BEAU LIVING",
                "price": "105.00GBP",
                "in_stock_quantity": 5
            },
            products[0]
        )

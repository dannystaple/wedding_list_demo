"""Designed for one shot product import."""
import json


import sys
import bson
from ..models.products import ProductList
from ..models import settings

def import_products(products_file, db):
    pl = ProductList(db).col
    pl.drop()
    pl = ProductList(db).col

    with open(products_file) as fd:
        data = json.load(fd)
        for product in data:
            product['_id'] = product['id']
            del product['id']
            product['currency'] = 'GBP'
            product['price'] = bson.Decimal128(product['price'].replace('GBP', ''))
            pl.insert_one(product)

if __name__ == "__main__":
    import_products(sys.argv[1], settings.get_db_connection())

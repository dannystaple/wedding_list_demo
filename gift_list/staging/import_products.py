"""Designed for one shot product import."""
import json


import sys
import bson
from ..models.products import ProductList

def main(products_file):
    pl = ProductList().col
    pl.drop()
    pl = ProductList().col

    with open(products_file) as fd:
        data = json.load(fd)
        for product in data:
            product['_id'] = product['id']
            del product['id']
            product['currency'] = 'GBP'
            product['price'] = bson.Decimal128(product['price'].replace('GBP', ''))
            pl.insert_one(product)

if __name__ == "__main__":
    main(sys.argv[1])

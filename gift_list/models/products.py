from bson.decimal128 import Decimal128


class Product():
    @staticmethod
    def from_bson(bson_data):
        new_item = Product()
        new_item.bson = bson_data
        return new_item

    @property
    def name(self):
        return self.bson['name']

    @property
    def brand(self):
        return self.bson['brand']

    @property
    def price(self):
        return str(self.bson['price'])

    @property
    def in_stock_quantity(self):
        return self.bson['in_stock_quantity']

    @property
    def item_id(self):
        return self.bson['_id']


class ProductList:
    def __init__(self, db):
        self.col = db['products']

    def get(self, _id):
        return Product.from_bson(self.col.find_one({'_id': _id}))

    def find(self, text='', in_stock=None, price_lt=None,
            price_gt=None):
        filter = {}
        if text:
            filter['$or'] = [
                {'brand': {"$regex": f".*{text}.*"}},
                {'name': {"$regex": f".*{text}.*"}}
            ]
        if in_stock:
            filter['in_stock_quantity'] = {'$gt': 0}
        if price_lt is not None:
            lt_value = Decimal128(str(price_lt))
            filter['price'] = {'$lt': lt_value}
        if price_gt is not None:
            gt_value = Decimal128(str(price_gt))
            filter['price'] = {'$gt': gt_value}
        return (Product.from_bson(item) for item in self.col.find(filter))

from bson.decimal128 import Decimal128
from . import settings

class ProductList:
    def __init__(self):
        db = settings.get_db_connection()
        self.col = db['products']

    def get(self, _id):
        return self.col.find_one({'_id': _id})

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
        return self.col.find(filter)

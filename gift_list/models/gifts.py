from . import settings
from .products import Product

class GiftAddedTwiceError(RuntimeError):
    pass


class GiftNotInListError(RuntimeError):
    pass


class GiftAlreadyPurchasedError(RuntimeError):
    pass

class Gift():
    product: Product

    @staticmethod
    def from_bson(bson_data):
        new_item = Gift()
        new_item.bson = bson_data
        new_item.product = Product.from_bson(bson_data['product'])
        return new_item

    @property
    def purchased(self) -> str:
        return self.bson['purchased']

    @property
    def item_id(self) -> str:
        return str(self.bson['_id'])


class GiftList:
    def __init__(self):
        db = settings.get_db_connection()
        self.col = db['gifts']

    def add(self, product_id):
        if self.col.count_documents({'product_id':product_id}):
            raise GiftAddedTwiceError(product_id)
        return self.col.insert_one(
            {
                'product_id' :product_id, 
                'purchased': False
            }
        ).inserted_id

    def remove(self, product_id):
        if self.col.count_documents({'product_id':product_id}) == 0:
            raise GiftNotInListError(product_id)
        
        self.col.delete_one({'product_id': product_id})
    
    def purchase(self, product_id):
        if self.col.count_documents({'product_id':product_id}) == 0:
            raise GiftNotInListError(product_id)
        if self.col.count_documents({
              'product_id':product_id,
              'purchased': True}) == 1:
            raise GiftAlreadyPurchasedError(product_id)
        query = {'product_id': product_id}
        update = {'$set': {'purchased': True}}
        self.col.update_one(query, update)

    @property
    def count(self):
        return self.col.count_documents({})

    def find(self, purchased=None):
        pipeline = []
        if purchased is not None:
            pipeline.append({
                '$match': {'purchased': purchased}
            })
        pipeline.extend([
            {
                '$lookup': {
                    'from': 'products',
                    'localField': 'product_id',
                    'foreignField': '_id',
                    'as': 'product'
                },
                
            },
            {"$unwind": "$product"},
            { "$project": {
                    "product": {
                        "currency": 0,
                    },
                    "product_id": 0
            }}
        ])
        return (Gift.from_bson(item) for item in self.col.aggregate(pipeline))

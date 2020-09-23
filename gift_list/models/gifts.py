from . import settings

class GiftList:
    def __init__(self):
        db = settings.get_db_connection()
        self.col = db['gifts']

    def add(self, product_id):
        self.col.insert_one(
            {
                'product' :'product_id', 
                'purchased': False
            }
        )
    
    @property
    def count(self):
        return self.col.count()

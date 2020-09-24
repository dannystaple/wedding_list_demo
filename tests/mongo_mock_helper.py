import mongomock
from gift_list.staging import import_products


def get_mongo_mock_with_populated_products():
    """Helper to set up a mock mongoDB, and then populate with products"""
    db = mongomock.MongoClient().db
    prod_collection = db['products']
    import_products.import_products('products.json', db)

    return db, prod_collection
import os

import pymongo

def get_db_connection():
    connection  = pymongo.MongoClient(os.getenv('DB'))
    return connection['gift_lists']

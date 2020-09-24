import os

import pymongo

def get_db_connection():
    connection = pymongo.MongoClient(os.getenv('DB', 'mongodb://testsrv/'))
    return connection[os.getenv('DB_NAME', 'test')]

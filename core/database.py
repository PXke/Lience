
from pymongo import MongoClient


def connect(address=None):
    if address:
        client = MongoClient(address)
    else:
        client = MongoClient()

    return client


def kill():
    db.close()

db = connect()
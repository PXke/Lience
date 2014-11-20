from pymongo import MongoClient
from pymongo.son_manipulator import ObjectId
from copy import deepcopy

def connect(address=None):
    if address:
        client = MongoClient(address)
    else:
        client = MongoClient()
    return client


def kill():
    db.close()


db = connect()["Lience"]


class BaseModel():
    """Base model for mongodb interfacing"""

    def __init__(self, tree):
        """Init the BaseModel class.

        :param tree: tree of collection
        :type tree: list

        :var table: table is a direct connector to the collection
        it is the one used for every operation function.
        """
        connector = db
        if isinstance(tree, list):
            for collection in tree:
                connector = connector[collection]
        else:
            connector = connector[tree]
        self.table = connector
        self.attributs = {}

    def add_by_attributs(self, attributs_param):
        new_object = deepcopy(self.attributs)
        for attribut in attributs_param:
            new_object[attribut] = attributs_param[attribut]
        

    def get_all(self):
        return self.table.find()

    def get_by_id(self, id):
        if isinstance(id, ObjectId):
            return self.table.find({"_id": id})
        else:
            return self.table.find({"_id": ObjectId(id)})

    def remove_by_id(self, id):
        if isinstance(id, ObjectId):
            return self.table.remove({"_id": id})
        else:
            return self.table.remove({"_id": ObjectId(id)})

    def update_representation(self, new, old):
        if not isinstance(new, dict):
            raise Exception("keys or udpates not a dict")
        if isinstance(old, dict):
            try:
                temp_id = old["_id"]
            except KeyError:
                raise Exception("No id in record")
            if not isinstance(temp_id, ObjectId):
                temp_id = ObjectId(temp_id)
            old["_id"] = temp_id

        else:
            temp_id = old
            if not isinstance(temp_id, ObjectId):
                temp_id = ObjectId(temp_id)
            old = {"_id": temp_id}

        self.table.update(old, {"$set": new})
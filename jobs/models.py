from ..core.database import db

# FIXME: Highly prototypical

class Job(object):
    def __init__(self):
        self.attributes = {"_id": "",
                           "name": "",
                           "description": "",
                           "organization": "",
                           "candidates": []
        }

    def __getitem__(self, item):
        return self.attributes[item]

    def __setitem__(self, key, value):
        self.attributes[key] = value

    def save(self):
        if not self["_id"]:
            self["_id"] = db["Lience"]["modules"]["jobs"].insert(
                self.attributes)
        else:
            self.update()

    def load_one(self, **kwargs):
        request = {}
        for key, value in kwargs:
            request[key] = value
        results = db["Lience"]["modules"]["jobs"].find(request)
        try:
            result = results[0]
            self.attributes = result
        except IndexError:
            return None

    def load_several(self, **kwargs):
        request = {}
        for key, value in kwargs:
            request[key] = value
        return list(db["Lience"]["modules"]["jobs"].find(request))

    def update(self):
        db["Lience"]["modules"]["jobs"].update({'_id': self["_id"]},
                                               self.attributes)


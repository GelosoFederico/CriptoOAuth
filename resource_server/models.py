import json

class User:
    def __init__(self, id, name, is_admin, pets=None):
        self.id = id
        self.name = name
        self.is_admin = is_admin
        self.pets = pets

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

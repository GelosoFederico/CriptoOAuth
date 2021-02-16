import json

class User:
    def __init__(self,id,nombre,is_admin):
        self.id = id
        self.nombre = nombre
        self.is_admin = is_admin

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

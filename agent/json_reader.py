import json
class JsonReader:
    @staticmethod
    def read(path):
        with open(path,"r") as file:
            return json.load(file)

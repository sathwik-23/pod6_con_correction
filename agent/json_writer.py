import json
class JsonWriter:

    @staticmethod
    def write(path, config):

        with open(path, "w") as file:
            json.dump(config, file, indent=4)
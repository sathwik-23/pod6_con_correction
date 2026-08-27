class ConfigValidator:

    @staticmethod
    def validate(config,actions):

        for action in actions:

            keys = action["parameter"].split(".")

            current = config

            for key in keys:
                current = current[key]

            if current != action["new_value"]:
                return False

        return True
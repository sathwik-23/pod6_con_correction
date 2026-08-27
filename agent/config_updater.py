class ConfigUpdater:

    @staticmethod
    def update_value(config, parameter, value):

        keys = parameter.split(".")

        current = config

        for key in keys[:-1]:

            if key not in current:
                raise KeyError(f"{key} not found")

            current = current[key]

        current[keys[-1]] = value

        return config
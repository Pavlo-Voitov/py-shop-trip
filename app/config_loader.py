import json
import os


def load_config() -> json:
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, "r") as file:
        return json.load(file)

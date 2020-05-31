import json


def read_config():
  with open("config.json") as f:
    config = json.load(f)
    return config


def write_config(config):
  with open("config.json", "w") as f:
    json.dump(config, f, indent=2)

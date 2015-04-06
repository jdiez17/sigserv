import yaml

def load_config(path):
    with open(path) as f:
        cfg = yaml.load(f.read())
        # TODO: Complain if sections of the thing are missing

    return cfg

config = load_config("config.yml")

import os
import yaml

def load_config(file_path):
    base_path = os.path.dirname(__file__)
    abs_path = os.path.join(base_path, file_path)
    with open(abs_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
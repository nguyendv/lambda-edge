"""
cli.config
~~~~~~~~~~~~

This module implements interface for getting and setting the "ledge" cli application's configuration.
The configuration is stored in the .config.yaml file
"""

import yaml
from pathlib import PosixPath

config_file = PosixPath('.config.yaml')
if not config_file.exists():
    config_file.touch()

def get(key):
    """Get the config value by providing the key"""
    with config_file.open('r') as f:
        conf = yaml.load(f)
        return conf.get(key)
    return None

def set(key, value):
    """Set a config by providine a key-value pair"""
    with config_file.open('r') as f:
        conf = yaml.load(f)
        if conf is None:
            conf = dict()

    with config_file.open('w') as f:
        conf[key] = value
        yaml.dump(conf, f)

def delete(key):
    """Delete a config key"""
    with config_file.open('r') as f:
        conf = yaml.load(f)

    with config_file.open('w') as f:
        conf.pop(key)
        yaml.dump(conf, f)

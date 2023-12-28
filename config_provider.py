# File name: config_provider.py
# Created on: 12/28/2023
# Created by: Oleg Gordiushenkov

import yaml

def read_config(config_fn):
    try:
        with open(config_fn, "r") as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
            return config
    except Exception as exc:
        print(exc)
    return dict()

if __name__ == '__main__':
    config = read_config('config.yml')
    print(config)
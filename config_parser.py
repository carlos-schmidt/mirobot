import configparser

config = configparser.ConfigParser()


def get_config_values(file='./config.cfg', section='DEFAULT'):
    config.read(file)
    if section in config:
        return config[section]
    else: raise FileNotFoundError("section not found in file")  # returns first element in cfg

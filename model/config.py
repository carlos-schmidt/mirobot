class Config:
    def __init__(self, file: str, section: str) -> None:
        """Initialize config object with file path and section.

        Args:
            file (str): Path to file. Example: '/home/env/miro-config.cfg'
            section (str): Which section of the config to use. In config: [SECTION]
        """
        config_dict = _get_config_values(file, section)
        print(config_dict)
        self.opcua_server_url = config_dict['opcua_server_url']
        self.opcua_request_timeout = config_dict['opcua_request_timeout']
        self.mirobot_portname = config_dict['mirobot_portname']
        self.mirobot_debug = config_dict['mirobot_debug']

    def get_opcua_server_url(self):
        return self.opcua_server_url

    def get_opcua_request_timeout(self):
        return self.opcua_request_timeout

    def get_mirobot_portname(self):
        return self.mirobot_portname

    def get_mirobot_debug(self):
        return self.mirobot_debug


def _get_config_values(file='./config.cfg', section='DEFAULT'):
    from configparser import ConfigParser
    config = ConfigParser()

    config.read(file)
    if section in config:
        return config[section]
    else:
        # returns first element in cfg
        raise FileNotFoundError("section not found in file")

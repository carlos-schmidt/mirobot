class Config:
    def __init__(self, file: str, section: str) -> None:
        """Initialize config object with file path and section.

        Args:
            file (str): Path to file. Example: '/home/env/miro-config.cfg'
            section (str): Which section of the config to use. In config: [SECTION]
        """
        config_dict = _get_config_values(file, section)
        print(config_dict)

        self.opcua_server_url = config_dict["opcua_server_url"]

        # For each topic, a value should be given where the mirobot shall trigger
        self.opcua_topics: list() = config_dict["opcua_topics"]
        self.opcua_values: list() = config_dict["opcua_values"]
        self.opcua_routines: list() = config_dict["opcua_routines"]
        assert len(self.opcua_topics) == len(self.opcua_values) and\
        len(self.opcua_values) == len(self.opcua_routines)

        self.opcua_polling_rate = config_dict["opcua_polling_rate"]
        self.opcua_request_timeout = config_dict["opcua_request_timeout"]
        
        self.mirobot_portname = config_dict["mirobot_portname"]
        self.mirobot_debug = bool(config_dict["mirobot_debug"])
        
        self.mirobot_destination_position = config_dict["mirobot_source_position"]
        self.mirobot_destination_position = config_dict["mirobot_destination_position"]
        self.mirobot_store_positions = config_dict["mirobot_store_positions"]
        
        


def _get_config_values(file="./config.cfg", section="DEFAULT"):
    from configparser import ConfigParser

    config = ConfigParser()

    config.read(file)
    if section in config:
        return config[section]
    else:
        # returns first element in cfg
        raise FileNotFoundError("section not found in file")

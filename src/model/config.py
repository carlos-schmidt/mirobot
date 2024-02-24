import ast


class Config:
    def __init__(self, file: str, section: str) -> None:
        """Initialize config object with file path and section.

        Args:
            file (str): Path to file. Example: '/home/env/miro-config.cfg'
            section (str): Which section of the config to use. In config: [SECTION]
        """
        config_dict = _get_config_values(file, section)
        print(config_dict)

        # ROBO ENV
        self.stored_items_initial = config_dict["stored_items_initial"]

        self.conveyor_belt_output_location = ast.literal_eval(
            config_dict["conveyor_belt_output_location"]
        )
        self.conveyor_belt_intermediate_locations = ast.literal_eval(
            config_dict["conveyor_belt_intermediate_locations"]
        )
        self.conveyor_belt_input_location = ast.literal_eval(
            config_dict["conveyor_belt_input_location"]
        )
        self.store_locations = ast.literal_eval(config_dict["store_locations"])
        self.obstacle_locations = ast.literal_eval(config_dict["obstacle_locations"])

        # OPC UA
        self.opcua_server_urls = ast.literal_eval(config_dict["opcua_server_urls"])

        # For each node, a value should be given where the mirobot shall trigger
        self.opcua_nodes = ast.literal_eval(config_dict["opcua_nodes"])
        self.opcua_value = ast.literal_eval(config_dict["opcua_values"])
        self.opcua_routines = ast.literal_eval(config_dict["opcua_routines"])
        assert len(self.opcua_nodes) == len(self.opcua_values) and len(
            self.opcua_values
        ) == len(self.opcua_routines)

        self.opcua_polling_rate = config_dict["opcua_polling_rate"]
        self.opcua_request_timeout = config_dict["opcua_request_timeout"]
        # ROBO CONF
        self.mirobot_portname = config_dict["mirobot_portname"]
        self.mirobot_debug = bool(config_dict["mirobot_debug"])


def _get_config_values(file="./config.cfg", section="DEFAULT"):
    from configparser import ConfigParser

    config = ConfigParser()

    config.read(file)
    if section in config:
        return config[section]
    else:
        # returns first element in cfg
        raise FileNotFoundError("section not found in file")

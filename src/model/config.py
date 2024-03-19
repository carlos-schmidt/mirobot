import ast
from typing import List

from src.model.opcua_binding import OpcUABinding


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

        # OPC UA
        self.opcua_configs: List[OpcUABinding] = list()
        for config_set in ast.literal_eval(config_dict["opcua_configs"]):
            self.opcua_configs.append(
                OpcUABinding(
                    config_set[0],
                    config_set[1],
                    config_set[2],
                    config_set[3],
                    config_set[4],
                    config_set[5]
                )
            )

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

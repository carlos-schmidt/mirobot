from config_parser import get_config_values
from model.config import Config
from model.mirobot_wrapper import Mirobot
from opcua import Client

# Change where to find config here. Also set section if needed
config = Config(get_config_values())

opcua_client = Client(config.get_opcua_server_url(), config.get_opcua_request_timeout())

with Mirobot(config) as m:

    m.home_individual()

    m.go_to_zero()

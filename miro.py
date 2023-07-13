from model.config import Config
from model.mirobot_wrapper import Mirobot
from opcua import Client

# Change where to find config here. Also set section if needed
config = Config(file='./config.cfg', section='DEFAULT') # section='BLE'

opcua_client = Client(config.get_opcua_server_url(), config.get_opcua_request_timeout())

opcua_client.connect()

robot = Mirobot(config)

robot.initialize()

robot.disconnect()
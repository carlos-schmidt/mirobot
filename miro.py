from model import Config, Mirobot
from opcua import Client

# Change where to find config here
_config_location: str = './config.cfg'
# Also set section if needed
_section: str = 'DEFAULT'  # Bluetooth Low Energy: 'BLE'

config = Config(file=_config_location, section=_section)

opcua_client = Client(config.get_opcua_server_url(),
                      config.get_opcua_request_timeout())

opcua_client.connect()

robot = Mirobot(config)

robot.initialize()

# try unlock_shaft()?

# put following line into mirobot/serial_interface.py:181
# print(f"EOL threshold: {eol_threshold}")

robot.disconnect()

class Config:
    def __init__(self, config_dict: dict) -> None:
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
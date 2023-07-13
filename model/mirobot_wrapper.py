from time import sleep
import mirobot
from model.config import Config


class Mirobot(mirobot.Mirobot):
    
    """
    Provide constructor with own config as param
    """
    def __init__(self, config: Config) -> None:
        self._blocking = True
        super().__init__(portname=config.get_mirobot_portname(),
                         debug=config.get_mirobot_debug(),
                         wait=False) # TODO no waiting for robot's 'ok'
        
    def initialize(self):
        self.home_simultaneous()
        if self._blocking:
            sleep(15)
        self.go_to_zero()

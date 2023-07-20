from time import sleep
import mirobot
from model.config import Config


class Mirobot(mirobot.Mirobot):

    def __init__(self, config: Config) -> None:
        """Provide constructor to Mirobot with own config as param

        Args:
            config (Config): Configuration containing values such as mirobot port name
        """
        self._blocking = True
        self._initialized = False
        super().__init__(portname=config.get_mirobot_portname(),
                         debug=config.get_mirobot_debug(),
                         wait=False)  # TODO no waiting for robot's 'ok'

    def initialize(self):
        self.home_simultaneous(wait=True)
        if self._blocking:
            sleep(15)
        self.go_to_zero()
        self._initialized = True

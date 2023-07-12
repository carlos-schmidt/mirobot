import mirobot
from config import Config


class Mirobot(mirobot.Mirobot):
    """
    Provide constructor with own config as param
    """
    def __init__(self, config: Config) -> None:
        super().__init__(portname=config.get_mirobot_config(),
                         debug=config.get_mirobot_debug())

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.getLogger('asyncua').setLevel(logging.WARNING)
import asyncio
from src.mirobot_runner import MirobotEventListener
from src.model.config import Config

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    config = Config("./custom-config.cfg", "DEFAULT")
    mirobot_runner = MirobotEventListener(config)
    asyncio.run(mirobot_runner.listen_for_opcua_events())


# TODO UPDATE CONV OUTPUT LOCATION 
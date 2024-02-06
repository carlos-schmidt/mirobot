import asyncio
from src.mirobot_runner import MirobotEventListener
from src.model.config import Config
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    config = Config("./config.cfg", "DEFAULT")
    mirobot_runner = MirobotEventListener(config)
    asyncio.run(mirobot_runner.listen_for_opcua_events())

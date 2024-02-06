import asyncio
import logging
import numpy as np

from model.config import Config
from model.demonstrator_mirobot import DemonstratorMirobot
from model.event_listener import EventListener
from model.mirobot_wrapper import Mirobot
from model.robot_pose import RobotPose

logging.basicConfig(level=logging.WARN)
mr_logger = logging.getLogger("MirobotRunner")


class MirobotRunner(EventListener):
    def __init__(self, config: Config):
        super().__init__(config)

        self.robot = DemonstratorMirobot(config.mirobot_portname, config.mirobot_debug)

        self.nodes_triggers_routines = []

    def datachange_notification(self, node, val, data):
        """
        Callback for asyncua Subscription.
        This method will be called when the Client received a data change message from the Server.
        """

        for trigger_node, trigger_value, routine in self.nodes_triggers_routines:
            if node == trigger_node and val == trigger_value:
                mr_logger.warn("Starting robot interaction")
                # Call routine by its name
                result = self.exec_robo_func(routine)
                if hasattr(self, routine):
                    routine = getattr(self, routine)
                    routine()
                else:
                    mr_logger.error(
                        f"Following routine does not exist in MirobotRunner: {routine}. Check config"
                    )
                return

    @EventListener.mutex
    def exec_robo_func(self, func):
        self.robot.execute_routine(func_name=func)


if __name__ == "__main__":
    config = Config("./config.cfg", "DEFAULT")
    mirobot_runner = MirobotRunner(config)
    asyncio.run(mirobot_runner.listen_for_opcua_events())

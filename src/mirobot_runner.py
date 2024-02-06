import asyncio
import logging
import numpy as np

from .model.config import Config
from .model.demonstrator_mirobot import DemonstratorMirobot
from .model.event_listener import EventListener

_logger = logging.getLogger(__name__)


class MirobotEventListener(EventListener):
    def __init__(self, config: Config):
        self.nodes_triggers_routines = []
        super().__init__(config)

        self.robot = DemonstratorMirobot(config)

    def datachange_notification(self, node, val, data):
        """
        Callback for asyncua Subscription.
        This method will be called when the Client received a data change message from the Server.
        """

        _logger.debug(f"Got datachange notification:\n{node}\n{val}\n{data}")
        for trigger_node, trigger_value, routine in self.nodes_triggers_routines:
            if str(node) == trigger_node and str(val) == str(trigger_value):
                _logger.info("Starting robot interaction")
                # Call routine by its name
                self.exec_robo_func(routine)
                return

    def exec_robo_func(self, func):
        return self.robot.execute_routine(func_name=func)

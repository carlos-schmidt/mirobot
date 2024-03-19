import logging
from threading import Thread
from functools import partial

from src.model.demonstrator_mirobot import DemonstratorMirobot
from src.test.mock_demo_miro import MockDemonstratorMirobot

from .model.config import Config
from .model.event_listener import HTTPEventListener, OpcUAEventListener

_logger = logging.getLogger(__name__)


class MirobotEventListener(OpcUAEventListener):
    def __init__(self, config: Config):
        self.nodes_triggers_routines = []
        OpcUAEventListener.__init__(self, config)
        self.http_listener = HTTPEventListener()

        self.accepted_endpoints = config.opcua_routines + ["empty_store"]
        
        self.register_http_endpoints(self.http_listener)
        
        # Start http server in different thread
        self.http_listener.start()
        
        self.robot = MockDemonstratorMirobot(config)

    def register_http_endpoints(self, http_listener: HTTPEventListener):
        """Register HTTP endpoints to listen on

        Args:
            http_listener (HTTPEventListener): HTTP server instance
        """
        for endpoint in self.accepted_endpoints:
            # This prepares the function to be executed with a predefined argument
            http_listener.register_endpoint(
                endpoint="/" + endpoint,
                method="POST",
                handler=partial(self.exec_robo_func, endpoint),
            )

        http_listener.register_endpoint("/get_stored_items", "GET", self.get_stored_items)

    def datachange_notification(self, node, val, data):
        """
        Callback for asyncua Subscription.
        This method will be called when the Client received a data change message from the Server.
        """

        _logger.debug(f"Got datachange notification:\n{node}\n{val}\n{data}")
        for trigger_node, trigger_value, routine in self.nodes_triggers_routines:
            if str(node) == trigger_node and str(val) == str(trigger_value):
                # _logger.info("Starting robot interaction")
                self.exec_robo_func(routine)
                break

    def get_stored_items(self):
        return {"value": self.robot.get_stored_items()}

    def exec_robo_func(self, func):
        Thread(target=self.robot.execute_routine, args=(func,)).start()

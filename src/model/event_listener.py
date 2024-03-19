import asyncio
import logging
from threading import Thread
from typing import List
from asyncua import Client

from .config import Config

_logger = logging.getLogger(__name__)


class OpcUAEventListener:
    def __init__(self, config: Config):
        self.config: Config = config
        self.event_call_mutex = asyncio.Lock()
        self.nodes_triggers_routines = []
        _logger.setLevel(level="INFO")

    def datachange_notification(self, _, __, ___):
        _logger.error("This should be implemented by a subclass")

    def status_change_notification(self, status):
        _logger.debug("Got a status_change_notification!")
        _logger.debug(status)

    def event_notification(self, event):
        _logger.debug("Got a event_notification!")
        _logger.debug(event)

    async def create_opcua_subscriptions(self):
        clients = []

        for opcua_config in self.config.opcua_configs:
            _url = opcua_config.get_url()
            _logger.info(f"Connecting to url {_url} ...")
            new_client = Client(url=_url)

            try:
                await new_client.connect()
            except asyncio.exceptions.TimeoutError:
                _logger.warn(
                    f"Client {_url} not available due to asyncio.exceptions.TimeoutError! Continuing without this client."
                )
                continue
            except ConnectionRefusedError:
                _logger.warn(
                    f"Client {_url} not available due to ConnectionRefusedError! Continuing without this client."
                )
                continue
            clients.append(new_client)
            _logger.info(f"Connected to url {_url}")
            # One handler for all nodes. In datachange_notification the decision is made what to do.
            subscription = await new_client.create_subscription(opcua_config.get_rate(), self)
            
            await subscription.subscribe_data_change(new_client.get_node(opcua_config.get_node()))
            
            self.nodes_triggers_routines.append([opcua_config.get_node(), opcua_config.get_value(), opcua_config.get_routine()])

        return clients

    async def listen_for_opcua_events(self):
        clients: List[Client] = await self.create_opcua_subscriptions()
        if len(clients) > 0:
            _logger.info("Subscribed to OPCUA nodes.")
        else:
            _logger.error("No OPCUA nodes available.")
            return
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            _logger.info("Disconnecting from opcua servers...")
            [client.disconnect() for client in clients]


from flask import Flask


class HTTPEventListener(Thread):
    """Also called HTTP server"""

    app = Flask(__name__)

    def __init__(self, host="127.0.0.1", port=5000):
        super().__init__()
        self.host = host
        self.port = port

    def run(self):
        type(self).app.run(self.host, self.port)

    def register_endpoint(self, endpoint: str, method: str = "GET", handler=None):
        global app
        """Register an endpoint at endpoint path with function handler

        Args:
            endpoint (str): Endpoint path
            method (str): HTTP Method (GET POST PUT DELETE ...)
            handler (function): Function to execute if endpoint is called
        """
        type(self).app.add_url_rule(
            rule=endpoint, endpoint=endpoint, view_func=handler, methods=[str(method)]
        )
        _logger.info(f"Registered HTTP endpoint {endpoint} for method {method}")

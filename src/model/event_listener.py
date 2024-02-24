import asyncio
import logging
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
        utvr = zip(
            self.config.opcua_server_urls,
            self.config.opcua_nodes,
            self.config.opcua_values,
            self.config.opcua_routines,
        )
        clients = []

        for url in set(self.config.opcua_server_urls):
            print("Connecting to url", url)
            new_client = Client(url=url)

            # Fixes some weird bug https://github.com/FreeOpcUa/python-opcua/issues/629#issuecomment-1591109039
            # await new_client.disconnect()
            try:
                await new_client.connect()
            except asyncio.exceptions.TimeoutError:
                _logger.warn(
                    f"Client {url} not available! Continuing without this client."
                )
                continue
            clients.append(new_client)
            print("Connected to url", url)
            # One handler for all nodes. In datachange_notification the decision is made what to do.
            subscription = await new_client.create_subscription(
                float(self.config.opcua_polling_rate), self
            )
            nodes = []
            for _url, node_id, value, routine in utvr:
                if url == _url:
                    nodes.append(new_client.get_node(node_id))
                    self.nodes_triggers_routines.append([node_id, value, routine])

            # We subscribe to data changes for two nodes (variables).
            await subscription.subscribe_data_change(nodes)

        return clients

    async def listen_for_opcua_events(self):
        clients: List[Client] = await self.create_opcua_subscriptions()
        try:
            print("Subscribed to OPCUA nodes.")
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                pass
            # await asyncio.sleep(999_999_999)
        except KeyboardInterrupt:
            _logger.info("Disconnecting from opcua servers...")
            [client.disconnect() for client in clients]


from flask import Flask

class HTTPEventListener:
    app = Flask(__name__)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # forwards all unused arguments
        type(self).app.run()

    def register_endpoint(self, endpoint:str, method:str='GET', handler=None):
        global app
        """Register an endpoint at endpoint path with function handler

        Args:
            endpoint (str): Endpoint path
            method (str): HTTP Method (GET POST PUT DELETE ...)
            handler (function): Function to execute if endpoint is called
        """
        type(self).app.add_url_rule(rule=endpoint, endpoint=endpoint, view_func=handler, methods=[str(method)])

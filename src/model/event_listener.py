import asyncio
import logging
from asyncua import Client

from model.config import Config

logging.basicConfig(level=logging.INFO)
el_logger = logging.getLogger("EventListener")


class EventListener:
    def __init__(self, config: Config):
        self.config: Config = config
        self.event_call_mutex = asyncio.Lock()

    def mutex(func):
        def mutexed_call(self):
            with self.event_call_mutex:
                func(self)

        return mutexed_call

    def datachange_notification(self, _, __, ___):
        el_logger("This should be implemented by a EventListener subclass")

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
            async with Client(url=url) as new_client:
                print("Connected to url", url)

                clients.append(new_client)

                await new_client.connect()

                # Get nodes by nodeID
                self.nodes_triggers_routines = [
                    (new_client.get_node(node_id), value, routine)
                    for _url, node_id, value, routine in utvr
                    if url == _url
                ]

                # One handler for all nodes. In datachange_notification the decision is made what to do.
                subscription = await new_client.create_subscription(
                    self.config.opcua_polling_rate, self
                )
                # We subscribe to data changes for two nodes (variables).
                await subscription.subscribe_data_change(self.config.opcua_nodes)

        return clients

    async def listen_for_opcua_events(self):
        clients = await self.create_opcua_subscriptions()
        try:
            print("Subscribed to OPCUA nodes.")
            await asyncio.sleep(999_999_999)
        except KeyboardInterrupt:
            el_logger.info("Disconnecting from opcua servers...")
            [client.disconnect() for client in clients]

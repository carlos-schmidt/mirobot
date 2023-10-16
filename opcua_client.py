import asyncio
from asyncua import Client, Node
import logging

url = 'opc.tcp://localhost:4840/freeopcua/server/'
namespace = 'http://iosb.fraunhofer.example'
topic = 'ns=3;s=MeasuringStationStep'
period = 500 # millis, period of reading value

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

class SubscriptionHandler:
    """
    The SubscriptionHandler is used to handle the data that is received for the subscription.
    """
    def datachange_notification(self, node: Node, val, data):
        """
        Callback for asyncua Subscription.
        This method will be called when the Client received a data change message from the Server.
        """
        _logger.info('datachange_notification %r %s', node, val)
        # TODO in case of publishing by server, use this callback for robot action triggering


async def main():
    
    print(f'Connecting to {url}...')
    async with Client(url=url) as client:
        
        # Find the namespace index
        nsidx = await client.get_namespace_index(namespace)
        print(f'Namespace Index for "{namespace}": {nsidx}')

        # Get the variable node for read / write
        var = await client.nodes.root.get_child(
            ['0:Objects', f'{nsidx}:MeasuringStationStep', f'{nsidx}:MyVariable']
        )
        value = await var.read_value()
        print(f'Value of MyVariable ({var}): {value}')
        
        handler = SubscriptionHandler()
        subscription = await client.create_subscription(period, handler)
        nodes = [
            var,
            client.get_node("ns=3;s=MeasuringStationStep")
        ]
        
        # We subscribe to data changes for two nodes (variables).
        await subscription.subscribe_data_change(nodes)
        
        # We let the subscription run for ten seconds
        await asyncio.sleep(10)
        
        # This is optional since closing the connection will also delete all subscriptions.
        await subscription.delete()
        
        # After one second we exit the Client context manager - this will close the connection.
        await asyncio.sleep(1)
        
if __name__ == "__main__":
    asyncio.run(main())

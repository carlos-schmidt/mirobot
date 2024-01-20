import asyncio
from asyncua import Client, Node
import logging
from run import main as robo

url = 'opc.tcp://192.168.1.1:4840/'
topic = "ns=3;s=\"MeasuringStationStep\""
period = 500 # millis, period of reading value

logging.basicConfig(level=logging.WARN)
_logger = logging.getLogger('asyncua')

class SubscriptionHandler:
        
    def datachange_notification(self, node: Node, val, data):
        """
        Callback for asyncua Subscription.
        This method will be called when the Client received a data change message from the Server.
        """
        if val==22:
            _logger.warn('Starting robot interaction')
            self.start_robot_interaction()
            robo()
        _logger.info('datachange_notification %r %s', node, val)
        # TODO in case of publishing by server, use this callback for robot action triggering
            
    
async def main():
    
    print(f'Connecting to {url}...')
    async with Client(url=url) as client:
        
        # Find the namespace index
        #nsidx = await client.get_namespace_index(namespace)
        #print(f'Namespace Index for "{namespace}": {nsidx}')
        #print(await client.nodes.root.get_child(["0:Objects"]))
        # Get the variable node for read / write
        var = client.get_node(topic)
        
        print("hello ",var, type(var))
        value = await var.read_value()
        print(f'Value of MyVariable ({var}): {value}')
        
        handler = SubscriptionHandler()
        subscription = await client.create_subscription(period, handler)
        nodes = [var]
        
        # We subscribe to data changes for two nodes (variables).
        await subscription.subscribe_data_change(nodes)
        
        # We let the subscription run for ten seconds
        await asyncio.sleep(100000)
        
        # This is optional since closing the connection will also delete all subscriptions.
        # await subscription.delete()
        
        # After one second we exit the Client context manager - this will close the connection.
        # await asyncio.sleep(1)
        
if __name__ == "__main__":
    asyncio.run(main())

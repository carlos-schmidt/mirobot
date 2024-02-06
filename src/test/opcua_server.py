from asyncua import ua, Server, Node
from threading import Thread
import logging
import time
import sys
import asyncio

sys.path.insert(0, "..")


async def main():
    _logger = logging.getLogger(__name__)
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # set up our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    _ = await server.register_namespace(uri)
    ns3 = await server.register_namespace(uri + "/")
    print(f"##### ##### REGISTERING ON NAMESPACE ns={ns3} ##### #####")
    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    myobj: Node = await server.nodes.objects.add_object(ns3, "obj")
    myvar = await myobj.add_variable(
        ua.NodeId('"test"', 3), '"test"', 420, ua.VariantType.Int16
    )
    myvar = await myobj.add_variable(
        ua.NodeId('"test_2"', 3), '"test_2"', 404, ua.VariantType.Int16
    )
    myvar = await myobj.add_variable(
        ua.NodeId('"MeasuringStationStep"', 3),
        '"MeasuringStationStep"',
        22,
        ua.VariantType.Int64,
    )

    # Set MyVariable to be writable by clients
    await myvar.set_writable()

    _logger.info("Starting server!")
    async with server:
        try:
            k = 0
            while True:
                k += 1
                v = 22 + k % 2
                await myvar.write_value(v)
                await asyncio.sleep(1)
                print(
                    'ns=3;s="MeasuringStationStep" VALUE=',
                    await server.get_node('ns=3;s="MeasuringStationStep"').read_value(),
                )

        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main(), debug=True)

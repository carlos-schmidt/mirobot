import asyncio
from asyncua import ua, Server, Node
from threading import Thread
import logging
import time
from math import sin
import sys

sys.path.insert(0, "..")


class VarUpdater(Thread):
    def __init__(self, var):
        Thread.__init__(self)
        self._stopev = False
        self.var = var

    def stop(self):
        self._stopev = True

    def run(self):
        k = 0
        while not self._stopev:
            k += 1

            v = 22 + k % 2
            self.var.set_value(v)
            time.sleep(2)


async def main():
    # optional: setup logging
    logging.basicConfig(level=logging.WARN)

    # now setup our server
    server = Server()
    await server.init()

    server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
    server.set_server_name("FreeOpcUa Example Server")
    
    # set all possible endpoint policies for clients to connect through
    server.set_security_policy([ua.SecurityPolicyType.NoSecurity])

    # setup our own namespace
    uri = "http://iosb.fraunhofer.example"
    idx = await server.register_namespace(uri)

    # populating our address space

    # create directly some objects and variables
    myobj: Node = await server.nodes.objects.add_object(idx, "MeasuringStationStep")
    myvar = await myobj.add_variable(idx, "MyVariable", 22, ua.VariantType.Int16)

    # starting!
    await server.start()
    # print(await server.get_endpoints())
    # vup = VarUpdater(myvar)  # just a class to update the variable
    # vup.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        vup.stop()
        await server.stop()


if __name__ == "__main__":
    asyncio.run(main())

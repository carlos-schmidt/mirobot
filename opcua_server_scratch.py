import asyncio
import copy
import logging
from datetime import datetime
import time
from math import sin
from asyncua import ua, uamethod, Server


async def main():
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    server.set_server_name("FreeOpcUa Example Server")

    # setup our own namespace
    uri = "http://examples.freeopcua.github.io"
    await server.register_namespace(uri)

    # starting!
    async with server:
        print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
        # enable following if you want to subscribe to nodes on server side
        # handler = SubHandler()
        # sub = await server.create_subscription(500, handler)
        # handle = await sub.subscribe_data_change(myvar)
        # trigger event, all subscribed clients wil receive it

        while True:
            await asyncio.sleep(0.1)


asyncio.run(main())

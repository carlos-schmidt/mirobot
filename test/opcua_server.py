from opcua import ua, uamethod, Server
from threading import Thread
import logging
import time
from math import sin
import sys

sys.path.insert(0, "..")

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        myvars = globals()
        myvars.update(locals())
        shell = code.InteractiveConsole(myvars)
        shell.interact()


class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)


# method to be exposed through server

def func(parent, variant):
    ret = False
    if variant.Value % 2 == 0:
        ret = True
    return [ua.Variant(ret, ua.VariantType.Boolean)]


# method to be exposed through server
# uses a decorator to automatically convert to and from variants

@uamethod
def multiply(parent, x, y):
    print("multiply method call with parameters: ", x, y)
    return x * y


class VarUpdater(Thread):
    def __init__(self, var):
        Thread.__init__(self)
        self._stopev = False
        self.var = var

    def stop(self):
        self._stopev = True

    def run(self):
        while not self._stopev:
            v = int(sin(time.time() / 10)*5)
            self.var.set_value(v)
            time.sleep(0.1)


if __name__ == "__main__":
    # optional: setup logging
    logging.basicConfig(level=logging.WARN)

    # now setup our server
    server = Server()
    # server.disable_clock()
    # server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    server.set_server_name("FreeOpcUa Example Server")
    # set all possible endpoint policies for clients to connect through
    server.set_security_policy([
        ua.SecurityPolicyType.NoSecurity,
        ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
        ua.SecurityPolicyType.Basic256Sha256_Sign])

    # setup our own namespace
    uri = "http://iosb.fraunhofer.example"
    idx = server.register_namespace(uri)

    # populating our address space

    # create directly some objects and variables
    myobj = server.nodes.objects.add_object(idx, "MeasuringStationStep")
    myvar = myobj.add_variable(idx, "MyVariable", 22, ua.VariantType.Int16)

    # creating a default event object
    # The event object automatically will have members for all events properties
    # you probably want to create a custom event type, see other examples
    myevgen = server.get_event_generator()
    myevgen.event.Severity = 300

    # starting!
    server.start()

    vup = VarUpdater(myvar)  # just  a stupid class update a variable
    vup.start()
    try:
        # enable following if you want to subscribe to nodes on server side
        # handler = SubHandler()
        # sub = server.create_subscription(500, handler)
        # handle = sub.subscribe_data_change(myvar)

        myevgen.trigger(message="This is BaseEvent")
        # Server side write method which is a bit faster than using set_value
        server.set_attribute_value(myvar.nodeid, ua.DataValue(9))

        embed()
    finally:
        vup.stop()
        server.stop()

import asyncio
import logging
import numpy as np
import sys
from time import sleep
from asyncua import Client, Node

from wlkata_mirobot import WlkataMirobot, WlkataMirobotTool
from model.config import Config
from model.mirobot_wrapper import Mirobot

from opcua_client import SubscriptionHandler

logging.basicConfig(level=logging.WARN)
mr_logger = logging.getLogger("MirobotRunner")


class MirobotRunner:
    def __init__(self, config: Config) -> None:
        self.opcua_handler = SubscriptionHandler()
        self.robot = Mirobot(config.mirobot_portname, config.mirobot_debug)
        # Nodes to listen for (there is a mapping topic->node)
        self.triggers_and_routines = []

    def datachange_notification(self, node: Node, val, data):
        """
        Callback for asyncua Subscription.
        This method will be called when the Client received a data change message from the Server.
        """

        for trigger_node, trigger_value, routine in self.triggers_and_routines:
            if node == trigger_node and val == trigger_value:
                mr_logger.warn("Starting robot interaction")
                # Call routine by its name (possibly unsafe?)
                if hasattr(self, routine):
                    getattr(self, routine)()
                else:
                    mr_logger.error(f"Routine does not exist in MirobotRunner: {routine}")
                return

    def put_from_conv_bucket():
        # TODO
        pass
    
    def store_item():
        # TODO
        pass
    
    def put_from_store():
        # TODO
        pass

    async def listen_for_opcua_events(self):
        url = config.opcua_server_url
        print(f"Connecting to {url}...")

        async with Client(url=url) as client:
            # Get nodes for topics
            self.triggers_and_routines = [
                (client.get_node(topic), value, routine)
                for topic, value, routine in zip(
                    config.opcua_topics, config.opcua_values, config.opcua_routines
                )
            ]

            # One handler for all topics. In datachange_notification the decision is made what to do.
            subscription = await client.create_subscription(
                config.opcua_polling_rate, self
            )

            # We subscribe to data changes for two nodes (variables).
            await subscription.subscribe_data_change(self.triggers_and_routines)

            # We let the subscription run for one hundred thousand seconds TODO change
            await asyncio.sleep(100_000)

    # TODO calculate trajectory and test for possible crashes
    # TODO maybe poll current position and stop if too close to obstacle? Also slow down when getting closer
    
    # TODO OR: compute halfway position and move there, before: test if anything between robo and halfway. do this for quarterway too?

if __name__ == "__main__":
    config = Config("./config.cfg")
    mirobot_runner = MirobotRunner(config)

    asyncio.run(mirobot_runner.listen_for_opcua_events())


source_position = (-63, 48.4, 22.46, 53, -52.8, 0)
intermediate_to_source_position = (-35, -16, 29, 0, 0, 0)
destination_position = (103, 45.99, -88, 5, 29.99, 2)
neutral_position = (200, 0, 300, 0, 0, 0)
height_item = 28
# 创建机械臂
arm = WlkataMirobot(portname="COM3")


def translate(point, x, y, z, alpha):
    """
    alpha in degrees!!!
    """
    slope = alpha * np.pi / 180  # 30 degrees

    homogenous_matrix = np.array(
        [
            [np.cos(slope), 0, -np.sin(slope), x],
            [0, 1, 0, y],
            [np.sin(slope), 0, np.cos(slope), z],
            [0, 0, 0, 1],
        ]
    )

    return (homogenous_matrix @ (point + [1]))[:3]


def move_to_neutral_position():
    arm.set_tool_pose(*neutral_position)


def pick_up_at(x, y, z, a, b, c, item_height):
    print(f"Picking up item at (x,y,z)=({x},{y},{z + item_height})")
    move_to_neutral_position()
    arm.set_tool_pose(x, y, z + 2 * item_height, a, b, c)
    arm.set_tool_pose(x, y, z + item_height, a, b, c)
    sleep(0.2)  # seconds
    arm.set_air_pump(WlkataMirobot.AIR_PUMP_SUCTION_PWM_VALUE)
    arm.set_tool_pose(x, y, z + 2 * item_height, a, b, c)


def drop_at(x, y, z, a, b, c, item_height):
    print(f"Dropping item at (x,y,z)=({x},{y},{z + item_height})")
    move_to_neutral_position()
    arm.set_tool_pose(x, y, z + 2 * item_height, a, b, c)
    # Stop a bit above end point (3mm)
    arm.set_tool_pose(x, y, z + item_height + 3, a, b, c)
    sleep(0.2)  # seconds
    arm.set_air_pump(WlkataMirobot.AIR_PUMP_OFF_PWM_VALUE)
    arm.set_tool_pose(x, y, z + 2 * item_height, a, b, c)


def calibrate():
    init()
    arm.set_tool_type(WlkataMirobotTool.SUCTION_CUP)
    arm.set_tool_offset(0, 0, 40)  # height of whole tool (mm)
    # pick_up_at(source_position, height_item)
    arm.go_to_zero()
    # input()
    source_position = [30, -185, -3.53]
    source_approach_position = translate(source_position, 0, 0, 0, 80)

    arm.set_tool_pose(*source_approach_position, -5, -30, 0)
    input()
    arm.set_tool_pose(*source_position, -5, -30, 0)
    # input()
    arm.set_air_pump(WlkataMirobot.AIR_PUMP_SUCTION_PWM_VALUE)

    arm.set_tool_pose(*source_approach_position, 0, -30, 0)

    arm.go_to_zero()
    input()
    arm.set_air_pump(WlkataMirobot.AIR_PUMP_OFF_PWM_VALUE)


def init():
    # arm = WlkataMirobot(portname='COM7')
    status = arm.get_status()
    print("Robot is in state:", status.state)

    if status.state == "Alarm":
        mr_logger.info("Homing")
        arm.home()


def move_n_items(n, source, destination):
    for i in range(n):
        pick_up_at(*source, (n - i) * height_item)
        drop_at(*destination, (i + 1) * height_item)


def main():
    source_position = (-63, 48.4, 22.46, 53, -52.8, 0)
    intermediate_to_source_position = (-35, -16, 29, 0, 0, 0)
    destination_position = (103, 45.99, -88, 5, 29.99, 2)
    init()
    arm.set_tool_type(WlkataMirobotTool.SUCTION_CUP)
    # arm.set_tool_offset(0, 0, 40)  # height of whole tool (mm)
    arm.go_to_zero()
    print("Hello")
    arm.go_to_axis(-35, -16, 29, 0, 0, 0)
    print("Hello")
    arm.go_to_axis(-63, 48.4, 22.46, 53, -52.8, 0)
    print("Hello")
    arm.set_air_pump(WlkataMirobot.AIR_PUMP_SUCTION_PWM_VALUE)
    arm.go_to_axis(-35, -16, 29, 0, 0, 0)
    arm.go_to_zero()

    exit(0)
    # arm.go_to_axis(1,0,0,0,0,0)
    # pick_up_at(source_position, height_item)
    # input()
    exit(0)
    source_position = [30, -185, -3.53]
    source_approach_position = translate(source_position, 0, 0, 0, 80)
    destination_position = [175, 195, 193.6]
    destination_approach_position = translate(
        destination_position, 0, 0, height_item, 0
    )

    arm.set_tool_pose(*source_approach_position, -5, -30, 0)
    # input()
    arm.set_tool_pose(*source_position, -5, -30, 0)
    # input()

    arm.set_tool_pose(*source_approach_position, 0, -30, 0)

    arm.go_to_zero()
    # input()
    arm.set_tool_pose(*destination_approach_position, 0, 0, 0)
    # input()
    arm.set_tool_pose(*destination_position, 0, 0, 0)
    # input()
    # input()
    arm.set_air_pump(WlkataMirobot.AIR_PUMP_OFF_PWM_VALUE)
    arm.set_tool_pose(*destination_approach_position, 0, 0, 0)

    arm.go_to_zero()

    # print(source_position, source_approach_position)
    # print(destination_position, destination_approach_position)
    move_to_neutral_position()


if __name__ == "__main__":
    main()

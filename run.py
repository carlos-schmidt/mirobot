import asyncio
import logging
import numpy as np
from time import sleep
from asyncua import Client, Node
from mirobot import BaseMirobot, Mirobot
from wlkata_mirobot import WlkataMirobot, WlkataMirobotTool
from model.config import Config
from model.mirobot_wrapper import Mirobot
from model.robot_pose import RobotPose
from opcua_client import SubscriptionHandler

logging.basicConfig(level=logging.WARN)
mr_logger = logging.getLogger("MirobotRunner")


class MirobotRunner:
    def __init__(self, config: Config) -> None:
        self.opcua_handler = SubscriptionHandler()
        self.robot = Mirobot(config.mirobot_portname, config.mirobot_debug)
        # Nodes to listen for (there is a mapping topic->node)
        self.triggers_and_routines = []
        self.conveyor_belt_output_location: RobotPose = RobotPose(
            config.conveyor_belt_output_location
        )
        self.conveyor_belt_intermediate_locations: [RobotPose] = [
            RobotPose(pos) for pos in config.conveyor_belt_intermediate_locations
        ]
        self.conveyor_belt_input_location: RobotPose = RobotPose(
            config.conveyor_belt_input_location
        )
        self.store_locations: [RobotPose] = [
            RobotPose(pos) for pos in config.store_locations
        ]
        self.stored_items: int = config.stored_items_initial


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
                    routine: function = getattr(self, routine)
                    routine()
                else:
                    mr_logger.error(
                        f"Following routine does not exist in MirobotRunner: {routine}"
                    )
                return

    def put_from_conveyor_belt_output(self):
        print(f"Picking up item at", self.conveyor_belt_output_location.astuple())
        self.robot.move_along_trajectory(self.conveyor_belt_output_location, self.conveyor_belt_intermediate_locations)
        self.robot.pick_up()
        self.robot.move_along_trajectory(self.conveyor_belt_input_location, self.conveyor_belt_intermediate_locations)
        self.robot.drop()

    def store_item(self):
        # TODO
        pass

    def put_from_store(self):
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
            await subscription.subscribe_data_change(config.opcua_topics)

            # We let the subscription run for one hundred thousand seconds TODO change
            await asyncio.sleep(100_000)


if __name__ == "__main__":
    config = Config("./config.cfg", "DEFAULT")
    mirobot_runner = MirobotRunner(config)
    asyncio.create_task(mirobot_runner.listen_for_opcua_events())
    asyncio.run()
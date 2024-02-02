import asyncio
import logging
import numpy as np

from model.config import Config
from model.event_listener import EventListener
from model.mirobot_wrapper import Mirobot
from model.robot_pose import RobotPose

logging.basicConfig(level=logging.WARN)
mr_logger = logging.getLogger("MirobotRunner")


class MirobotRunner(EventListener):
    def __init__(self, config: Config):
        super().__init__(config)

        self.robot = Mirobot(config.mirobot_portname, config.mirobot_debug)

        self.nodes_triggers_routines = []
        self.conveyor_belt_output_location = RobotPose(
            np.asarray(config.conveyor_belt_output_location)
        )
        self.conveyor_belt_intermediate_locations = [
            RobotPose(np.asarray(pos))
            for pos in config.conveyor_belt_intermediate_locations
        ]
        self.conveyor_belt_input_location = RobotPose(
            np.asarray(config.conveyor_belt_input_location)
        )
        self.store_locations = [
            RobotPose(np.asarray(pos)) for pos in config.store_locations
        ]
        self.stored_items: int = config.stored_items_initial
        self.zero_position = RobotPose(np.asarray((0.0, 0.0, 0.0, 0.0, 0.0, 0.0)))

    def datachange_notification(self, node, val, data):
        """
        Callback for asyncua Subscription.
        This method will be called when the Client received a data change message from the Server.
        """

        for trigger_node, trigger_value, routine in self.nodes_triggers_routines:
            if node == trigger_node and val == trigger_value:
                mr_logger.warn("Starting robot interaction")
                # Call routine by its name
                if hasattr(self, routine):
                    routine = getattr(self, routine)
                    routine()
                else:
                    mr_logger.error(
                        f"Following routine does not exist in MirobotRunner: {routine}. Check config"
                    )
                return

    @EventListener.mutex
    def put_from_conveyor_belt_output(self):
        with self.robo_mutex:
            mr_logger.info(f"ITEM-OUTPUT->ITEM-INPUT")
            self.robot.move_along_trajectory(
                self.conveyor_belt_output_location,
                self.conveyor_belt_intermediate_locations,
            )
            self.robot.pick_up()
            self.robot.move_along_trajectory(
                self.conveyor_belt_input_location,
                self.conveyor_belt_intermediate_locations,
            )
            self.robot.drop()
            self.robot.go_to_zero()

    @EventListener.mutex
    def store_item(self):
        mr_logger.info(f"ITEM-OUTPUT->STORE[{self.stored_items}]")
        self.robot.move_along_trajectory(
            self.conveyor_belt_output_location,
            self.conveyor_belt_intermediate_locations,
        )
        self.robot.pick_up()
        self.robot.move_along_trajectory(self.store_locations[self.stored_items])
        self.robot.drop()
        self.robot.move_along_trajectory(
            self.zero_position, self.conveyor_belt_intermediate_locations
        )

        self.stored_items += 1

    @EventListener.mutex
    def put_from_store(self):
        if self.stored_items < 1:
            mr_logger.warn("No items in store or wrong configuration values")
        mr_logger.info(f"STORE[{self.stored_items}]->ITEM-INPUT")
        self.robot.move_along_trajectory(
            self.store_locations[self.stored_items],
            self.conveyor_belt_intermediate_locations,
        )
        self.robot.pick_up()
        self.robot.move_along_trajectory(
            self.conveyor_belt_input_location, self.conveyor_belt_intermediate_locations
        )
        self.robot.drop()
        self.robot.go_to_zero()

        self.stored_items -= 1


if __name__ == "__main__":
    config = Config("./config.cfg", "DEFAULT")
    mirobot_runner = MirobotRunner(config)
    asyncio.run(mirobot_runner.listen_for_opcua_events())

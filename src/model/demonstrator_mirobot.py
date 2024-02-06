import asyncio
from collections.abc import Callable
import logging

import numpy as np
from model.config import Config
from model.mirobot_wrapper import Mirobot
from model.robot_pose import RobotPose

logging.basicConfig(level=logging.INFO)
dem_logger = logging.getLogger("MirobotRunner")

allowed_routines = ["put_from_conveyor_belt_output", "store_item", "put_from_store"]


class RoutineNotFoundError:
    pass


class DemonstratorMirobot(Mirobot):
    def __init__(
        self,
        config: Config,
        default_to_zero: bool = True,
    ):
        super().__init__(config, default_to_zero)
        self.routine_mutex = asyncio.Lock()

        self.conv_belt_out = RobotPose(np.asarray(config.conveyor_belt_output_location))
        self.conv_belt_intermediate = [
            RobotPose(np.asarray(pos))
            for pos in config.conveyor_belt_intermediate_locations
        ]
        self.conv_belt_in = RobotPose(np.asarray(config.conveyor_belt_input_location))
        self.store_locations = [
            RobotPose(np.asarray(pos)) for pos in config.store_locations
        ]
        self.stored_items: int = config.stored_items_initial
        self.zero_position = RobotPose(np.asarray((0.0, 0.0, 0.0, 0.0, 0.0, 0.0)))

    def execute_routine(self, routine_name: str):
        """Run a routine if it exists.
        Only one routine is allowed at a time.
        The robot always returns to the zero location at the end of a routine.

        Args:
            routine_name (str): Name of the routine to be executed

        Raises:
            RoutineNotFoundError: Routine with the given name not found
        """
        if routine_name not in allowed_routines or not hasattr(self, routine_name):
            raise RoutineNotFoundError()

        # Get the function
        routine = getattr(self, routine)

        # Mutex to ensure no concurrent moves being made
        with self.routine_mutex:
            self.routine()

    def put_from_conveyor_belt_output(self):
        dem_logger.info(f"ITEM-OUTPUT->ITEM-INPUT")
        self.move_along_trajectory(
            self.conv_belt_out,
            self.conv_belt_intermediate,
        )
        self.pick_up()
        self.move_along_trajectory(
            self.conv_belt_in,
            self.conv_belt_intermediate,
        )
        self.drop()
        self.go_to_zero()

    def store_item(self):
        dem_logger.info(f"ITEM-OUTPUT->STORE[{self.stored_items}]")
        self.move_along_trajectory(
            self.conv_belt_out,
            self.conv_belt_intermediate,
        )
        self.pick_up()
        self.move_along_trajectory(self.store_locations[self.stored_items])
        self.drop()
        self.move_along_trajectory(self.zero_position, self.conv_belt_intermediate)

        self.stored_items += 1

    def put_from_store(self):
        if self.stored_items < 1:
            dem_logger.warn("No items in store or wrong configuration values")
            return
        dem_logger.info(f"STORE[{self.stored_items}]->ITEM-INPUT")
        self.move_along_trajectory(
            self.store_locations[self.stored_items],
            self.conv_belt_intermediate,
        )
        self.pick_up()
        self.move_along_trajectory(self.conv_belt_in, self.conv_belt_intermediate)
        self.drop()
        self.go_to_zero()

        self.stored_items -= 1

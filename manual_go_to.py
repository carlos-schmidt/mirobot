import numpy as np
from wlkata_mirobot import WlkataMirobot, WlkataMirobotTool

from src.model.config import Config
from src.model.robot_pose import RobotPose

config = Config("./custom-config.cfg", "DEFAULT")

bot = WlkataMirobot(portname='/dev/tty8', default_speed=9999)
store_locations = [RobotPose(np.asarray(pos)) for pos in config.store_locations]


for store_location in store_locations:
    bot.go_to_axis(*store_location.astuple())
    bot.go_to_axis(*RobotPose(config.conveyor_belt_intermediate_locations[0]).astuple())
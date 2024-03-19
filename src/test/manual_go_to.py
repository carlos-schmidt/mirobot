import numpy as np
from wlkata_mirobot import WlkataMirobot

from src.model.config import Config
from src.model.robot_pose import RobotPose


# Playground where you can set custom positions for the robot go move to
config = Config("./custom-config.cfg", "DEFAULT")

bot = WlkataMirobot(portname='COM8', default_speed=3000)
store_locations = [RobotPose(np.asarray(pos)) for pos in config.store_locations]

# Choose intermediate position
bot.linear_interpolation(134.034,-93.823,188.632,0.000,13.001,-34.992)
for store_location in store_locations:
    store_intermediate = store_location + RobotPose(np.asarray([0,0,50,0,0,0])) # Z coord + 50
    #bot.linear_interpolation(*store_intermediate.astuple())
    bot.linear_interpolation(*store_location.astuple())

import logging
from time import sleep
import numpy as np
from wlkata_mirobot import WlkataMirobot, WlkataMirobotTool
from model.config import Config
from model.RobotPose import RobotPose


logging.basicConfig(level=logging.WARN)
_logger = logging.getLogger("Mirobot")


def _translate(current_position: RobotPose, x, y, z, alpha) -> RobotPose:
    """Translate and rotate point around y axis using a homogenous matrix

    Args:
        point (RobotPosition): Current position
        x (float): x axis translation offset
        y (float): y axis translation offset
        z (float): z axis translation offset
        alpha (float): Rotation angle

    Returns:
        RobotPosition: translated position
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

    return (homogenous_matrix @ (current_position + [1]))[:3]


def _print_response(response):
    _logger.debug("Robot returned: ", response)


class Mirobot(WlkataMirobot):
    def __init__(
        self, mirobot_portname: str, mirobot_debug: bool, default_to_zero: bool = True, tool_length: float = 0
    ):
        """Provide constructor to Mirobot with own config as param. Check the current state of the robot. If state = 'Alarm', ask to home to unlock movement. If no homing is requested, try to unlock axes without homing.

        Args:
            mirobot_portname (str): mirobot port name for base class
            mirobot_debug (str): Mirobot base class debug
            default_to_zero (bool, optional): Go to zero at the end of the initialization process. Defaults to True.
            tool_length (float, optional): The length of the tool added to the standard endeffector. Defaults to 0 if the coordinates were computed with the tool attached.

        """
        super().__init__(portname=mirobot_portname, debug=mirobot_debug)

        self._blocking = False
        self._initialized = False
        self.set_tool_type(WlkataMirobotTool.SUCTION_CUP)
        self.set_tool_offset(0, 0, tool_length)  # height of whole tool (mm)

        if self.get_status().state == "Alarm":
            yn = input("Current state is Alarm. Start homing procedure? (y/n)")
            if "y" in yn:
                _logger.info("Homing")
                self.home()
            else:
                _logger.info("Trying to unlock axes without homing")
                resp = self.unlock_all_axis()
                _print_response(resp)
        if default_to_zero:
            print("Moving to zero position...")
            self.go_to_zero()

        self._initialized = True

    def pick_up(self):
        """Turn air pump on to activate suction gripper"""
        self.set_air_pump(WlkataMirobot.AIR_PUMP_SUCTION_PWM_VALUE)

    def drop(self):
        """Turn air pump off to deactivate suction gripper"""
        self.set_air_pump(WlkataMirobot.AIR_PUMP_SUCTION_PWM_VALUE)

    def move_along_trajectory(
        self,
        destination: RobotPose,
        trajectory: [RobotPose],
        speed: float = 0.5,
    ):
        """Move to destination along a trajectory defined by positions in trajectory at a specified speed

        Args:
            destination (RobotPosition): Destination position
            trajectory (RobotPosition], optional): Trajectory along which to move towards destination. Defaults to None.
            speed (float, optional): Speed of robot (values in interval (0,1] allowed). Defaults to 0.5.
        """
        if type(self.set_speed(3000 * speed)) is bool and not self.set_speed(
            3000 * speed
        ):
            _logger.warn("Speed out of bounds:", speed, "defaulting to 0.5")
            self.set_speed(1500)

        for pose in trajectory:
            self.go_to_axis(
                pose.x,
                pose.y,
                pose.z,
                pose.a,
                pose.b,
                pose.c,
            )

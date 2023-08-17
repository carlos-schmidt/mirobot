import numpy as np
import sys
from time import sleep

from wlkata_mirobot import WlkataMirobot, WlkataMirobotTool

source_position = (7, -160, 34, 0, 0, 0)
destination_position = (123, -217, 0, 0, 0, 0)
neutral_position = (200, 0, 300, 0, 0, 0)
height_item = 28
# 创建机械臂
arm = WlkataMirobot(portname='/dev/tty.usbserial-140')


def translate(point, x, y, z, alpha):
    """
    alpha in degrees!!!
    """
    slope = alpha * np.pi/180  # 30 degrees

    homogenous_matrix = np.array([
        [np.cos(slope), 0, -np.sin(slope), x],
        [0, 1, 0, y],
        [np.sin(slope), 0, np.cos(slope), z],
        [0, 0, 0, 1]])

    return (homogenous_matrix @ (point+[1]))[:3]


def move_to_neutral_position():
    arm.set_tool_pose(*neutral_position)


def pick_up_at(x, y, z, a, b, c, item_height):
    print(f"Picking up item at (x,y,z)=({x},{y},{z + item_height})")
    move_to_neutral_position()
    arm.set_tool_pose(x, y, z + 2 * item_height, a, b, c)
    arm.set_tool_pose(x, y, z + item_height, a, b, c)
    sleep(.2)  # seconds
    arm.set_air_pump(WlkataMirobot.AIR_PUMP_SUCTION_PWM_VALUE)
    arm.set_tool_pose(x, y, z + 2 * item_height, a, b, c)


def drop_at(x, y, z, a, b, c, item_height):
    print(f"Dropping item at (x,y,z)=({x},{y},{z + item_height})")
    move_to_neutral_position()
    arm.set_tool_pose(x, y, z + 2 * item_height, a, b, c)
    # Stop a bit above end point (3mm)
    arm.set_tool_pose(x, y, z + item_height + 3, a, b, c)
    sleep(.2)  # seconds
    arm.set_air_pump(WlkataMirobot.AIR_PUMP_OFF_PWM_VALUE)
    arm.set_tool_pose(x, y, z + 2 * item_height, a, b, c)


def init():
    arm = WlkataMirobot(portname='/dev/tty.usbserial-140')
    status = arm.get_status()
    print("Robot is in state:", status.state)

    if status.state == 'Alarm':
        print("Homing")
        arm.home()


def move_n_items(n, source, destination):
    for i in range(n):
        pick_up_at(*source, (n - i) * height_item)
        drop_at(*destination, (i + 1) * height_item)


if __name__ == "__main__":
    init()
    arm.set_tool_type(WlkataMirobotTool.SUCTION_CUP)
    arm.set_tool_offset(0, 0, 40)  # height of whole tool (mm)
    # pick_up_at(source_position, height_item)
    # arm.go_to_zero()
    source_position = [7, -160, 34]
    source_approach_position = translate(source_position, 0, 0, 60, 30)

    destination_position = [173, 180, 150]
    destination_approach_position = translate(
        destination_position, 0, 0, height_item, 0)

    arm.set_tool_pose(*source_approach_position, 0, -30, 0)
    input()
    arm.set_tool_pose(*source_position, 0, -30, 0)
    input()
    arm.set_air_pump(WlkataMirobot.AIR_PUMP_SUCTION_PWM_VALUE)

    arm.set_tool_pose(*source_approach_position, 0, -30, 0)

    arm.go_to_zero()

    arm.set_tool_pose(*destination_approach_position, 0, 0, 0)
    input()
    arm.set_tool_pose(*destination_position, 0, 0, 0)
    arm.set_air_pump(WlkataMirobot.AIR_PUMP_OFF_PWM_VALUE)
    arm.set_tool_pose(*destination_approach_position, 0, 0, 0)

    arm.go_to_zero()

    print(source_position, source_approach_position)
    print(destination_position, destination_approach_position)
    move_to_neutral_position()
    exit(0)
    drop_at()
    print(rotation)
    print([1, 0, 0])
    print(rotation@[1, 0, 0])
    exit(0)
    init()
    move_n_items(4, source=destination_position, destination=source_position)
    move_n_items(4, source=source_position, destination=destination_position)
    move_to_neutral_position()

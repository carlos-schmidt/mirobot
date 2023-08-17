import sys
from time import sleep
from wlkata_mirobot import WlkataMirobot


source_position = (123, 217, 30)
destination_position = (123, -217, 30)
neutral_position = (200, 0, 300)
height_item = 30
# 创建机械臂
arm = WlkataMirobot(portname='/dev/tty.usbserial-140')


def move_to_neutral_position():
    arm.set_tool_pose(*neutral_position, 0, 0, 0)


def pick_up_at(x, y, height, item_height):
    print(f"Picking up item at (x,y,z)=({x},{y},{height + item_height})")
    move_to_neutral_position()
    arm.set_tool_pose(x, y, height + 2 * item_height, 0, 0, 0)
    arm.set_tool_pose(x, y, height + item_height, 0, 0, 0)
    sleep(.2)  # seconds
    arm.set_air_pump(WlkataMirobot.AIR_PUMP_SUCTION_PWM_VALUE)
    arm.set_tool_pose(x, y, height + 2 * item_height, 0, 0, 0)


def drop_at(x, y, height, item_height):
    print(f"Dropping item at (x,y,z)=({x},{y},{height + item_height})")
    move_to_neutral_position()
    arm.set_tool_pose(x, y, height + 2 * item_height, 0, 0, 0)
    # Stop a bit above end point (20%)
    arm.set_tool_pose(x, y, height + item_height * 1.1, 0, 0, 0)
    sleep(.2)  # seconds
    arm.set_air_pump(WlkataMirobot.AIR_PUMP_OFF_PWM_VALUE)
    arm.set_tool_pose(x, y, height + 2 * item_height, 0, 0, 0)


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
    move_n_items(4, source=destination_position, destination=source_position)
    move_n_items(4, source=source_position, destination=destination_position)
    move_to_neutral_position()

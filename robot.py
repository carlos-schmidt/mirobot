from time import sleep

from wlkata_mirobot import WlkataMirobot, WlkataMirobotTool

from util import Point, dist, translate


class Robot(WlkataMirobot):
    # allow inaccuracies of .5 millimeters and 2 degrees:
    eps = [.5, .5, .5, 2, 2, 2]

    def __init__(self, *device_args, portname=None, debug=False, connection_type='serial', autoconnect=True,
                 autofindport=True, exclusive=True, default_speed=2000, reset_file=None,
                 wait_ok=False, **device_kwargs):
        super().__init__(*device_args, portname, debug, connection_type, autoconnect,
                         autofindport, exclusive, default_speed, reset_file,
                         wait_ok, **device_kwargs)
        self.set_tool_type(WlkataMirobotTool.SUCTION_CUP)
        self.set_tool_offset(0, 0, 40)  # height of whole tool (mm)

        if self.get_status().state == 'Alarm':
            answer = input(
                "State of robot is 'Alarm'. Need to perform homing operation to be able to move. Home now? (y/n)")
            if "y" in answer:
                self.home()
            else:
                print("Not homing. Robot may not be working now!")

    def debug_print(self, str):
        if self.debug:
            print(str)

    def _safe_move(self, pos: Point) -> bool:
        self.debug_print(f"Moving to: {pos}")
        self.set_tool_pose(pos.astuple())
        status = self.get_status()
        if dist(Point(status.cartesian), pos) > self.eps:
            self.debug_print(
                f"Robot either did not execute move or moved inaccurately!\nTarget position: {pos}, actual position: {status.cartesian}")
            return False
        elif status.state != 'Idle':
            self.debug_print(
                f"Robot not in idle state but in {status.state} state!")
            return False
        else:
            return True

    def pick_up_at(self, position: Point, approach_distance, return_to_original_position: bool = False) -> bool:
        """
        Approach distance is only z axis distance as the end effector should approach the object from above because of the suction cup.

        Returns True if move was successful, False otherwise
        """

        approach_position = translate(position, 0, 0, approach_distance)

        return_pos = approach_position

        if return_to_original_position:
            return_pos = Point(self.get_status().cartesian)

        if not self._safe_move(approach_position) or not self._safe_move(position):
            return False

        self.set_air_pump(WlkataMirobot.AIR_PUMP_SUCTION_PWM_VALUE)

        if not self._safe_move(approach_position) or not self._safe_move(return_pos):
            return False

        return True

    def drop_at(self, position, approach_distance, return_to_original_position: bool = False) -> bool:
        """
        Approach distance is only z axis distance as the end effector should approach the object from above because of the suction cup.

        Returns True if move was successful, False otherwise
        """

        approach_position = translate(position, 0, 0, approach_distance)

        return_pos = approach_position

        if return_to_original_position:
            return_pos = Point(self.get_status().cartesian)

        if not self._safe_move(approach_position) or not self._safe_move(position):
            return False

        self.set_air_pump(WlkataMirobot.AIR_PUMP_OFF_PWM_VALUE)

        if not self._safe_move(approach_position) or not self._safe_move(return_pos):
            return False

        return True

    def move_object(self, from_position, from_approach_distance, to_position, to_approach_distance, *neutral_positions, return_to_original_position: bool = False):
        if not self.pick_up_at(from_position, from_approach_distance, return_to_original_position):
            return False

        for neutral_position in neutral_positions:
            if not self._safe_move(neutral_position):
                return False

        if not self.drop_at(to_position, to_approach_distance, return_to_original_position):
            return False

        return True

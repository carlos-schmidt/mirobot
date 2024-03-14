from math import sqrt
from typing import List
import numpy as np


class RobotPose:
    """Robot end effector position in 3 axis system + direction: x, y, z alpha, beta, gamma"""

    def __init__(self, x: float, y: float, z: float, a: float, b: float, c: float):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.c = c
        # Assuming base is zero. No rotation
        self.base = np.zeros(3) 

    def __init__(self, np_arr: np.ndarray):
        self.x = np_arr[0]
        self.y = np_arr[1]
        self.z = np_arr[2]
        self.a = np_arr[3]
        self.b = np_arr[4]
        self.c = np_arr[5]
        # Assuming base is zero. No rotation
        self.base = np.zeros(3) 


    def get_position(self) -> List[float]:
        return [self.x, self.y, self.z]

    def get_rotation(self) -> List[float]:
        """
        Endeffector rotation
        """
        return [self.a, self.b, self.c]

    def asnumpy(self):
        return np.asarray([self.x, self.y, self.z, self.a, self.b, self.c])

    def __sub__(self, other):
        if isinstance(other, RobotPose):
            return RobotPose(self.asnumpy() - other.asnumpy())
        else:
            raise TypeError("Both values must be of type point")

    def distance(self, other):
        """Calculate distance between self and other of type RobotPose.

        other (RobotPose): Current position
        """
        other: RobotPose = other
        return sqrt(sum([x**2 for x in (self - other).get_position()]))

    def length(self) -> float:
        return sqrt(sum([x**2 for x in self.get_position()]))

    def __repr__(self) -> str:
        return " ".join(
            [
                "X:",
                str(self.x),
                "Y:",
                str(self.y),
                "Z:",
                str(self.z),
                "A:",
                str(self.a),
                "B:",
                str(self.b),
                "C:",
                str(self.c),
            ]
        )

    def calc_trajectory(self, destination, steps: int = 1):
        destination: RobotPose = destination  # type for linting
        
        closest_point_to_base = np.asarray(destination.get_position())\
             * np.dot(np.asarray((self-destination).get_position()), self.base)


    def astuple(self):
        return (self.x,self.y,self.z,self.a,self.b,self.c)

from math import sqrt
from typing import List, Tuple
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

    def __init__(self, np: np.ndarray):
        self.x = np[0]
        self.y = np[1]
        self.z = np[2]
        self.a = np[3]
        self.b = np[4]
        self.c = np[5]
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
                self.x,
                "Y:",
                self.y,
                "Z:",
                self.z,
                "A:",
                self.a,
                "B:",
                self.b,
                "C:",
                self.c,
            ]
        )

    def calc_trajectory(self, destination, steps: int = 1):
        destination: RobotPose = destination  # type for linting
        
        closest_point_to_base = np.asarray(destination.get_position())\
             * np.dot(np.asarray((self-destination).get_position()), self.base)


    def astuple(self):
        return (self.x,self.y,self.z,self.a,self.b,self.c)

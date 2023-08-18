import numpy as np
from numpy import ndarray
from scipy.spatial.transform import Rotation as R
from wlkata_mirobot import MirobotCartesians


class Point():

    def __init__(self, x, y, z, a, b, c):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.c = c

    def __init__(self, miro_cartesians: MirobotCartesians) -> None:
        self.__init__(miro_cartesians.x, miro_cartesians.y, miro_cartesians.z,
                      miro_cartesians.a, miro_cartesians.b, miro_cartesians.c)

    def __init__(self, numpy: ndarray) -> None:
        if numpy.shape == (6):
            self.__init__(tuple(np.array(numpy)))
        else:
            raise AttributeError

    def __init(self):
        self.__init__(0, 0, 0, 0, 0, 0)

    def xyz(self):
        return np.array([self.x, self.y, self.z])

    def abc(self):
        return np.array([self.a, self.b, self.c])

    def astuple(self):
        return self.x, self.y, self.z, self.a, self.b, self.c

    def asnumpy(self):
        return np.asarray([self.x, self.y, self.z, self.a, self.b, self.c])

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.asnumpy() - other.asnumpy())
        else:
            raise TypeError("Both values must be of type point")

    def __repr__(self) -> str:
        return str([self.x, self.y, self.z, self.a, self.b, self.c])


def dist(a: Point, b: Point):
    return np.linalg.norm(a.asnumpy()-b.asnumpy())


def translate(point: Point, x, y, z):
    """
    The angles are implicitly given by the point
    """
    r = R.from_rotvec(np.pi/180*(point.abc()))
    r_inv = R.from_rotvec(-np.pi/180*(point.abc()))
    t = np.array([x, y, z])
    return Point(*(r.as_matrix() @
                   (r_inv.as_matrix() @ point.xyz()
                    + t)), *point.abc())

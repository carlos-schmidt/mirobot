class RobotPose:
    """Robot (end effector) position in 6 axis system: x, y, z alpha, beta, gamma"""

    def __init__(self, x: float, y: float, z: float, a: float, b: float, c: float):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.c = c

    def get_position(self) -> (float, float, float):
        return self.x, self.y, self.z

    def get_rotation(self) -> (float, float, float):
        return self.a, self.b, self.c

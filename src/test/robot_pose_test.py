from math import sqrt

import numpy as np
from ..model.robot_pose import RobotPose


def assert_similar(this, that, digits: int = 8):
    assert round(this, digits) == round(that, digits)


class RobotPoseTest:
    def __init__(self):
        self._test_subject = RobotPose(np.asarray([1, 2, 3, 4, 5, 6]))

    def test_distance(self):
        assert self._test_subject.distance(
            RobotPose(np.asarray([0, 0, 0, 0, 0, 0]))
        ) == sqrt(14)
        assert (
            self._test_subject.distance(
                RobotPose(np.asarray([1, 2, 3, 4, 5, 6]))
            )
            == 0
        )
        assert_similar(
            self._test_subject.distance(
                RobotPose(np.asarray([1.0001, 2.0001, 3.0001, 4, 5, 6]))
            ),
            sqrt((0.0001**2) * 3),
            10,
        )

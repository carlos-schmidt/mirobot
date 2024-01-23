from model.RobotPose import RobotPose
from math import sqrt


def assert_similar(this, that, digits: int = 8):
    assert round(this, digits) == round(that, digits)


class RobotPoseTest:
    def __init__(self):
        self._test_subject = RobotPose(1, 2, 3, 4, 5, 6)

    def test_distance(self):
        assert self._test_subject.distance(
            RobotPose(0, 0, 0, 0, 0, 0)
        ).length() == sqrt(14)
        assert self._test_subject.distance(RobotPose(1, 2, 3, 4, 5, 6)).length() == 0
        assert_similar(
            self._test_subject.distance(
                RobotPose(1.0001, 2.0001, 3.0001, 4, 5, 6)
            ).length(),
            sqrt((0.0001**2) * 3),
            10,
        )


if __name__ == "__main__":
    tester = RobotPoseTest()
    tester.test_distance()

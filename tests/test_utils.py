import time
from unittest import TestCase
from utils import distance, speed_knots

class UtilsTesting(TestCase):

    def setUp(self):
        ...

    def test_distance(self):
        res = distance((50.0359, 5.4253), (58.3838, 3.0412))
        assert res == 940.947626060444

    def test_distance2(self):
        res = distance((0,0),(0,0))
        assert res == 0
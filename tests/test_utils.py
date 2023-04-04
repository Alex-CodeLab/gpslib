import time
from unittest import TestCase
from utils import distance, speed_kn

from datetime import datetime, timedelta

class UtilsTesting(TestCase):

    def setUp(self):
        ...

    def test_distance(self):
        res = distance((50.0359, 5.4253), (58.3838, 3.0412))
        self.assertAlmostEqual(res, 940.947626060443)

    def test_distance2(self):
        res = distance((0,0),(0,0))
        assert res == 0

    def test_distance_3(self):
        latlon1 = (40.7128, -74.0060)  # New York City
        latlon2 = (37.7749, -122.4194)  # San Francisco
        expected_distance = 4129.08  # km
        calculated_distance = distance(latlon1, latlon2)
        self.assertAlmostEqual(calculated_distance, expected_distance, delta=0.01)


    def test_speed_knots(self):
        latlon1 = (40.7128, -74.0060)  # New York City
        latlon2 = (37.7749, -122.4194)  # San Francisco
        time1 = datetime(2022, 1, 1, 0, 0, 0)
        time2 = datetime(2022, 1, 5, 0, 0, 0)
        expected_speed = 23.22  # knots
        expected_kmh = 43.01  # kmh
        knots, kmh = speed_kn(latlon1, time1, latlon2, time2)
        self.assertAlmostEqual(knots, expected_speed, delta=0.01)
        self.assertAlmostEqual(kmh, expected_kmh, delta=0.01)

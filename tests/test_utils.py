from unittest import TestCase
from utils import distance, speed_kn, bearing, average_last_n
import unittest
from datetime import datetime

class UtilsTesting(TestCase):

    def setUp(self):
        ...

    def test_distance(self):
        res = distance((50.0359, 5.4253), (58.3838, 3.0412))
        self.assertAlmostEqual(res, 940.947626060443)

    def test_distance2(self):
        res = distance((0,0),(0,0))
        assert res == 0

    def test_distance3(self):
        res = distance((37.7749, -122.4194),(37.3352, -121.8813))
        self.assertAlmostEqual(res, 68.12, delta=0.1)

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



class TestBearing(TestCase):
    def test_bearing_1(self):
        # Test case 1: Coordinates of two points on a straight line (bearing should be 90 degrees)
        lat1, lon1 = 0, 0
        lat2, lon2 = 0, 1
        expected_bearing = 90
        self.assertAlmostEqual(bearing(lat1, lon1, lat2, lon2), expected_bearing, places=1)

    def test_bearing_2(self):
        # Test case 2: Coordinates of two points on a straight line (bearing should be -90 degrees)
        lat1, lon1 = 0, 1
        lat2, lon2 = 0, 0
        expected_bearing = -90
        self.assertAlmostEqual(bearing(lat1, lon1, lat2, lon2), expected_bearing, places=1)

    def test_bearing_3(self):
        # Test case 3:
        lat1, lon1 = 0, 1
        lat2, lon2 = 1, 0
        expected_bearing = -45
        self.assertAlmostEqual(bearing(lat1, lon1, lat2, lon2), expected_bearing, places=1)

    def test_bearing_4(self):
        # Test case 4: Coordinates of two points on the same meridian (bearing should be 0 degrees)
        lat1, lon1 = 0, 0
        lat2, lon2 = 1, 0
        expected_bearing = 0
        self.assertAlmostEqual(bearing(lat1, lon1, lat2, lon2), expected_bearing, places=1)

    def test_bearing_5(self):
        # Test case 5: Coordinates of two points with the same longitude (bearing should be 0 or 180 degrees)
        lat1, lon1 = 0, 0
        lat2, lon2 = 1, 0
        bearing1 = bearing(lat1, lon1, lat2, lon2)
        bearing2 = bearing(lat2, lon2, lat1, lon1)
        self.assertIn(bearing1, [0, 180])
        self.assertIn(bearing2, [0, 180])


    def test_bearing_6(self):
        # Test case 6:
        lat1, lon1 = 37.7749, -122.4194 # sanfran
        lat2, lon2 = 37.3352, -121.8813 # sanjose
        expected_bearing = 135.7
        self.assertAlmostEqual(bearing(lat1, lon1, lat2, lon2), expected_bearing, places=1)


class TestAverageLastN(unittest.TestCase):
    def test_empty_coords(self):
        coords = []
        lat, lon, dt = average_last_n(coords)
        self.assertIsNone(lat)
        self.assertIsNone(lon)
        self.assertIsNone(dt)

    def test_single_coord(self):
        coords = [(1.0, 2.0, '2022-04-07 12:00:00')]
        lat, lon, dt = average_last_n(coords)
        self.assertIsNone(lat)
        self.assertIsNone(lon)
        self.assertIsNone(dt)

    def test_two_coords(self):
        coords = [(1.0, 2.0, '2022-04-07 12:00:00'), (2.0, 4.0, '2022-04-07 13:00:00')]
        lat, lon, dt = average_last_n(coords)
        self.assertAlmostEqual(lat, 1.5)
        self.assertAlmostEqual(lon, 3.0)
        self.assertEqual(dt, '2022-04-07 13:00:00')

    def test_four_coords(self):
        coords = [
            (1.0, 2.0, '2022-04-07 12:00:00'),
            (2.0, 4.0, '2022-04-07 13:00:00'),
            (3.0, 6.0, '2022-04-07 14:00:00'),
            (4.0, 8.0, '2022-04-07 15:00:00')
        ]
        lat, lon, dt = average_last_n(coords)
        self.assertAlmostEqual(lat, 2.5)
        self.assertAlmostEqual(lon, 5.0)
        self.assertEqual(dt, '2022-04-07 15:00:00')

    def test_malformed_coords(self):
        coords = [(1.0, 2.0, '2022-04-07 12:00:00'), (2.0, 'foo', '2022-04-07 13:00:00')]
        lat, lon, dt = average_last_n(coords)
        self.assertIsNone(lat)
        self.assertIsNone(lon)
        self.assertIsNone(dt)
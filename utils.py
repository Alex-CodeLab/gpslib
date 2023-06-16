from __future__ import annotations

import math
from typing import Tuple

# Constants
A = 6378137.0  # Semi-major axis of the earth (m)
F = 1 / 298.257223563  # Flattening of the earth
B = (1 - F) * A  # Semi-minor axis of the earth (m)
L = -0.0000115  # Difference between the prime meridian and the Greenwich Meridian (degrees)
R = 6371  # radius of the Earth in kilometers
GRAVITY = 9.81  # m/s^2


def distance(latlongalt1, latlongalt2):
    # orthodromic distance in km

    lat1, lon1, *alt1 = latlongalt1
    lat2, lon2, *alt2 = latlongalt2
    alt1 = alt1[0] if alt1 else 0
    alt2 = alt2[0] if alt2 else 0
    # Convert latitudes and longitudes to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Calculate distance using Haversine formula
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c

    # Calculate altitude difference
    delta_alt = alt2 - alt1

    return math.sqrt(d ** 2 + delta_alt ** 2)


def speed(latlon1, time1, latlon2, time2):
    """Function to calculate the speed between two points in kilometers per hour"""
    d = distance(latlon1, latlon2)
    t = (time2 - time1).total_seconds() / 3600
    return d / t


def speed_kn(latlon1, time1, latlon2, time2):
    """Function to calculate the speed between two points in knots"""
    d = distance(latlon1, latlon2)
    t = (time2 - time1).total_seconds() / 3600
    kmh = d / t
    knots = kmh / 1.852
    return knots, kmh


def bearing(lat1, lon1, lat2, lon2):
    """Function to calculate the bearing between two points"""
    d_lon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    y = math.sin(d_lon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)
    return math.degrees(math.atan2(y, x))


def average_last_n(coords):
    """Calculate average of last coordinates"""
    n = len(coords)
    if n < 2:
        return None, None, None
    lat_sum = 0
    lon_sum = 0
    for i in range(-n, 0):
        try:
            lat_sum += float(coords[i][0])
            lon_sum += float(coords[i][1])
        except Exception:
            return None, None, None
    lat_avg = lat_sum / n
    lon_avg = lon_sum / n
    return lat_avg, lon_avg, coords[-1][2]


class SensorFusion:
    """
        Represents a sensor fusion object that integrates accelerometer and gyroscope data to estimate position and velocity.

    """

    def __init__(self, lat: float, lon: float, alt: float) -> None:
        """
        Initializes the SensorFusion object with initial position and velocity values.

        Args:
            lat (float): Initial latitude coordinate.
            lon (float): Initial longitude coordinate.
            alt (float): Initial altitude coordinate.

        This method sets up the SensorFusion object with the provided initial position and velocity values.
        """
        self.lat = lat
        self.lon = lon
        self.alt = alt

        self.vel_north = 0.0
        self.vel_east = 0.0
        self.vel_down = 0.0

        self.prev_time: [float| None] = None
        self.prev_accel_x: [float| None] = None
        self.prev_accel_y: [float| None] = None
        self.prev_accel_z: [float| None] = None
        self.prev_gyro_x: [float| None]= None
        self.prev_gyro_y: [float| None]= None
        self.prev_gyro_z: [float| None]= None

    def fuse_data(self, time: float, accel_x: float, accel_y: float, accel_z: float, gyro_x: float, gyro_y: float,
                  gyro_z: float) -> Tuple[float, float, float, float, float, float]:
        """
               Fuses sensor data to estimate position and velocity.
        """
        dt = time - self.prev_time if self.prev_time is not None else 0.0

        # Calculate new velocity using trapezoidal integration
        vel_north_new = self.vel_north + (accel_x + self.prev_accel_x) / 2.0 * dt
        vel_east_new = self.vel_east + (accel_y + self.prev_accel_y) / 2.0 * dt
        vel_down_new = self.vel_down + (accel_z + self.prev_accel_z) / 2.0 * dt

        # Calculate new position using trapezoidal integration
        lat_new = self.lat + (
                self.vel_north + vel_north_new) / 2.0 * dt / 111319.9  # 1 degree of latitude is approximately 111319.9 meters
        lon_new = self.lon + (self.vel_east + vel_east_new) / 2.0 * dt / (111319.9 * math.cos(self.lat))
        alt_new = self.alt - (self.vel_down + vel_down_new) / 2.0 * dt

        # Calculate new velocity using gyroscope data
        vel_north_new += self.prev_gyro_x * dt
        vel_east_new += self.prev_gyro_y * dt
        vel_down_new += self.prev_gyro_z * dt

        # Update class variables
        self.lat = lat_new
        self.lon = lon_new
        self.alt = alt_new
        self.vel_north = vel_north_new
        self.vel_east = vel_east_new
        self.vel_down = vel_down_new

        self.prev_time = time
        self.prev_accel_x = accel_x
        self.prev_accel_y = accel_y
        self.prev_accel_z = accel_z
        self.prev_gyro_x = gyro_x
        self.prev_gyro_y = gyro_y
        self.prev_gyro_z = gyro_z

        return lat_new, lon_new, alt_new, vel_north_new, vel_east_new, vel_down_new

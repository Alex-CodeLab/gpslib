import math
from math import radians, sin, cos, atan2, sqrt

# Constants
a = 6378137.0 # Semi-major axis of the earth (m)
f = 1 / 298.257223563 # Flattening of the earth
b = (1 - f) * a # Semi-minor axis of the earth (m)
L = -0.0000115 # Difference between the prime meridian and the Greenwich Meridian (degrees)


def distance(lat1, lon1, lat2, lon2):
    R = 6371  # radius of the Earth in kilometers
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + \
        math.sin(d_lon / 2) * math.sin(d_lon / 2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def speed_knots(lat1, lon1, time1, lat2, lon2, time2):
    d = distance(lat1, lon1, lat2, lon2)
    t = (time2 - time1).total_seconds()
    nautical_miles_per_second = d / t / 1852
    return nautical_miles_per_second * 3600  # knots

# Function to calculate the speed between two points in kilometers per hour
def speed(lat1, lon1, time1, lat2, lon2, time2):
    d = distance(lat1, lon1, lat2, lon2)
    t = (time2 - time1).total_seconds() / 3600
    return d / t

def speed_kn(lat1, lon1, time1, lat2, lon2, time2):
    d = distance(lat1, lon1, lat2, lon2)
    t = (time2 - time1).total_seconds()
    nautical_miles_per_second = d / t / 1852
    knots = nautical_miles_per_second * 3600
    kilometers_per_hour = d / t * 3600
    kilometers_per_hour_to_knots = kilometers_per_hour / 1.852 * 0.5399568
    return knots, kilometers_per_hour_to_knots


# Function to calculate the bearing between two points
def bearing(lat1, lon1, lat2, lon2):
    d_lon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    y = math.sin(d_lon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)
    return math.degrees(math.atan2(y, x))


def average_last_n(coords):
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

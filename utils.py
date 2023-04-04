import math

# Constants
A = 6378137.0 # Semi-major axis of the earth (m)
F = 1 / 298.257223563 # Flattening of the earth
B = (1 - F) * A # Semi-minor axis of the earth (m)
L = -0.0000115 # Difference between the prime meridian and the Greenwich Meridian (degrees)
R = 6371  # radius of the Earth in kilometers
GRAVITY = 9.81  # m/s^2

def distance(latlon1, latlon2):
    lat1, lon1 = latlon1
    lat2, lon2 = latlon2
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + \
        math.sin(d_lon / 2) * math.sin(d_lon / 2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def speed_knots(latlon1, time1, latlon2, time2):
    d = distance(latlon1, latlon2)
    t = (time2 - time1).total_seconds()
    nautical_miles_per_second = d / t / 1852
    return nautical_miles_per_second * 3600  # knots

# Function to calculate the speed between two points in kilometers per hour
def speed(latlon1, time1, latlon2, time2):
    d = distance(latlon1, latlon2)
    t = (time2 - time1).total_seconds() / 3600
    return d / t

def speed_kn(latlon1, time1, latlon2, time2):
    d = distance(latlon1, latlon2)
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


class SensorFusion:

    def __init__(self, lat, lon, alt):
        self.lat = lat
        self.lon = lon
        self.alt = alt

        self.vel_north = 0.0
        self.vel_east = 0.0
        self.vel_down = 0.0

        self.prev_time = None
        self.prev_accel_x = None
        self.prev_accel_y = None
        self.prev_accel_z = None
        self.prev_gyro_x = None
        self.prev_gyro_y = None
        self.prev_gyro_z = None

    def fuse_data(self, time, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z):
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
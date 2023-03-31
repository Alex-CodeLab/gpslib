import contextlib
from datetime import datetime

from serial import Serial
from pyubx2 import UBXReader
import logging
import signal
import sys
import zmq
import json
import math
from time import sleep
from config import tty, BAUDRATE, ipaddress
from utils import average_last_n

logging.basicConfig(filename='/var/log/gps.log', level=logging.INFO)

def signal_handler(sig, frame):
    logging.info('-- exit --')
    sys.exit(0)

"""
1   UTC of this position report, hh is hours, mm is minutes, ss.ss is seconds.
2   Latitude, dd is degrees, mm.mm is minutes
3   N or S (North or South)
4   Longitude, dd is degrees, mm.mm is minutes
5   E or W (East or West)
6   GPS Quality Indicator (non null)
    0 - fix not available,
    1 - GPS fix,
    2 - Differential GPS fix (values above 2 are 2.3 features)
    3 = PPS fix
    4 = Real Time Kinematic
    5 = Float RTK
    6 = estimated (dead reckoning)
    7 = Manual input mode
    8 = Simulation mode
7   Number of satellites in use, 00 - 12
8   Horizontal Dilution of precision (meters)
9   Antenna Altitude above/below mean-sea-level (geoid) (in meters)
10  Units of antenna altitude, meters
11  Geoidal separation, the difference between the WGS-84 earth ellipsoid and mean-sea-level (geoid), "-" means mean-sea-level below ellipsoid
12  Units of geoidal separation, meters
13  Age of differential GPS data, time in seconds since last SC104 type 1 or 9 update, null field when DGPS is not used
14  Differential reference station ID, 0000-1023
15  Checksum
<CR> Carriage return, end tag
<LF> line feed, end tag

"""


signal.signal(signal.SIGINT, signal_handler)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(f"tcp://{ipaddress}")
stream = Serial(tty, BAUDRATE, timeout=3)
ubr = UBXReader(stream, protfilter=7)


class GPS:
    msgtype = ['GN',]
    msg_ids = ['GLL', 'GGA', 'RMC']

    def __init__(self, test_data=None):
        self.spd = None
        self.coordinates = None
        print('init ....')

        self._stop = False
        self._test_data = test_data

    def start(self):
        print('start sending')
        self.coordinates, nmh, knots = [], None, None,
        while not self._stop:

            parsed_data = self.get_data()
            # print(parsed_data)
            if parsed_data and not self._test_data:
                socket.send_multipart([b'', json.dumps(parsed_data).encode('utf-8')])
            else:
                sleep(.1)


    def get_data(self):

        if self._test_data:
            # print(len(self._test_data))
            return self._test_data.pop(0)
        if stream.in_waiting:

            try:
                raw_data, parsed_data = ubr.read()
                if parsed_data.msgID == 'RMC':
                    self.spd = parsed_data.spd
                    # print(self.spd)
                if (
                        parsed_data.talker in self.msgtype
                        and parsed_data.msgID in self.msg_ids
                        and len(str(parsed_data.time).split('.')) == 1
                ):
                    today = datetime.now().strftime('%y-%m-%d')
                    ts = f'{str(parsed_data.time)} {today}'
                    dt = datetime.strptime(ts, '%H:%M:%S %y-%m-%d')
                    lat, lon, _ = average_last_n(self.coordinates)

                    if len(self.coordinates) >= 4:

                        with contextlib.suppress(Exception):
                            return self.make_gnss(parsed_data, dt)
                    else:
                        self.coordinates.append((parsed_data.lat, parsed_data.lon, dt))

            except Exception as e:
                print('ERROR:  ', e)
                logging.error(e)

    def make_gnss(self, parsed_data, dt) -> json:
        old_lat, old_lon, _ = average_last_n(self.coordinates)
        self.coordinates.append((parsed_data.lat, parsed_data.lon, dt))
        lat, lon, _ = average_last_n(self.coordinates)
        nm = haversine((old_lat, old_lon), (lat, lon), unit=Unit.NAUTICAL_MILES)
        nmh = nm * 3600
        knots = 0.5399568 * nmh

        self.coordinates.pop(0)

        return {
            'utc': str(parsed_data.time),
            'lat': lat or None,
            'lon': lon or None,
            'quality': parsed_data.quality,
            'hdop': parsed_data.HDOP,
            'altitude': parsed_data.alt,
            'knots': knots or None,
            'nmh': nmh or None,
            'spd': self.spd or None
        }
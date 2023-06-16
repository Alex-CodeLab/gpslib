#!/home/debain/gpslib/env/bin/python
"""
GPS Handler
"""
# pylint: disable=import-error, inconsistent-return-statements, useless-suppression
from __future__ import annotations

import contextlib
import json
import logging
from datetime import datetime
from time import sleep

import zmq
from haversine import haversine, Unit
from pynmeagps import NMEAMessage
from pyubx2 import UBXReader, UBXStreamError, UBXParseError, UBXMessage
from serial import Serial

from config import TTY, BAUDRATE, IPADDRESS, PORT
from utils import average_last_n

logging.basicConfig(filename='/var/log/gps.log', level=logging.INFO)


stream = Serial(TTY, BAUDRATE, timeout=3)
ubr = UBXReader(stream, protfilter=7)


class GPS:
    """
    Represents a GPS object that handles data retrieval and processing from a GPS device.

    Attributes:
        msgtype (list[str]): A list of valid message types.
        msg_ids (list[str]): A list of valid message IDs.
        spd (float): Current speed.
        coordinates (list[tuple]): A list of GPS coordinates.
        socket (zmq.Socket): ZeroMQ socket for publishing data.
        _test_data (list, optional): Test data for simulation (default: None).

    Methods:
        __init__(test_data=None): Initializes the GPS object.
        run(): Starts the GPS data sending process.
        get_data() -> tuple, optional: Retrieves GPS data.
        make_gnss(parsed_data, dt) -> dict: Creates a GNSS object.

    """

    msgtype = ['GN', ]
    msg_ids = ['GLL', 'GGA', 'RMC']

    def __init__(self, test_data: (list| None)=None):
        print('init ....')
        self.spd = None
        self.coordinates = []
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.connect(f"tcp://{IPADDRESS}:{PORT}")
        self._test_data = test_data
        self.parsed_data = None

    def run(self):
        """
        Starts the GPS data sending process.

        This method initiates the GPS data sending process. It clears the coordinates list and starts a loop to
        retrieve and process GPS data indefinitely.
        """
        print('start sending')
        self.coordinates = []
        while True:
            parsed_data = self.get_data()
            if parsed_data and not self._test_data:
                self.socket.send_multipart([b'', json.dumps(parsed_data).encode('utf-8')])
            else:
                sleep(.1)

    def get_data(self) -> [tuple| None]:
        """
        Retrieves GPS data.

        Returns:
            tuple, optional: A tuple containing the retrieved GPS data.

        This method retrieves GPS data either from the test data or from a connected device. It processes the data,
        calculates average latitude and longitude, and creates a GNSS object if enough coordinates are available.
        """
        if self._test_data:
            return self._test_data.pop(0)
        if stream.in_waiting:
            try:
                _, self.parsed_data = ubr.read()
                if self.parsed_data.msgID == 'RMC':
                    self.spd = self.parsed_data.spd
            except UBXParseError as e:
                print('ERROR:  ', e)
                logging.error(e)
            try:
                # If the parsed message is of a valid message type and message ID, and the timestamp is valid
                if self._validate_msg():
                    dt = self._make_dt()

                    # If there are at least 4 coordinates in the list, create a GNSS object
                    if len(self.coordinates) >= 4:
                        with contextlib.suppress(Exception):
                            return self.make_gnss(self.parsed_data, dt)
                    else:
                        self.coordinates.append((self.parsed_data.lat, self.parsed_data.lon, dt))

            except UBXStreamError as e:
                print('ERROR:  ', e)
                logging.error(e)

    def _validate_msg(self) -> bool:
        return (
            self.parsed_data.talker in self.msgtype
            and self.parsed_data.msgID in self.msg_ids
            and len(str(self.parsed_data.time).split('.')) == 1
        )

    def _make_dt(self) -> datetime:
        """Create timestamp"""
        today = datetime.now().strftime('%y-%m-%d')
        ts = f'{str(self.parsed_data.time)} {today}'
        return datetime.strptime(ts, '%H:%M:%S %y-%m-%d')

    def make_gnss(self, parsed_data: [UBXMessage| NMEAMessage], dt:datetime) -> json:
        """
        Creates a GNSS object.

        Args:
            parsed_data: The parsed GPS data.
            dt: The datetime object representing the timestamp of the data.

        Returns:
            dict: A dictionary containing the GNSS data.

        This method calculates the average latitude and longitude, calculates the distance traveled, and creates
        a GNSS object with relevant information.
        """
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


def main():
    gps = GPS()
    gps.run()


if __name__ == "__main__":
    main()

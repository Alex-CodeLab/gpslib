

### Application structure
There are multiple standalone programs that can 
be started separately using systemd.

(Experiments using a single Multi-processing app resulted in some (interrupt) issues and very slow sensor readings.)


- main.py :  start/stop the other programs
- imu     :  gyro sensor readings  
- gps     :  gps sensor readings
- zeromq  :  receive sensordata and send to websocket (or to network)

- utils   :  general gps, imu formulas
- kalmann :  experimental sensor-fusion filter



## Sensor Fusion

Sensor-fusion is the process of combining two or more 
data sources to get a better understanding of the system.

The datasource could be a sensor, but also a mathematical model.

SensorFusion can increase the quality of the data, 
increase reliability and can estimate unmeasured states.


Orientation (attitude, heading) can be estimated
using magnetometer, accelerometer and gyro (IMU).




## GPS message

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
    11  Geoidal separation, the difference between the WGS-84 earth ellipsoid and mean-sea-level (geoid), "-" means 
        mean-sea-level below ellipsoid
    12  Units of geoidal separation, meters
    13  Age of differential GPS data, time in seconds since last SC104 type 1 or 9 update, null field when DGPS is not used
    14  Differential reference station ID, 0000-1023
    15  Checksum
    <CR> Carriage return, end tag
    <LF> line feed, end tag
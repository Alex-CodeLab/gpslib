
[Work In Progress]

Collection of GPS/autopilot related code.


The goal of this project is to create a tillerpilot (autopilot for a 7m sailboat)
using Beagleboard Blue, a Ublox GPS module and a DC motor.

The data will be sent to the network using ZMQ. This allows navigation software (chart plotter) 
to use the data. Also, it allows the sensors or gps to be easily replaced with any 
other devices.


 

![](https://github.com/Alex-CodeLab/gpslib/blob/main/bbb_gps.jpg)

Todo:
- [x] tests
- [ ] CLI
- [x] configure magnetometer, digital compass - IMU
- [ ] dashboard



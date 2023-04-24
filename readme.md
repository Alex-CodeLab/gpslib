
[Work In Progress - Don't use.]

Collection of GPS/autopilot related code.


The goal of this project is to create a tillerpilot (autopilot for a 7m sailboat)
using Beagleboard Blue, a Ublox GPS module and a DC motor.

The data will be sent to the network using ZMQ. This allows navigation software (chart plotter) 
to use the data. Also, it allows the sensors or gps to be easily replaced with any 
other devices.


![](https://github.com/Alex-CodeLab/gpslib/blob/main/docs/img/bbb_gps.jpg)
![](https://github.com/Alex-CodeLab/gpslib/blob/main/docs/img/dashboard.png)
![](https://github.com/Alex-CodeLab/gpslib/blob/main/docs/img/darkmode.png)

Todo:
- [x] tests
- [x] CLI
- [x] configure magnetometer, digital compass - IMU
- [x] dashboard
- [x] dark mode
- [ ] connect websockets to dashboard
- [ ] Gyroscope chart
- [ ] replace FastApi with Rust (actix-web)
- [ ] install instructions



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



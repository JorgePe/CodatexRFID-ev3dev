# CodatexRFID-ev3dev
Python scripts to use Codatex RFID Sensor with ev3dev

Codatex RFID Sensor for NXT (http://www.codatex.com/lego-sensor.html) also works with the EV3 (at least with LeJOS and RobotC) but there is no driver yet for ev3dev.

The Codatex RFID sensor is an I2C device but it also needs power on pin 1. That is a problem because current I2C modes implemented by ev3dev ("nxt-i2c" and "other-i2c") don't activate pin1. Since I don't know how to create a new driver, I made an adapter cable, with a PP3 9V battery conencted to pin1 (Analog Voltage) and pin3 (Ground) of the sensor (to prevent damage I cut the first wire so no voltage reaches the EV3).

The Codatex RFID sensor has 2 reading modes:
- singleshot
- continuous

There is a script to demonstrate each of these modes and another to just get information about the sensor (like version and serial number).

Everything was based on available code from NXC, LeJOS and RobotC for NXT/EV3. Thanks for your work, guys!

- NXC:
 http://www.codatex.com/picture/upload/en/RFID_NXC_lib.zip
- LeJOS:
 https://github.com/SnakeSVx/ev3/blob/master/Lejos/src/main/java/lejos/hardware/sensor/RFIDSensor.java
- RobotC:
 http://botbench.com/driversuite/codatech-rfid_8h_source.html


Thanks also to David Lechner that corrected my first cable. Despite lots of pictures, pin2 **IS NOT** Ground.

To use the Codatex RFID Sensor:
- connect the cable adapter to one of the EV3 input ports
- configure the port for 'other-i2c' mode

NOTE: My scripts assume Input Port 1 is used.

I2C operations work fine with a normal cable so it's always possible to read Vendor, Serial Number, etc. All tag readings will return 0 and the sensor LED will never blick.

A few more details at my blog:
http://ofalcao.pt/blog/2017/codatex-rfid-sensor

A video with ev3dev reading several tags (4001 and 4120):
https://youtu.be/ONw08QqMvhc

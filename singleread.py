#!/usr/bin/env python3

__author__ = 'Jorge Pereira'

# Codatex Sensor webpage:
# http://www.codatex.com/lego-sensor.html
#
# based on previous drivers for NXT and EV3:
# NXC
# http://www.codatex.com/picture/upload/en/RFID_NXC_lib.zip
#
# LeJOS
# https://github.com/SnakeSVx/ev3/blob/master/Lejos/src/main/java/lejos/hardware/sensor/RFIDSensor.java
#
# RobotC
# http://botbench.com/driversuite/codatech-rfid_8h_source.html

from smbus import SMBus
from time import sleep
from codecs import encode

# We assume Codatex sensor at Input Port 1
# and the port previously initialized to "other-i2c" mode
IN1_I2CBUS = 3

CODATEX_ADDRESS = 0x02    # I2C Address of the Codatex sensor

# Codatex Registers
CODATEX_VERSION = 0x00    # Read - Version = "V1.0"
CODATEX_VENDOR  = 0x08    # Read - Vendor = "CODATEX"
CODATEX_TYPE    = 0x10    # Read - Type = "RFID"
CODATEX_COMMAND = 0x41    # Write - Command
CODATEX_TAGID   = 0x42    # Read - TagID
CODATEX_SERIAL  = 0xA0    # Read - Serial Number

# Codatex Commands
CMD_SINGLE = 0x01  # Single shot read
CMD_CONTIN = 0x02  # Continuous read
CMD_INITFW = 0x83  # Initialize firmware (normal operation)
CMD_BTLDR  = 0x81  # Start bootlader

# Data Sizes
LEN_TYPE   = 8
LEN_VENDOR = 8
LEN_VERS   = 5
LEN_SERIAL = 4     # Codatex document says 16 but last 12 seems all 0xFF
LEN_TAGID  = 5

# Some of these timings can be reduced a bit but let's use the same as LeJOS
DELAY_WAKEUP = 0.005
DELAY_FIRMWARE = 0.100
DELAY_ACQUIRE = 0.250
DELAY_READ = 0.200

# This is just empiric
DELAY_LOOP = 0.025

####

bus = SMBus(IN1_I2CBUS)

# LeJOS does a single shot read after init
# probably not needed
#bus.write_quick(CODATEX_ADDRESS)
#sleep(DELAY_WAKEUP)
#bus.write_byte_data(CODATEX_ADDRESS,CODATEX_COMMAND,1)
#sleep(DELAY_ACQUIRE)
#bus.write_quick(CODATEX_ADDRESS)
#sleep(DELAY_WAKEUP)
#print("First Read:", bus.read_i2c_block_data(CODATEX_ADDRESS,CODATEX_TAGID,LEN_TAGID) )

#wakeup
bus.write_quick(CODATEX_ADDRESS)
sleep(DELAY_WAKEUP)

type = bus.read_i2c_block_data(CODATEX_ADDRESS,CODATEX_TYPE,LEN_TYPE)
vendor = bus.read_i2c_block_data(CODATEX_ADDRESS,CODATEX_VENDOR,LEN_VENDOR)
version = bus.read_i2c_block_data(CODATEX_ADDRESS,CODATEX_VERSION,LEN_VERS)

#wakeup and init bootloader to read Serial Number
bus.write_quick(CODATEX_ADDRESS)
sleep(DELAY_WAKEUP)
bus.write_byte_data(CODATEX_ADDRESS,CODATEX_COMMAND,CMD_BTLDR)
sleep(DELAY_FIRMWARE)
serial=bus.read_i2c_block_data(CODATEX_ADDRESS,CODATEX_SERIAL,LEN_SERIAL)

print('Type:', bytes(type).decode('utf-8'))
print('VendorId:',bytes(vendor).decode('utf-8'))
print('Version:',bytes(version).decode('utf-8'))
print('Serial:',encode(bytes(serial),'hex'))

#wakeup and init firmware for normal operation
bus.write_quick(CODATEX_ADDRESS)
sleep(DELAY_WAKEUP)
bus.write_byte_data(CODATEX_ADDRESS,CODATEX_COMMAND,CMD_INITFW)
sleep(DELAY_FIRMWARE)

# From Daniele Benedettelli NXC
# probably not needed
#sleep(2)

while True:

    #wakeup
    bus.write_quick(CODATEX_ADDRESS)
    sleep(DELAY_WAKEUP)

    #read single shot mode
    bus.write_byte_data(CODATEX_ADDRESS,CODATEX_COMMAND,CMD_SINGLE)
    sleep(DELAY_ACQUIRE)

    #wakeup again
    #probably not needed
#    bus.write_quick(0x02)
#    sleep(DELAY_WAKEUP)

    #read tag ID
    tagid = bus.read_i2c_block_data(CODATEX_ADDRESS,CODATEX_TAGID,LEN_TAGID)
    if tagid == [0,0,0,0,0]:
        print("No Tag found")
    else:
       # Just to compare with LeJOS long format of TagID
       tagid_LeJOS = tagid[0] \
                     + tagid[1]*256 \
                     + tagid[2]*65536 \
                     + tagid[3]*16777216 \
                     + tagid[4]*4294967296
       print("Tag ID:", tagid, "(LeJOS:", tagid_LeJOS, ")")

    # some delay is needed before next read
    # but much less than LeJOS
#    sleep(DELAY_READ)
    sleep(DELAY_LOOP)

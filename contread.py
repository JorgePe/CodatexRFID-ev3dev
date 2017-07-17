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
# https://github.com/SnakeSVx/ev3/blob/master/Lejos/src/main/java/lejos/hardwar$
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
CODATEX_STATUS  = 0x32    # Read - Tag Acquired = 0/1
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

####

bus = SMBus(IN1_I2CBUS)

#wakeup and init firmware for normal operation
bus.write_quick(CODATEX_ADDRESS)
sleep(DELAY_WAKEUP)
bus.write_byte_data(CODATEX_ADDRESS,CODATEX_COMMAND,CMD_INITFW)
sleep(DELAY_FIRMWARE)

#read continuous mode
bus.write_byte_data(CODATEX_ADDRESS,CODATEX_COMMAND,CMD_CONTIN)
sleep(DELAY_ACQUIRE)

while True:

    #wakeup
    bus.write_quick(CODATEX_ADDRESS)
    sleep(DELAY_WAKEUP)

    if bus.read_byte_data(CODATEX_ADDRESS,CODATEX_STATUS) == 0 :
       bus.write_byte_data(CODATEX_ADDRESS,CODATEX_COMMAND,CMD_CONTIN)
       sleep(DELAY_ACQUIRE)

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

    sleep(DELAY_READ)

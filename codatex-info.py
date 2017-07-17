#!/usr/bin/env python3

__author__ = 'Jorge Pereira'

from codatex import *
from smbus import SMBus
from time import sleep
from codecs import encode

# Assume Codatex sensor at Input Port 1
# and the port previously initialized to "other-i2c" mode
IN1_I2CBUS = 3

bus = SMBus(IN1_I2CBUS)

#wakeup and init firmware
bus.write_quick(CODATEX_ADDRESS)
sleep(DELAY_WAKEUP)
bus.write_byte_data(CODATEX_ADDRESS,CODATEX_COMMAND,CMD_INITFW)
sleep(DELAY_FIRMWARE)

# read Type, Vendor and version
type = bus.read_i2c_block_data(CODATEX_ADDRESS,CODATEX_TYPE,LEN_TYPE)
vendor = bus.read_i2c_block_data(CODATEX_ADDRESS,CODATEX_VENDOR,LEN_VENDOR)
version = bus.read_i2c_block_data(CODATEX_ADDRESS,CODATEX_VERSION,LEN_VERS)

#wakeup and init bootloader to read Serial Number
bus.write_quick(CODATEX_ADDRESS)
sleep(DELAY_WAKEUP)
bus.write_byte_data(CODATEX_ADDRESS,CODATEX_COMMAND,CMD_BTLDR)
sleep(DELAY_FIRMWARE)
serial=bus.read_i2c_block_data(CODATEX_ADDRESS,CODATEX_SERIAL,LEN_SERIAL)

print('Type:    ', bytes(type).decode('utf-8'))
print('VendorId:', bytes(vendor).decode('utf-8'))
print('Version: ', bytes(version).decode('utf-8'))
print('Serial:  ', (encode(bytes(serial),'hex')).decode("utf-8"))

#wakeup and re-init firmware
bus.write_quick(CODATEX_ADDRESS)
sleep(DELAY_WAKEUP)
bus.write_byte_data(CODATEX_ADDRESS,CODATEX_COMMAND,CMD_INITFW)
sleep(DELAY_FIRMWARE)

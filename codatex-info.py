#!/usr/bin/env python3

__author__ = 'Jorge Pereira'

from codatex import *
from smbus import SMBus

# Assume Codatex sensor at Input Port 1
# and the port previously initialized to "other-i2c" mode
IN1_I2CBUS = 3
bus = SMBus(IN1_I2CBUS)

#wakeup and init firmware
codatex_initfw(bus)

# read fimwware information
print('Type:    ', codatex_type(bus))
print('VendorId:', codatex_vendor(bus))
print('Version: ', codatex_version(bus))
print('Serial:  ', codatex_sn(bus))

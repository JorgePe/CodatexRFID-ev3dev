#!/usr/bin/env python3

__author__ = 'Jorge Pereira'

from codatex import *
from smbus import SMBus

# Just to compare with LeJOS long format of TagID
def taglongid(tagid):
    tagid_long = tagid[0] \
                 + tagid[1]*256 \
                 + tagid[2]*65536 \
                 + tagid[3]*16777216 \
                 + tagid[4]*4294967296
    return tagid_long

# We assume Codatex sensor at Input Port 1
# and the port previously initialized to "other-i2c" mode
IN1_I2CBUS = 3
bus = SMBus(IN1_I2CBUS)

#wakeup and init firmware
codatex_initfw(bus)

#read continuous mode
codatex_continuous(bus)
sleep(DELAY_ACQUIRE)

while True:

    #wakeup
    codatex_wakeup(bus)

    if codatex_status(bus) == 0 :
        codatex_continuous(bus)
        sleep(DELAY_ACQUIRE)

    #read tag ID
    tagid = codatex_tagid(bus)

    if tagid == [0,0,0,0,0]:
        print("No Tag found")
    else:
        print("Tag ID:", tagid, "(LeJOS:", taglongid(tagid), ")")

    sleep(DELAY_READ)


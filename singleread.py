
#!/usr/bin/env python3

__author__ = 'Jorge Pereira'

from codatex import *
from smbus import SMBus

# We assume Codatex sensor at Input Port 1
# and the port previously initialized to "other-i2c" mode
IN1_I2CBUS = 3
bus = SMBus(IN1_I2CBUS)

#wakeup and init firmware
codatex_initfw(bus)

# This is just empiric
DELAY_LOOP = 0.025

while True:

    #wakeup
    codatex_wakeup(bus)

    #singleshot mode read
    codatex_singleshot(bus)
    sleep(DELAY_ACQUIRE)

    #read tag ID
    tagid = codatex_tagid(bus)
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

    sleep(DELAY_LOOP)

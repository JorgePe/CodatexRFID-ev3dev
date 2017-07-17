# Assume Codatex sensor at Input Port 1
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

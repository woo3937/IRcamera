# appending quick2wire to the path. must be named right, in the proper location!
import sys
sys.path.append('/home/pi/temp.rpi/quick2wire-python-api')

# i2c is the interface that talks between the rpi and IR sensor
import quick2wire.i2c as i2c
import time


bus = i2c.I2CMaster(1)
address = 0x5A
command = 0x07

while True:
    f = i2c.writing_bytes(address, command)
    g = i2c.reading(address, 2)
    a = bus.transaction(f, g)
    time.sleep(1e-5)



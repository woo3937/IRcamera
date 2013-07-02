import smbus
import time
bus = smbus.SMBus(1)

address = 0x5a
command = 0x25
lsb = 0x74
msb = 0xb4
pec = 0x70
nada = 0xff
n = 0

time.sleep(0.1)
bus.pec = True
#bus.write_block_data(address, command, [lsb, msb, pec])
bus.write_byte_data(address, command, lsb)
bus.write_byte_data(msb, pec, nada)
time.sleep(0.1)
print "Success!"







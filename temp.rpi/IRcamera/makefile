# gcc steppers.c IRcamera.c
#   compiles those two files together
# -o IRcamera
#   puts the output to IRcamera
# -l bcm2835
#   links to the library bcm2835, the i2c library
# -std=c99
#   use modern C
# -lm
#   link to the math library
# -lphidget21
#   link to the phidget library, for controlling the stepper motors
# -lrt
#   I just got rid of this
all:
	gcc brain.c steppers.c IRcamera.c -o IRcamera -l bcm2835 -std=c99  -lm  -lphidget21



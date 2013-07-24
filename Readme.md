This is a single pixel infa-red camera. Normally, IR cameras are in the range
4,000 -- 40,000 dollars. This camera costs ~400 dollars, and takes a not long
(unknown) time to capture an image. Examples will be shown on this page at a
later date.

This project is based off the instructions at [cheap-thermocam.tk][1]. These
instructions aren't very good, and many of the links are dead. Since I find that
frustrating, some better instructions are below. 

Raspberry Pi Project
====================
I started off with the Arduino, but it didn't even make enough RAM to hold the
entire image. I moved to the RPi, which has 250,000x the RAM. I also moved to
more accurate motors, as the servos were horribly inaccurate.

The parts list for this project:

| Part                      | Number   | Total Price   |
| ----------------          | -------- | ------------- |
| [RPi][rpi]                | 1        | 35            |
| [IR sensor][ir]           | 1        | 35            |
| [Driver boards][driver]   | 2        | 200           |
| [Stepper motors][stepper] | 2        | 70            |
| Total                     |          | 340           |

Also, the comments in the project on the RPi (`temp.rpi/IRcamera`) are
wonderfully accurate and complete. I hate bad documentation, and am trying to
write good docs.

#### Pysical Directions
1. Look at the comments at the top of `IRcamera.c` (in `temp.rpi/IRcamera` as
   of 2013-7-24) to determine where to wire SDA/SCK/Vdd/GND, and where those pins
   are on the IR sensor.
2. Make a motor controller that allows the motor to rotate in two dimensions. I
   had our department's machine shop make ours. On the final camera, the sensor
   will go on the disk on the upper motor.
   ![a shot of the motor setup][./motors.jpg?raw=true]


Ardino Project
================
To run a cheap version of the thermocam, use (possibly with some modification)
`IRcamera.ino` in the main folder. For parts, get
* [IR Sensor][ir3accurate]
* [Arduino Uno R3][arduino]
* SD card and [SD card shield][SD]
* [Pan tilt brackets][pan]
* [Servos][servos]
* breadboard, wires, superglue, etc (you probably have it already)

This Arduino writes images to the SD card in the simplest RGB format available
(PPM). To do that, you'll need a good PPM viewer. For the Mac, look at
[Xee][xee] (I downloaded it from [here][free-xee], and I didn't get a license).



#### Physical Directions
1. Look in the comments of `IRcamera.ino` for the directions.


Bugs
===================================

I'm writing down all the painfully hard to resolve bugs I find so I don't have
to go through the whole process of figuring it out again.

#### RPi and Internet
I could SSH into the RPi simply by joining the University's network (the
unprotected one) and sharing my internet via a USB-ethernet cable I bought.







[1]:http://www.cheap-thermocam.net/old-version/
[servos]:https://www.sparkfun.com/products/9065
[pan]:https://www.sparkfun.com/products/10335
[arduino]:https://www.sparkfun.com/products/11021
[ir3accurate]:http://www.futureelectronics.com/en/technologies/semiconductors/analog/sensors/temperature/Pages/3003055-MLX90614ESF-DCI-000-TU.aspx?IM=0
[SD]:https://www.sparkfun.com/products/9802
[header]:http://en.wikipedia.org/wiki/Pin\_header
[picture]:https://raw.github.com/scottsievert/IRcamera/master/pan-tilt-brackets.jpg
[i2cmaster]:homepage.hispeed.ch/peterfleury/avr-software.html
[thread]:http://forum.arduino.cc/index.php/topic,21317.0.html
[stepper]:http://www.phidgets.com/products.php?category=23&product_id=3317_1

[driver]:http://www.phidgets.com/products.php?product\_id=1067
[ir]:http://www.futureelectronics.com/en/technologies/semiconductors/analog/sensors/temperature/Pages/3003055-MLX90614ESF-DCI-000-TU.aspx?IM=0
[rpi]:http://www.raspberrypi.org
[motors]:https://raw.github.com/scottsievert/IRcamera/master/motors.jpg


[xee]:http://xee.c3.cx
[free-xee]:https://www.macupdate.com/app/mac/19978/xee

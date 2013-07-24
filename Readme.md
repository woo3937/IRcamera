This is a single pixel infa-red camera. Normally, IR cameras are in the range
4,000-40,000 dollars. This camera costs ~100 dollars, and takes a not long
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
1. To wire the Arduino and SD card together, and to make the SD card available
   to the Arduino, simply connect all of the output pins (the pins on the side
   with the names) to the Arduino output pins using a [header][header]
   connector.

2. To arrange the servos and tilt brackets, place the tilt brackets oppisite
   each other, so the two holes on the two tabs align. Then, screw in one servo
   on the "top" (oppisite the directions the tabs are facing). For the other
   servo, first connect it with the connector that came with the pan tilt
   brackets. After that, screw in the other servo so it rotates in a
   perpendicular direction from the other servo. You're going to mount the IR
   sensor on top of this, so it can rotate in both the horizontal and vertical
   directions.

   That description is best shown with a picture, even though I'm not all the
   way doing that yet (if it's past June 2013, please tell me to fix it). The
   pictures are included in the `example-photo-tilt-brackets` folder.

3. Servos operate by reading in a PWM signal, and go to that value. For example,
   if you put out a PWM signal of 50%, the servo would go to the location range
   of motion * 0.50. In my case, the servos can read values between 0 and 255,
   so 170 * X / 255, where X is the duty cycle you set with analogWrite (see
   gotoPixel for more info) or 127 for the above example. 

4. Following [this thread][thread] on the forums (and the comment by
   SensorJunkie a ways down), I connected 3.3V and ground to the corresponding
   pins (datasheet time!) on the IR sensor, analog pin 4 to SDA and analog pin 5
   to SCK. SCL is the pin closest to the tab, on the right side (bottom view!),
   and goes to pin 5. SDA is the pin on the bottom right side (bottom view!),
   and is connected to pin 4.

5. I downloaded `i2cmaster.h` from [this website][i2cmaster], and renamed
   `twimaster.c` to `twimaster.cpp`. Yes, I know it sounds weird -- I think it's
   something to do with how the Arduino IDE defines functions. If I didn't do
   it, I got errors about having duplicate functions defined. 
   
6. If you're using an Arduino with a different clock frequency, you have to
   include the lines (untested!)
   `#ifndef F_CPU` `#define F_CPU 16000000UL` `#endif` `/* I2C clock in Hz */`
   `#define SCL_CLOCK 50000L`


Bugs
===================================

I'm writing down all the painfully hard to resolve bugs I find so I don't have
to go through the whole process of figuring it out again.

#### RPi and Internet
Add `nameserver 8.8.8.8` to `/etc/resolv.conf`. So simple. I went through a long
process where it would connect just fine at my apartment, where there were no
restrictions. At the University, where there are restrictions, it didn't work.







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


[xee]:http://xee.c3.cx
[free-xee]:https://www.macupdate.com/app/mac/19978/xee

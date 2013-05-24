This is a single pixel infa-red camera. Normally, IR cameras are in the range
4,000-40,000 dollars. This camera costs ~100 dollars, and takes a not long
(unknown) time to capture an image. Examples will be shown on this page at a
later date.

This project is based off the instructions at [cheap-thermocam.tk][1]. These
instructions aren't very good, and many of the links are dead. Since I find that
frustrating, some better instructions are below.


Parts List
=========
* [IR Sensor][iraccurate]
* [Arduino Uno R3][arduino]
* SD card and [SD card shield][SD]
* [Pan tilt brackets][pan]
* [Servos][servos]
* breadboard, wires, superglue, etc (you probably have it already)

Physical Directions
===================
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
   way doing that yet (if it's past June 2013, please tell me to fix it): ![picture][picture]


[1]:http://www.cheap-thermocam.net/old-version/
[servos]:https://www.sparkfun.com/products/9065
[pan]:https://www.sparkfun.com/products/10335
[arduino]:https://www.sparkfun.com/products/11021
[ir3accurate]:http://www.futureelectronics.com/en/technologies/semiconductors/analog/sensors/temperature/Pages/3003055-MLX90614ESF-DCI-000-TU.aspx?IM=0
[SD]:https://www.sparkfun.com/products/9802
[header]:http://en.wikipedia.org/wiki/Pin\_header
[picture]:https://raw.github.com/scottsievert/IRcamera/master/pan-tilt-brackets.jpg

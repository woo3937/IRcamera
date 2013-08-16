from pylab import *

ion()

x = arange(4)
y = arange(4)
x, y = meshgrid(x, y)

for i in arange(5)+1:
    z = x*i + y**i
    imshow(z)
    draw()

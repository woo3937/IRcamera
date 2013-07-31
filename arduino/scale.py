from __future__ import division
from pylab import *
from scipy.optimize import curve_fit
from sympy import *

x = var('x')
a = 2.4e-1
center = 30
f = 255 / (1 + e**(-(x-center) * a))

figure()
plot(f, (x, 0, 60))
show()


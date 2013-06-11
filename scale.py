from __future__ import division
from pylab import *
from scipy.optimize import curve_fit
from sympy import *

#color = array([0, 85, 170, 255])
#temp = array([20, 60, 100, 150])

##plot(color, temp)

#def fit(x, a, b, c):
    #step = 1/(1 + e**(-a*(x-30)))
    #color = 255*step
    #return color


#popt, pcov = curve_fit(fit, color, temp)
#print popt
#x = arange(0, 200)
#plot(x, fit(x, *popt))



#figure()
#x = arange(20, 150)
#plot(x, fit(x, *popt))
#show()


x = var('x')
a = 3.8e-1
f = 255 / (1 + e**(-(x-30) * a))

figure()
plot(f, (x, 20, 40))
show()


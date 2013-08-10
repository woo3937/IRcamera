from __future__ import division
from pylab import *





# for an approx of the image
# Notes:
#   the base functions are defined first, and should probably be in their own
#   script. the base functions are i/dwt, i/dwt2, i/dwt2_full -- they're just
#   functions to put the image in a sparse (wavelet) domain.

#   I solely declared them early on to call them later, in IST and ISTreal.
#   Here, I use IST to time in the notebook (in this same folder) and ISTreal
#   as my callable function (you can change iterations/sampling rate/cut off
#   value).

# Some notes on notation and variable names, in ISTreal:
#   cut:    this is the cut off value that is done for iterative soft
#           thresholding. everything below this value is set to 0
#   I:      Our original image/signal.
#   rp:     Our random permuatation of indicies, to ensure random sampling. If we
#           had [1,2,3,4], rp would be [3,1,2,4]
#   tn1:    Stands for t_{n+1} (explained elsewhere, I'm sure)
#   xold1:  Stands for xold_{n-1}
#   ys:     Our sampled measurements
#   y:      Our measurements
#   p:      Our sampling rate

# What IST actually does:
#   The equation for IST is 

from pylab import *
import pywt
import random

def dwt(x):
    y = zeros_like(x)
    l = int(len(x)/2)
    i = arange(l, dtype=int)
    y[i] = x[2*i] + x[2*i + 1]
    y[i+l] = x[2*i] - x[2*i + 1]
    y = y / sqrt(2)
    return y

def dwt2(x):
    y = x.copy()
    w = y.shape[0]
    i = arange(w, dtype=int)
    y = dwt(y[i])
    y = rot90(y, 3)
    y = dwt(y[i])
    y = fliplr(y).T
    return y

x = arange(64).reshape(8,8)

def dwt2_order(s, order):
    # order means how many places width is shifted over: the bottom of the
    # "approx" image
    x = s*1.0
    width  = len(x[0,:])
    height = len(x[:,0])
    for k in range(0, order):
        # do it on each row and column
        y = x[0:width>>k, 0:width>>k]
        y = dwt2(y)
        x[0:width>>k, 0:width>>k] = y
    return x

def dwt2_full(x):
    order = int(log2(len(x)))
    return dwt2_order(x, order)

def idwt(x):
    l = int(len(x)/2)
    y = zeros_like(x)
    i = arange(l, dtype=int)
    y[2*i] = x[i] + x[i+l]
    y[2*i+1] = x[i] - x[i+l]
    y = y / sqrt(2)
    return y


def idwt2(x):
    y = x.copy()
    w = y.shape[0]
    i = arange(w)
    y = idwt(y[i])
    y = rot90(y, 3)
    y = idwt(y[i])
    y = fliplr(y).T
    y = np.round(y)
    return y

def idwt2_order(x, order):
    """ assumes x is 2D"""
    x = np.asarray(x)
    x = 1.0*x
    w, l = x.shape
    w, l = int(w), int(l)
    for i in range(order, 0, -1):
        y = x[0:w>>i-1, 0:l>>i-1]
        y = idwt2(y)
        x[0:w>>i-1, 0:l>>i-1] = y
    return x

def idwt2_full(x):
    order = int(log2(len(x)))
    return idwt2_order(x, order)


N = 16
p = 0.42
# setting up our coeffecient mctrix

x = zeros(N)
x[N/2:N/1] = 1
x[N/2-1] = 0.75
x[N/2-2] = 0.5



# make y some random components of x, and make it power of 2. keep track of the
# indicies as well
seed(42)
i = rand(N) < p
y = x[i]
ind = array(where(i==False))

# depends on seed()! for 2**n!
yW = dwt(y)
xW = dwt(x)



plot(x, marker='o')
show()

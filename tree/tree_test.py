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




def FISTA_1D(samples, locations, n, its=100, p=0.5, cut=6, draw=False):
    """ 
    n === size of full signal
    samples === sampled locations
    locations === the location of those samples
    """
    sz = (n,)
    y = samples

    xold = zeros(sz);
    xold1 = zeros(sz);
    tn = 1;
    for i in arange(its):
        tn1 = (1 + sqrt(1 + 4*tn*tn))/2;
        xold = xold + (tn-1)/tn1 * (xold - xold1)
        
        t1 = idwt_full(xold);
        temp = t1.flat[locations];
        temp2 = y - temp;

        temp3 = zeros(sz);
        temp3.flat[locations] = temp2;
        temp3 = dwt_full(temp3);

        temp4 = xold + temp3;
        xold = temp4;


        j = abs(xold) < cut
        xold[j] = 0
        j = abs(xold) > cut
        xold[j] = xold[j] - sign(xold[j])*cut
      
        
        xold1 = xold
        xold = xold
        tn = tn1
        

    return xold

def haarMatrix(n):
    """ 
    assumes n is to make a haar matrix for signal of size n
        found at google: "make haar matrix"
        n=WidthOfSquareMatrix; % copy the parameter

        % check input parameter and make sure it's the power of 2
        Level=log2(n);
        if 2^Level<n, error('please ensure the value of input parameter is the power of 2');end 

        %Initialization
        H=[1];
        NC=1/sqrt(2);%normalization constant
        LP=[1 1]; 
        HP=[1 -1];

        % iteration from H=[1] 
        for i=1:Level
            H=NC*[kron(H,LP);kron(eye(size(H)),HP)];
        end
        HaarTransformationMatrix=H;
    """
    level = log2(n)
    nc = 1/sqrt(2)
    h = array([1])
    lp = array([1, 1])
    hp = array([1, -1])
    for i in arange(level):
        fir = kron(h, lp)
        sec = kron(eye(h.shape[0]), hp)
        h = nc * vstack((fir, sec))
    #h = h / sqrt(8)
    #h = h/4.0
    return h


def dwt_full(x):
    order = log2(len(x))
    n = len(x)
    y = x.copy()
    y = asarray(y, dtype=float)
    for i in arange(order):
        i = int(i)
        y[0:n>>i] = dwt(y[0:n>>i])
    return y

def idwt_full(x):
    order = log2(len(x))
    n = len(x)
    y = x.copy()
    y = asarray(y, dtype=float)
    for i in arange(order-1, -1, -1):
        i = int(i)
        y[0:n>>i] = idwt(y[0:n>>i])
    return y

def findIndiciesForHaar(n):
    """ assumes n dimensional haar wavelet
    returns what indicies are used at those locations"""
    #i = arange(n, dtype=int)
    re = zeros(n, dtype=object )

    h = haarMatrix(n)
    row, col = where(h != 0)
    # we don't care about the rows -- always 0...n

    # row, seperate the cols by row
    for i in arange(n):
        j = where(row == i)
        re[i] = col[j]

    #for i in arange(len(re)):
        #re[i] = tuple(re[i])
    #re = tuple(re)
    return re


seed(4)
#n = 32
#maxx = 3
#t = linspace(0, maxx, num=n)

#x = 1 / (1 + exp(-50 * (t-2)))
#plot(x, marker='o')
#show()

#wavletIndicies = findIndiciesForHaar(n)

#t = 1e-3
#p = 0.2
#sam = array(around(rand(n) - 0.5 + p), dtype=bool)
#i = arange(n)
#for level in arange(log2(len(x)))+1:
    #print level
    #w = approxWavelet(x, sam)

    ## see where the wavelet is not zero. approximate closer to there

#plot(sam, marker='o')
#show()

#plot(dwt_full(x))
#plot(w)
#show()

x = 1 / (1 + exp(-50 * (t-2)))

#def approxWavelet(x, level):
""" 
    approximates the haar wavelet transform of x at location sam.
    sam -- boolean array of to index x
    x   -- numerical
"""
# it should be at a level
# setting the "level" -- 2**level indicies
j = arange(n)

# find the haar matrix
h = haarMatrix(n)
# getting x = h w
h = asmatrix(h)
h = h.T

# delete columns -- find an approximation
indd = j[logical_not(sam)]
j = asmatrix( delete(h, indd, axis=1))

f = (j.T * j).I * j.T

x = asmatrix(x)
x.shape = (-1,1)

# an exact approximation of the wavelet coeffs. of x!
w = f * x
    #return w

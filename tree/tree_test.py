
"""
COPYRIGHT BY SparKEL Lab, University of Minnesota
DIRECTOR OF LAB: Jarvis Haupt (jdhaupt@umn.edu)
CREATOR OF SCRIPT: Scott Sievert (sieve121@umn.edu)

This script does edge detection, and finds the interested parts of an image. It
looks for the edges in an image, because that's the interesting part of an
image. The other areas, the "flat" areas, can be approximated with just a
couple samples.
"""


from __future__ import division
from pylab import *
import pywt
import random

# a c-style '#define'
PRINT = True

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

def haarMatrix(n, level=-1):
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
    if level == -1: level = log2(n)
    #level = log2(n)
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

############################################################
############ BEGINNING OF 1D CASE FUNCTIONS ################
############################################################


def findIndiciesForHaar(n):
    """ assumes n dimensional haar wavelet
    returns what indicies are used at those locations"""
    #i = arange(n, dtype=int)
    re = zeros(n, dtype=object )
    re = zeros((n, n))

    h = haarMatrix(n)
    row, col = where(h != 0)
    # we don't care about the rows -- always 0...n

    # row, seperate the cols by row
    for i in arange(n):
        j = where(row == i)
        re[i] = hstack((col[j], zeros(len(re[i])-len(col[j]))-1))

    return re

def findElement(array, error_value):
    idx = -1
    while idx == -1:
        idx = array[np.random.randint(0, n)]
    return idx

def approxWavelet(x, sampleAt, m):
    """
        x: the original signal
        sampleAt: where we should sample
        m: how many terms to get (Haar: 2**level)
    """
    # h as in x = h w
    n = x.shape[0]
    h = haarMatrix(n)
    h = asmatrix(h); h = h.I
    x = asmatrix(x).reshape((-1,1))


    h = asmatrix(h); 

    j = arange(0, n)
    toDelete = logical_not(sampleAt)
    h = delete(h, j[j >= m], axis=1)

    h = delete(h, j[toDelete], axis=0)

    h = h.I
    w = h * x[sampleAt]

    approx = zeros_like(x)
    approx[0:len(w)] = w
    return approx

def oneD():
    np.random.seed(42)
    seed(42)

    # the size of our signal
    n = 2**11

    # wavelet above this term are looked at closer
    threshold = 0.2

    # how far down the wavelet "tree" should we approximate?
    levelA = 8

    # the maximum time value?
    maxx = 5

    # how many samples do we want to take to better approximate the wavelet?
    maxNumber = 7

    # initially, take "everyOther" sample.
    everyOther = 2**9

    # making our signal
    t = linspace(0, maxx, num=n)
    x  = 1 / (1 + exp(500 * (t - maxx*1/4)**2))
    x += 1 / (1 + exp(500 * (t - maxx*3/4)**2))
    x += 1 / (1 + exp(500 * (t - maxx*2/4)**2))




    # select random indicies from this
    haarToTimeInd = findIndiciesForHaar(n)
    haarToTimeInd = asarray(haarToTimeInd, dtype=int)

    # sam is "where we want to SAMple at
    sam = zeros(n, dtype=bool)
    sam[::everyOther] = True



    for level in arange(levelA):
        if PRINT: print level

        # approximate the wavelet with the terms we sample at
        w = approxWavelet(x, sam, 2**level)

        j = argwhere(abs(asarray(w).reshape(-1,)) > threshold)

        # we have the indicies where it's off (in the wavelet domain)
        k = unique(clip(j, 2**(level-1), 2**(level)))

        k = asarray(k, dtype=int)
        if PRINT: print k
        for element in haarToTimeInd[k]:
            if 0 in element and level > 2: 
                continue
            totalNumber = 0
            while totalNumber < maxNumber:
                idx = findElement(element, -1)
                sam[idx] = True
                totalNumber += 1



    w = asarray(w); w.shape = (-1,)
    error = abs(x - idwt_full(w))




    ########################################################################
    ########################### PLOTTING ###################################
    ########################################################################

    perc = 100 * len(sam[sam==True])/n
    ind = arange(n)
    wA = asarray(w).reshape(-1,)


    fig, ax1 = subplots()
    ax2 = ax1.twinx()

    # plot
    ax1.plot(ind, idwt_full(w), 'g')
    ax1.plot(ind, x, 'r--')
    ax1.set_xlabel('\\textrm{Index}')
    junk, y = ax1.get_ylim()
    ax1.set_ylim(0, 1.2*y)

    # plot
    ax2.hist(ind[sam], bins=15,label='\\textrm{Samples per index range}',\
            ls='dashed', histtype='step')
    ax2.legend(loc='best')
    ax2.set_ylabel('\\textrm{Frequency}')
    junk,current_y = ax2.get_ylim()
    ax2.set_ylim(0, 1.2*current_y)

    ti = 'Reconstruction after sampling at {:.1f}\% rate'.format(perc)
    title('\\textrm{'+ti+'}')
    savefig('reconstruction.png', dpi=200)
    show()

    #plot(abs(dwt_full(x) - wA))
    #title('\\textrm{Wavelet domain error}')
    #show()

    print "l1 norm: ", sum(error)
    print "l2 norm: ", sum(error**2)

############################################################
############ BEGINNING OF 2D CASE FUNCTIONS ################
############################################################


def haarMatrix2D(x):
    """ 
        relies on x being invertible. that's not likely with the images we'll
        be dealing with.
    """
    x = asarray(x)
    w = dwt2_full(x)
    w = asmatrix(w)
    x = asmatrix(x)

    m = w * x.I
    return m

def returnIndForWaveletXY(argX, argY):
    """
        argX, argY: some arguments that are functions of where you want to
        sample the wavelet domain signal

        returns a set of coordinates that you can access with
            >>> array[x, y] = True
        That will set the portion of the array to True for sampling.
    """
    # we're going to "stack" the values
    #sig = arange(n*n, dtype=int).reshape(n,n)
    x = findIndiciesForHaar(n)
    y = findIndiciesForHaar(n).T
    x = asarray(x, dtype=int)
    y = asarray(x, dtype=int)

    xx = x[argX]
    xx = xx[xx != -1]

    yy = y[argY]
    yy = yy[yy != -1]
    return xx, yy[:, newaxis]


n = 8
sig = asarray(around(zeros((n,n))), dtype=bool)

x, y = returnIndForWaveletXY(4, 5)

sig[x,y] = True
sometimes = asarray(around(rand(sig[x,y].shape[0], sig[x,y].shape[1])), dtype=bool)
sig[x,y] = logical_and(sometimes, sig[x,y])


#def approxWavelet2D(...):
level = 2
x = arange(n*n).reshape(n,n)
c = haarMatrix(n)
r = haarMatrix(n)

r = r.T

r = asmatrix(r)
c = asmatrix(c)
x = asmatrix(x)

#c = c[0:2**level]
#r = r[:, 0:2**level]



#argwhere(array==-1)
#argwhere[-1]

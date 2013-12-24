from __future__ import division
from pylab import *
"""
COPYRIGHT BY SparKEL Lab, University of Minnesota
ADVISOR OF LAB    : Prof. Jarvis Haupt ( jdhaupt@umn.edu  )
CREATOR OF SCRIPT : Scott Sievert      ( sieve121@umn.edu )

This script does edge detection, and finds the interested parts of an image. It
looks for the edges in an image, because that's the interesting part of an
image. The other areas, the "flat" areas, can be approximated with just a
couple samples.
"""
def haarMatrix(n, level=-1):
    """ 
    assumes n is to make a haar matrix for signal of size n

    returns matrix as in 
        w = h x
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
    return h
def waveletIndexToTime(element, h=None):
    i = argwhere(h[element,:] != 0)
    i = reshape(i, -1)
    return i
def reshapeToPixels(pix):
    """ reshapes an array of pixel values to the values they take. ie, does

    requires dynamic scope for N
    
    > reshapeToPixels(waveletIndexToTime(0, h=h))
    >> array([[0, 2],
              [1, 3]])
    """
    if len(pix) == N**2: return pix.reshape(N,N).T
    else:
        a = diff(pix) - 1
        pixelsInLine = nonzero(a)[0][0] + 1
        i = arange(len(pix)/pixelsInLine, dtype=int)
        #one = pix[pixelsInLine*i]
        #two = pix[pixelsInLine*i+1]

        done = zeros(len(pix)/pixelsInLine)
        for j in arange(pixelsInLine):
            part = pix[pixelsInLine*i + j]
            done = vstack((done, part))

        done = done[1:]
        return done
def sampleInDetail(interestedIn, sampleAt, h=None):
    """ takes in interestedIn and samples at (just) enough locations for that """
    for i in interestedIn:
        time = waveletIndexToTime(i, h=h)
        time = reshapeToPixels(time)

        halfwayH = time[0,:].size/2
        halfwayV = time[:,0].size/2
        
        sampleAt = hstack((sampleAt, \
                time[0,0], time[0,halfwayH], time[halfwayV,0], time[halfwayV,halfwayH]))

    sampleAt = unique(sampleAt)
    return sampleAt

N = 2**2
h = haarMatrix(N)
h = kron(h,h)

x = ones((N,N))

sampleAt = array([])
interestedIn = array([0,1,N,N+1, 3])
# we're currently limited to below the highest order (or corners?) by
# reshapeToPixels -- a small fix I don't feel like doing now.

# scaleAndApprox
# addSubTerms





#   0 4 8 c
#   1 5 9 d 
#   2 6 a e
#   3 7 b f







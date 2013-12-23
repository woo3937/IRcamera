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




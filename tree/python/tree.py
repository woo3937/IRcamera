from __future__ import division
from pylab import *
from functions import haarMatrix

"""
COPYRIGHT BY SparKEL Lab, University of Minnesota
ADVISOR OF LAB    : Prof. Jarvis Haupt ( jdhaupt@umn.edu  )
CREATOR OF SCRIPT : Scott Sievert      ( sieve121@umn.edu )

This script does edge detection, and finds the interested parts of an image. It
looks for the edges in an image, because that's the interesting part of an
image. The other areas, the "flat" areas, can be approximated with just a
couple samples.
"""

def sampleInDetail(interestedIn, sampleAt, h=None):
    """
        gets two samples per term
        h is the haarMatrix as in w = h x
        depends on global scope for `h = haarMatrix(n)`
    """
    for i in interestedIn:
        non_zero = where(h[i,:] != 0)[0]

        # how many terms do we want to sample at?
        number_of_terms = len(non_zero)//2
        sampleHere = non_zero[::number_of_terms]
        sampleAt = hstack((sampleAt, sampleHere))

    # collect the unique terms
    sampleAt = unique(sampleAt)

    return sampleAt
def approxWavelet(x, sampleAt, interestedIn, h=None):
    """
        approximates the wavelet transform but doesn't scale the wavelet
    """
    x_hat = x[sampleAt]
    h_hat = h[: , sampleAt ]
    h_hat = h_hat[interestedIn, :]
    w_hat = h_hat.dot(x_hat)
    # now we have the proper wavwelet, but not scaled
    return w_hat
def findIndiciesThatMatter(element):
    i = argwhere(h[element,:] != 0)
    i = reshape(i, -1)
    return i
def scaleWavelet(w_hat):
    """
        n2 for n^2, the number of terms  you sample at
        m  for the number of samples in the space
    """
    for i in arange(len(w_hat)):
        n2 = findIndiciesThatMatter(i)
        m = argwhere(n2 == sampleAt[:,newaxis])
        m = len(m)
        n2 = len(n2)
        w_hat[i] = w_hat[i] * n2 / m
    return w_hat

N = 32
h = haarMatrix(N)
x = linspace(0,N-1,N)
#x = ones(N)

interestedIn = arange(8)
sampleAt = array([], dtype=int)

sampleAt = sampleInDetail(interestedIn, sampleAt, h=h)
w_hat = approxWavelet(x, sampleAt, interestedIn, h=h)
w_hat = scaleWavelet(w_hat)








w = h.dot(x)
figure()
plot(w, marker='o')
plot(w_hat, marker='o')
show()








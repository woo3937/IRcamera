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

    w_hat2 = zeros(len(x))
    w_hat2[interestedIn] = w_hat
    return w_hat2
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
        if w_hat[i] == 0: continue
        n2 = findIndiciesThatMatter(i)
        m = argwhere(n2 == sampleAt[:,newaxis])
        m = len(m)
        n2 = len(n2)
        w_hat[i] = w_hat[i] * n2 / m
    return w_hat
def addToInterestedIn(interestedIn, level):
    """ level=XXX for the base term. it's the level we're going to """
    # we have [0 1 2 3] ==> [0 1 2 3 4 5 6 7]

    # get the bottom level of terms
    bottomLevel = interestedIn[interestedIn >= 2**(level-1)]

    # add to interestedIn
    nextLevel = 2 * bottomLevel
    interestedIn = hstack((interestedIn, nextLevel, nextLevel+1))
    interestedIn = unique(interestedIn)

    return interestedIn
def scaleAndApproxWavelet(x, sampleAt, interestedIn, h=None):
    """ """
    i = arange(len(sampleAt)-1, dtype=int)
    prod = sampleAt[i+1] - sampleAt[i]
    prod = hstack((prod, N-sampleAt[-1]))
    x_scaled = x[sampleAt] * prod

    h = h[:, sampleAt]
    h = h[interestedIn, :]

    w_hat = h.dot(x_scaled)
    ret = zeros(len(x))
    ret[interestedIn] = w_hat
    return ret

N = 2048
h = haarMatrix(N)
x = linspace(-1,1,N)
a = 1/5
x = exp(-x**2 / a**2) / (a * sqrt(pi))
#x = ones(N)

interestedIn = arange(6)
sampleAt = array([], dtype=int)

sampleAt = sampleInDetail(interestedIn, sampleAt, h   = h)
w_hat = scaleAndApproxWavelet(x, sampleAt, interestedIn, h=h)

# now, we can approximate the wavelet from an arbitrary number of samples. not
# we need to choose the best places to sample at the right locations ==>
    # 1. approximate the wavelet
    # 2. see where non-zero
    # 3. add the non-zero locations to "interestedIn"

threshold = 0.5
# in that arange(1,4), 0*2 = 0 ==> steady state, no change
for iteration in arange(1,6): 
    # adding to interestedIn
    interestedIn = addToInterestedIn(interestedIn, iteration)

    # sample in detail
    sampleAt = sampleInDetail(interestedIn, sampleAt, h=h)

    # approx and scale the wavelet
    w_hat = scaleAndApproxWavelet(x, sampleAt, interestedIn, h=h)

    # where is it greater than the threshold?
    i = argwhere(abs(w_hat[:2**(iteration+1)]) >= threshold)
    interestedIn = unique(i)
    # we need to add to interestedIn. in the terms that are non-zero, we need to add
    # the sub-terms, then sample in detail, then approx the wavelet
    
    # right. I went over this before. they might be more clustered by the negative terms.


w = h.dot(x)
figure()
plot(w, marker='.', label='Exact')
plot(w_hat, marker='.', label='Approx')
legend()
show()

figure()
plot(inv(h).dot(w), marker='.')
plot(inv(h).dot(w_hat), marker='.')
show()



# 0 1 | 2 3 | 4 5 6 7 | 8 9 10 11 12 13 14 15


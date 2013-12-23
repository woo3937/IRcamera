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
def findIndiciesThatMatter(element):
    i = argwhere(h[element,:] != 0)
    i = reshape(i, -1)
    return i
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
def scaleAndApproxWavelet(x, sampleAt, interestedIn, h=None, N=None):
    """ 
        deletes the rows and columns out of `h` then multiplies each term by
        how many it terms it stands for -- how many empty spaces can be filled
        by that one term.
    """
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

def oneD():
    """
        this function approximates the wavelet transform with edge detection <more description>.

        we have to add to interestedIn (which wavelet terms we're interested in) each time;
        we have to go down those branches. 

        for approximating the wavelet transform, we "fill in" for the missing pixels, 
        kind of like a really poor inpainting job. what if for some wavelet term 
        it's more clustered? we can't do `n / m` then.
    """
    N = 2**11
    h = haarMatrix(N)
    x = linspace(-1,1,N)
    a = 1/5
    x = exp(-x**2 / a**2) / (a * sqrt(pi))
    #x = ones(N)

    interestedIn = arange(6)
    sampleAt = array([], dtype=int)

    sampleAt = sampleInDetail(interestedIn, sampleAt, h   = h)
    w_hat = scaleAndApproxWavelet(x, sampleAt, interestedIn, h=h, N=N)

    # now, we can approximate the wavelet from an arbitrary number of samples. not
    # we need to choose the best places to sample at the right locations ==>
        # 1. approximate the wavelet
        # 2. see where non-zero
        # 3. add the non-zero locations to "interestedIn"

    # what's the threshold, and how far?
    threshold = 0.5
    level = 6
    # in that arange(1,4), 0*2 = 0 ==> steady state, no change
    for iteration in arange(1,level): 
        threshold = 2**-iteration * 0.5
        print "Threshold: ", threshold

        # adding the subterms to interestedIn
        interestedIn = addToInterestedIn(interestedIn, iteration)

        # sample in detail
        sampleAt = sampleInDetail(interestedIn, sampleAt, h=h)

        # approx and scale the wavelet
        w_hat = scaleAndApproxWavelet(x, sampleAt, interestedIn, h=h, N=N)

        # where is it greater than the threshold?
        # we're seeing where in the current "level" it's greater than the threshold
        i = argwhere(abs(w_hat[:2**(iteration+1)]) >= threshold)
        interestedIn = unique(i)
        
        # right. I went over this before. they might be more clustered by the negative terms.


    w = h.dot(x)
    figure()
    plot(w[0:2**level], marker='.', label='Exact')
    plot(w_hat[0:2**level], marker='.', label='Approx')
    legend()
    show()

    figure()
    plot(sampleAt, 'o')
    show()

    exact = inv(h).dot(w)
    approx = inv(h).dot(w_hat)

    figure()
    plot(inv(h).dot(w), marker=' ', label='Exact')
    plot(inv(h).dot(w_hat), marker=' ', label='Approx')
    plot(abs(exact - approx), label='Error')
    legend()
    show()

    print "Sampling rate: ", len(sampleAt) / N


    # 0 1 | 2 3 | 4 5 6 7 | 8 9 10 11 12 13 14 15


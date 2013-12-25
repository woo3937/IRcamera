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
    """ 
        reshapes an array of pixel values to the values they take. ie, does

        requires dynamic scope for N
        
        > reshapeToPixels(waveletIndexToTime(0, h=h))
        >> array([[0, 2],
                  [1, 3]])

        we're limited to the second-lowest wavelet term here; a bug I don't
        feel like fixing
    """
    a = diff(pix)
    b = ones(len(pix)-1)
    if len(pix) == N**2: return pix.reshape(N,N).T
    elif sum(abs(a-b))==0:
        # if pix contains something in the top row...
        i = arange(len(pix)/2, dtype=int)
        one = pix[2*i]
        two = pix[2*i+1]
        done = vstack((one,two))
        return done
    else:
        a = diff(pix) - 1
        pixelsInLine = nonzero(a)[0][0] + 1
        i = arange(len(pix)/pixelsInLine, dtype=int)

        done = zeros(len(pix)/pixelsInLine)
        for j in arange(pixelsInLine):
            part = pix[pixelsInLine*i + j]
            done = vstack((done, part))

        done = done[1:]
        return done
def sampleInDetail(interestedIn, sampleAt, h=None):
    """ takes in interestedIn and samples at (just) enough locations for that """
    for i in interestedIn:
        try:
            time = waveletIndexToTime(i, h=h)
            time = reshapeToPixels(time)

            halfwayH = time[0,:].size/2
            halfwayV = time[:,0].size/2
            
            sampleAt = hstack((sampleAt, \
                    time[0,0], time[0,halfwayH], time[halfwayV,0], time[halfwayV,halfwayH]))
        except:
            print "Except!"
            continue

    sampleAt = unique(sampleAt)
    sampleAt = asarray(sampleAt, dtype=int)
    return sampleAt
def scaleAndApprox(x, sampleAt, interestedIn, h=None):
    """ 
        scales and approximates the wavelet. it takes in

        x            : the signal
        sampleAt     : where you want to sample
        interestedIn : the wavelet terms you're interested in, indexed in the kron
                        sense
        h=h          : kron(h,h), the 2D haar matrix. only required so additional computation
                         not needed.

        There could be errors in this function. It assumes that each pixel stands
        for a region of pixels in the same rectangle (a fair assumption). But it
        also assumes that this rectangle is bounded by the nearest sample locations
        *in the same column/row.* If you have samples not bounded by these rules,
        this approximation would fail. But it works since we sample at those
        locations with sampleInDetail -- the least number of terms to accurately
        approximate the wavelet.
    """
    x = x.copy()
    h = h.copy()
    # mutliply x to stand for the other components
    fill_in = zeros((N,N))
    fill_in.T.flat[sampleAt] = 1

    # we want to take the starting index and see where non-zero around it
    # so fill in the surronding rectangle -- go as far right and down as you can
    i = argwhere(fill_in == 1)
    for y2, x2 in i:
        countX = 0
        countY = 0
        for countX in arange(N):
            countX += 1
            if x2+countX >= N: break
            if fill_in[y2,x2+countX] == 1: break
        for countY in arange(N):
            countY += 1
            if y2+countY >= N: break
            if fill_in[y2+countY,x2] == 1: break
        fill_in[y2, x2] = countY * countX
    x *= fill_in

    print "interestedIn.max(): ", interestedIn.max()
    print "h.shape: ", h.shape
    h = h[:,sampleAt]
    h = h[interestedIn, :]

    w_hat = h.dot(x.T.flat[sampleAt])
    w_hat2 = zeros((N,N))
    w_hat2.T.flat[interestedIn] = w_hat
    return w_hat2
def addSubTerms(interestedIn):
    interesting = array([2*interestedIn, 2*interestedIn+1, \
                         2*interestedIn+N, 2*interestedIn+N+1 ])
    interesting = unique(interesting.flat[:])
    interestedIn = hstack((interesting, interestedIn))
    return interestedIn

def tree():
    N = 2**6
    x = ones((N,N))
    x[:N/2, :] = 0
    x = imread('tumblr128.png')
    x = mean(x, axis=2)

    N = x.shape[0]
    h = haarMatrix(N)
    h = kron(h,h)


    sampleAt = array([])
    interestedIn = array([0,1,N,N+1])
    # we're currently limited to below the highest order (or corners?) by
    # reshapeToPixels -- a small fix I don't feel like doing now.

    sampleAt = sampleInDetail(interestedIn, sampleAt, h=h)
    w_hat = scaleAndApprox(x, sampleAt, interestedIn, h=h)

    threshold = 0.0
    level = 4
    for iteration in arange(1, level):
        threshold = 2**-iteration * threshold
        print "Threshold: ", threshold

        # adding the subterms
        interestedIn = addSubTerms(interestedIn)
        sampleAt = sampleInDetail(interestedIn, sampleAt, h=h)
        w_hat = scaleAndApprox(x, sampleAt, interestedIn, h=h)
        i = argwhere(abs(w_hat.T.flat[:] >= threshold))
        interestedIn = unique(i)

    h = haarMatrix(N)
    h = kron(h,h)
    #w_hat = scaleAndApprox(x, sampleAt, interestedIn, h=h)
    w = h.dot(x.T.flat[:])
    w = w.reshape((N,N))

    x_hat = inv(h).dot(w_hat.T.flat[:])
    x_hat = x_hat.reshape(N,N)

    figure()
    imshow(w_hat, interpolation='nearest')
    title('w_hat')
    colorbar()
    show()

    figure()
    imshow(w, interpolation='nearest')
    title('w')
    colorbar()
    show()

    error = abs(w-w_hat)
    #error[2**level:, 2**level:] = 0

    figure()
    imshow(error[:2**level, :2**level], interpolation='nearest')
    colorbar()
    title('Error')
    show()

    figure()
    imshow(x_hat, interpolation='nearest')
    colorbar()
    title('Time')
    show()

#def testSampling():
N = 2**3
x = arange(N*N).reshape(N,N).T
h = haarMatrix(N)
h = kron(h,h)
interestedIn = arange(N*N)
sampleAt = array([])

for i in interestedIn:
    #try:
    time = waveletIndexToTime(i, h=h)
    time = reshapeToPixels(time)

    halfwayH = time[0,:].size/2
    halfwayV = time[:,0].size/2
    
    sampleAt = hstack((sampleAt, \
            time[0,0], time[0,halfwayH], time[halfwayV,0], time[halfwayV,halfwayH]))
    #except:
        ##print "---------------------"
        ##print i
        #i = arange(len(time)/2, dtype=int)
        #one = time[2*i]
        #two = time[2*i+1]
        #done = vstack((one,two))
        ##print time
        #continue

sampleAt = unique(sampleAt)
sampleAt = asarray(sampleAt, dtype=int)
print sampleAt

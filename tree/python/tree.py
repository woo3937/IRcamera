from __future__ import division
from pylab import *
import ipdb

#from IST import idwt2_full, dwt2_full
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
        #i = arange(len(pix)/2, dtype=int)
        #one = pix[2*i]
        #two = pix[2*i+1]
        #done = vstack((one,two))
        done = reshape(pix, (-1,N)).T
        # make the rows the proper length
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
        time = waveletIndexToTime(i, h=h)
        time = reshapeToPixels(time)

        halfwayH = time[0,:].size/2
        halfwayV = time[:,0].size/2
        
        sampleAt = hstack((sampleAt, \
                time[0,0], time[0,halfwayH], time[halfwayV,0], time[halfwayV,halfwayH]))

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

        This function *can not* assume that each wavelet term has a rectangle
        bounded by other terms in the same rows/columns. Two boxes may overlap
        in this situation:

            x   x   x

            x       x
            x       x
            x       x
            ...

        We need to have a "box array" to fix this: what pixels have we already
        used to make boxes?

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
            if fill_in[y2+countY,x2] != 0: break
        fill_in[y2, x2] = countY * countX
    x *= fill_in
    #print fill_in[fill_in != 0]

    h = h[:,sampleAt]
    h = h[interestedIn, :]

    w_hat = h.dot(x.T.flat[sampleAt])
    w_hat2 = zeros((N,N))
    w_hat2.T.flat[interestedIn] = w_hat
    return w_hat2
def addSubTerms(interestedIn, N):
    interesting = array([2*interestedIn, 2*interestedIn+1, \
                         2*interestedIn+N, 2*interestedIn+N+1 ])
    interesting = unique(interesting.flat[:])
    interestedIn = hstack((interesting, interestedIn))
    interestedIn = unique(interestedIn)
    return interestedIn

def tree():
    N = 2**4
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

        # adding the subterms
        interestedIn = addSubTerms(interestedIn, N)
        #print interestedIn

        # sample more at those locations
        sampleAt = sampleInDetail(interestedIn, sampleAt, h=h)

        # approximate the wavelet at those locations
        w_hat = scaleAndApprox(x, sampleAt, interestedIn, h=h)

        # see where >= threshold.
        # fix so it's only looking at the last level?
        i = argwhere(abs(w_hat.T.flat[:] > threshold))


        interestedIn = unique(i)

    h = haarMatrix(N)
    h = kron(h,h)

    w = h.dot(x.T.flat[:])
    w = w.reshape((N,N))

    w = np.round(w)
    w_hat = np.round(w_hat)
    w = w.T

    s = zeros((N,N))
    s.T.flat[sampleAt] = 1

    figure()
    imshow(s, interpolation='nearest')
    title('SampleAt')
    show()

    figure()
    imshow(w_hat[:2**level, :2**level], interpolation='nearest')
    title('w_hat -- approx')
    colorbar()
    show()

    figure()
    imshow(w[:2**level, :2**level], interpolation='nearest')
    title('w -- exact')
    colorbar()
    show()

    error = abs(w-w_hat)
    #error[2**level:, 2**level:] = 0

    figure()
    imshow(error[:2**level, :2**level], interpolation='nearest')
    colorbar()
    title('Error')
    show()

def testSampling():
    N = 2**3
    x = arange(N*N).reshape(N,N).T
    h = haarMatrix(N)
    h = kron(h,h)
    interestedIn = array([0,1,N,N+1,2*N,2*N+1,3*N])
    sampleAt = array([])

    sampleAt = sampleInDetail(interestedIn, sampleAt, h=h)

    w_hat = scaleAndApprox(x, sampleAt, interestedIn, h=h)

    w = h.dot(x.T.flat[:])
    w = reshape(w, (N,N)).T
    w = np.round(w)
    w_hat = np.round(w_hat)

    figure()
    imshow(w_hat, interpolation='nearest')
    colorbar()
    show()

    figure()
    imshow(w, interpolation='nearest')
    colorbar()
    show()

def testScaleAndApprox():
    N = 2**4
    x = ones((N,N))
    x[:N/2, :N/2] = 0
    h = haarMatrix(N)
    h = kron(h,h)
    sampleAt = array([])
    interestedIn = array([0,1,N,N+1, 2*N, 5*N+1, 11*N+1])
    sampleAt = sampleInDetail(interestedIn, sampleAt, h=h)

    w_hat = scaleAndApprox(x, sampleAt, interestedIn, h=h)
    w = dwt2_full(x)




    #error = abs(w - w_hat)
    #figure()
    #imshow(error, interpolation='nearest')
    #colorbar()
    #title('error')
    #show()

    interesting=zeros((N,N))
    interesting.T.flat[interestedIn] = 1
    interesting[0:9,0:9] *= 2
    interesting[0:5,0:5] *= 2
    interesting[0:2,0:2] *= 2

    figure()
    imshow(interesting, interpolation='nearest')
    colorbar()
    show()

    figure()
    imshow(w_hat, interpolation='nearest')
    colorbar()
    title('w hat -- approx')
    show()

    figure()
    imshow(w, interpolation='nearest')
    colorbar()
    title('w -- exact')
    show()


    s = zeros((N,N))
    s.T.flat[sampleAt] = 1
    figure()
    imshow(s, interpolation='nearest')
    show()


def iDontKnow():
    N = 2**4
    x = ones((N,N))
    x[:N/2, :N/2] = 0
    h = haarMatrix(N)
    h = kron(h,h)
    sampleAt = array([])
    interestedIn = array([0,1,N,N+1, 2*N, 5*N+1, 13*N+5])
    sampleAt = sampleInDetail(interestedIn, sampleAt, h=h)

    #w_hat = scaleAndApprox(x, sampleAt, interestedIn, h=h)
    boxes = zeros((N,N))
    boxes.T.flat[sampleAt] = 1

    for i in sampleAt:
        # keep expanding by going diagonally until you hit an edge?
        # go diagonally until you hit a "1" then go in the x/y direction?
        continue
        


    h = h[:,sampleAt]
    h = h[interestedIn, :]

    w_hat = h.dot(x.T.flat[sampleAt])
    w_hat2 = zeros((N,N))
    w_hat2.T.flat[interestedIn] = w_hat
    # return...
    w_hat = w_hat2.copy()

    s = zeros((N,N))
    s.T.flat[sampleAt] = 1
    figure()
    imshow(s, interpolation='nearest')
    show()

    figure()
    imshow(w_hat, interpolation='nearest')
    show()

# make a rectangle bounded by the other terms
# fill that rectangle with the sampleAt value

# can fill in rectangles as of now
#ipdb.set_trace()
def trial():
    for y2, x2 in i[:-1]:
        # we have the point
        # make a rectangle
        for rect in arange(1,N):
            # see if we've hit a sampleAt
            if x2+rect+0 > N or y2+rect+0 > N: break
            elif sum(isnan(approx[y2:y2+rect, x2:x2+rect])==False) > 1: break
        approx[y2:y2+rect-1, x2:x2+rect-1] = approx[y2, x2]
        # okay, we've hit a sampleAt. but to increase in the x/y direction?
        if   sum(isnan(approx[y2:y2+rect, x2:x2+rect+1])==False) > 1: increase = "y"
        elif sum(isnan(approx[y2:y2+rect+1, x2:x2+rect])==False) > 1: increase = "x"
        else: increase="none"

        # keep increasing until we hit a sampleAt
        inc_Y = 0; inc_X = 0;
        for inc in arange(1,N):
            if increase=="x": 
                inc_X += 1; inc_Y = 0
            elif increase=="y": 
                inc_X = 0; inc_Y += 1
            else: 
                inc_X = 0; inc_Y = 0
            if sum(isnan(approx[y2:y2+rect+inc_Y, x2:x2+rect+inc_X])==False)>=2:
                print approx[y2:y2+rect+inc_Y, x2:x2+rect+inc_X]
                break
        #approx[y2:y2+rect+inc_Y-1, x2:x2+rect+inc_X-1] = approx[y2, x2]
def recurse(A):
    if A.shape[0]>A.shape[1]:   #split longest axis first
        if not np.isnan( A[0,A.shape[1]//2]):
            return [rect for part in np.split(A, 2, axis=1) for rect in recurse(part)]
        if not np.isnan( A[A.shape[0]//2,0]):
            return [rect for part in np.split(A, 2, axis=0) for rect in recurse(part)]
    else:
        if not np.isnan( A[A.shape[0]//2,0]):
            return [rect for part in np.split(A, 2, axis=0) for rect in recurse(part)]
        if not np.isnan( A[0,A.shape[1]//2]):
            return [rect for part in np.split(A, 2, axis=1) for rect in recurse(part)]
    return [A]
#def approxImage(x, sampleAt):
N = 2**3
h = haarMatrix(N)
h = kron(h,h)
x = arange(N*N).reshape(N,N)
interestedIn = array([0,1,N,N+1, 2*N, 26, 3])
sampleAt = array([])
sampleAt = sampleInDetail(interestedIn, sampleAt, h=h)

approx = zeros((N,N))+nan

# for term in sampleAt
approx.T.flat[sampleAt] = x.T.flat[sampleAt]

i = recurse(approx)

for index in arange(len(i)):
    i[index] = x.flat[sampleAt][index] * ones(i[index].shape)


s = zeros((N,N))
s.T.flat[sampleAt] = 1
figure()
imshow(s, interpolation='nearest')
show()

figure()
imshow(approx, interpolation='nearest')
show()




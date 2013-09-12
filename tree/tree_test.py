
"""
COPYRIGHT BY SparKEL Lab, University of Minnesota
ADVISOR OF LAB: Prof. Jarvis Haupt (jdhaupt@umn.edu)
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
import pdb

# a c-style '#define'
PRINT = False

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
    levelA = 7

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
        print abs(w).max()

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

def waveletIndToTimeInd(argX, argY, n):
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


def makePwr(pwr):
    y = 0
    n = pwr.shape[0]
    for x in arange(n):
        pwr[y, x] = floor(log2(x))
        if pwr[y, x] == -inf: pwr[y,x] = 0
        y += 1

    x = 0
    for y in arange(n):
        pwr[y, x] = floor(log2(x))
        if pwr[y, x] == -inf: pwr[y,x] = 0
        x += 1

    # it's now diagonal -- fill in the diagonals
    for i in arange(n):
        #print pwr[i,i]
        pwr[0:i, i] = pwr[i,i]
        pwr[i, 0:i] = pwr[i,i]
    pwr = pwr - log2(n)
    return pwr

def S2imshow(im, top):
    imshow(im, interpolation='nearest')
    title('\\textrm{'+top+'}')
    colorbar()
    show()

def old2D():
    nPower = 3
    n = 2**nPower
    sampleLevel = 2

    x = imread('./lenna.png').mean(axis=2) * 100
    #n = x.shape[0]
    x = arange(n*n).reshape(n,n) * 100 / (n*n)

    h = haarMatrix(n)

    # deleting where we don't sample at
    sampleAt = zeros((n,n))
    sampleAt[::n/(2**sampleLevel), ::n/(2**sampleLevel)] = 1
    sampleAt = asarray(sampleAt, dtype=bool)

    approxLevel = 2

    #waveletCoeffs = hstack((waveletCoeffs, n*n-1))
    #sampleAt[-2:, -2:] = True

    #def approxWavelet2D(x, sampleAt, approxLevel):
    """
        x: the original signal
        sampleAt: where to sample that signal -- an array of bool's
        waveletCoeffs: 
            what wavelet coeffs are you interested in? Note that you
            *must* sample in appropiate locations to guarantee a correct result.
            This is ordered as flat, column wise. If you were interested in
            every location, you would pass an array like so in: 

            >>> arange(n*n).reshape(n,n).T.flat[:]
    """
    # w = h x (for 1D)
    n = x.shape[0]
    h = haarMatrix(n)

    # making our array of which index
    ii = arange(n*n).reshape(n,n).T
    ii = ii[:2**approxLevel, :2**approxLevel]
    waveletCoeffs = ii.flat[:]

    # vec(w) = m vec(x) = vec(c x r)
    m = kron(h,h)
    k = m.copy()


    # making it flat
    s = sampleAt.T.flat[:]

    # our samples
    y = x.T.flat[:][s]


    # what terms are we interested in?
    i = arange(n*n)
    i = delete(i, waveletCoeffs)
    m = delete(m, i, axis=0)

    # deleting the corresponding columns of m
    m = delete(m, argwhere(s==False), axis=1)

    # our actual approx, in flat form
    terms = m.dot(y)

    # now, put the flat back into a square and zeros otherwise
    approx = zeros((n,n))

    for j in arange(len(waveletCoeffs)):
        approx.flat[waveletCoeffs[j]] = terms[j]
        #return approx

    # len((s == False) & (m[i] != 0))
    #approx = approxWavelet2D(x, sampleAt, waveletCoeffs)




    exact = h.dot(x).dot(h.T)
    time = h.T.dot(approx).dot(h)
    exactT = x

    rate = len(sampleAt[sampleAt == True]) / (n*n)
    S2imshow(exact[:2**approxLevel, :2**approxLevel], 'exact')
    S2imshow(approx[:2**approxLevel, :2**approxLevel], 'approx')
    S2imshow(time, 'approx time, %.0f'%(100*rate)+'\% rate')
    S2imshow(x, 'exact time')

def old2Dv2():
    nPower = 5
    n = 2**nPower
    sampleLevel = 1
    approxLevel = 3

    x = arange(n*n).reshape(n,n) * 100 / (n*n)
    x = zeros((n,n))
    x[0*n/2:1*n/2, 0*n/2:1*n/2] = 3
    x[1*n/2:2*n/2, 0*n/2:1*n/2] = 3
    x[0*n/2:1*n/2, 1*n/2:2*n/2] = 3
    x[1*n/2:2*n/2, 1*n/2:2*n/2] = 3

    sampleAt = zeros((n,n))
    sample = n/(2**(sampleLevel-0))
    sampleAt[::sample, ::sample] = 1
    sampleAt = asarray(sampleAt, dtype=bool)
    sampleAt[n/2-1:n/2+1, n/2-1:n/2+1] = True
    s = sampleAt.T.flat[:]

    i = arange(n)
    h = haarMatrix(n)
    m = kron(h,h)


    # the level
    m = delete(m, argwhere(i >= 2**approxLevel), axis=0)

    # the samples
    m = delete(m, argwhere(s == False), axis=1)

    # the samples
    y = x.T.flat[s]

    # the coeffs
    c = m.dot(y)

    # actually making the approx
    z = zeros((n,n))
    z[0:2**approxLevel, 0:2**approxLevel].flat[:] = c

    exact = x
    exactW = h.dot(x).dot(h.T)
    approx = h.T.dot(z.T).dot(h)



    rate = 100 * len(y) / len(x.flat[:]) 
    st = 2**approxLevel
    S2imshow(exact, 'exact')
    S2imshow(approx, 'approx: %.0f'%rate + '\% rate')
    S2imshow(z.T[:st, :st], 'wavelet approx')
    S2imshow(exactW[:st, :st], 'wavelet exact')

def approxWavelet2D(x, interestedIn, sampleAt):
    """
        x: a full 2D signal. it is complete and not already sampled.
        sampleAt: where you want to sample this signal. 2D again.
        interestedIn: 
            what wavelet terms you're interested in. Note that this
            is column wise flat. The terms go as below:

            >>> waveletInd = arange(n*n).reshape(n,n).T
    """
    s = sampleAt.T.flat[:]

    n = x.shape[0]
    h = haarMatrix(n)
    m = kron(h,h)

    # our measurements
    y = x.T.flat[s]

    # deleting the rows where we don't sample
    i = arange(n*n)
    m = delete(m, delete(i, interestedIn), axis=0)

    # deleting the columns we don't sample at
    m = delete(m, i[logical_not(s)], axis=1)
    print "m.shape: ", m.shape

    # getting the wavelet coeffs.
    c = m.dot(y)

    # putting the 1D back into the 2D
    z = zeros((n,n))
    z.flat[interestedIn] = c

    # some proper scaling?
    #z = z * n * n / len(argwhere(s==True))
    return z

# basics
def tree():
    seed(31)
    nPower = 5
    n = 2**nPower
    approxLevel = 2
    MAX_TERMS = 2

    threshold = -1e-3#1e-523
    ar = arange(n, dtype=int)

    # the signal
    shift = asarray((ar[::-1] - n/2.3) % n, dtype=int)
    x = zeros((n,n)) 
    x[ar, ar] = sin(2.673*pi*ar/n)+4
    x[shift, ar] = cos(ar)+400
    #x[1*n/4:3*n/4, 1*n/4:3*n/4] = 5

    #x = imread('tumblr.gif').mean(axis=2)

    n = x.shape[0]
    h = haarMatrix(n)

    # sampling at the minimum required
    sampleAt = zeros((n,n))
    sampleAt[::n/4, ::n/4] = 1
    sampleAt = asarray(sampleAt, dtype=bool)

    # where are the wavelet terms?
    waveletTerms = arange(n*n).reshape(n,n).T
    interestedIn = waveletTerms[:2**approxLevel, :2**approxLevel].flat[:]
    interestedIn = hstack((interestedIn))

    # initial approx
    z = approxWavelet2D(x, interestedIn, sampleAt)
    pwr = makePwr(zeros((n,n))) + nPower


    # wait. do we have to sample evenly?
    level = 0
    EVERY_OTHER = 3
    MAX_LEVEL = 3
    for level in arange(MAX_LEVEL):
        print "LEVEL: ", level
        i = argwhere(abs(z) >= threshold)

        # only look at the values of the appropiate level
        yI = i[:,0]
        xI = i[:,1]
        trim = pwr[yI, xI] == level
        if len(i) > 0: i = i[trim]
        elif len(i)==0: i= array([])

        # for each element, find the corresponding wavelet indicies that matter and
        # set those to True
        for element in i:
            ## try reversing [1] and [0]?
            x1, y1 = waveletIndToTimeInd(element[1], element[0], n)
            #y1 = y1.reshape(-1,)

            EVERYX = int(len(x1)/4)
            EVERYY = int(len(y1)/4)
            x2 = x1[::EVERYX] if EVERYX != 0 else x1[:]
            y2 = y1[::EVERYY] if EVERYY != 0 else y1[:]

            ## finally. sampling at MAX_TERM locations
            sampleAt[y2, x2] = True

            ## now where're interested in those locations.
            term = element[1]*n + element[0]
            interesting = array([2*term, 2*term+1, 2*term+n, 2*term+n+1])
            interestedIn = unique(hstack((interestedIn, interesting)))


        # finally, approximate the wavelet with those terms again
        z = approxWavelet2D(x.T, interestedIn, sampleAt)



    sampleAt[-1, -1] = False








    time = h.T.dot(z).dot(h)
    exact = h.dot(x).dot(h.T)
    rate = 100 * len(argwhere(sampleAt == True)) / (n*n)

    print "\n\n---------v exact v----------"
    S2imshow(x, 'exact')
    S2imshow(exact, 'wavelet exact')

    print "\n\n-----------v reconstructed v----------"
    S2imshow(z, 'wavelet reconstruction')
    S2imshow(time, 'time reconstructed, %.2f'%rate+'\% rate')
    S2imshow(sampleAt, 'where sampled')






    """
                                                             
       find level = 2 and 2 only                                                      
       n = 8
                                           
         0    1   2  3  4   5  6   7       
       .----|---|--|--|---|---|--|---.                       
       | 0  | 0 | 1 1 |  2       2   |                       
       |--------|     |              |                       
       |    |   |     |              |                       
       -----|---|------              |                       
       |        |     |              |                       
       |        |     |              |                       
       |        |     |              |                       
       |        |     |              |                       
       ---------|---------------------                       
       |              |              |                       
       |              |              |                       
       |              |              |                       
       |              |              |                       
       |              |              |                       
       |              |              |                       
       .--------------|--------------.                       



    """



def seeWhereNonZero(w, threshold, pwr, level):
    """
        sees where abs(w) >= threshold. returns 
            [ y x ]
            [ y x ]
            [ y x ]
    """
    i = argwhere(abs(w) >= threshold)
    x = i[:,1]
    y = i[:,0]
    trim = pwr[y, x] == level
    try: 
        i = i[trim]
    except: i = i
    return i

def putInterestedInIn(w, threshold, pwr, interestedIn, level):
    """
        takes in seeWhereNonZero, currentInterestedIn

        it needs to put the non-zero terms in if the parents are inteteresting.
    """
    parents = interestedIn
    parents = hstack((interestedIn, parents*2, parents*2+1, parents*2+n, parents*2+1+n))

    i = seeWhereNonZero(w, threshold, pwr, level)
    terms = i[:,1]*n + i[:,0]

    interesting = array([2*terms, 2*terms+1, 2*terms+n, 2*terms+n+1])
    interesting = interesting.flat[:]

    kids = []
    for child in interesting:
        if child in parents:
            kids += [child]
    kids = asarray(kids, dtype=int)

    #interestedIn = hstack((interestedIn, interesting))
    # enforcing the tree structure...
    interestedIn = hstack((interestedIn, kids))

    return interestedIn

def makeSampleAtTrue(i, sampleAt):
    # takes in i
    for element in i:
        y, x = element
        x1, y1 = waveletIndToTimeInd(x, y, n)
        
        # sample evenly
        # we'll always have at least 2 values
        DIV = 8
        EVERY_X = ceil(len(x1)/DIV)
        EVERY_Y = ceil(len(y1)/DIV)
        x2 = x1[::EVERY_X]
        y2 = y1[::EVERY_Y]

        sampleAt[y2, x2] = True
        sampleAt[x2, y2] = True

def scaleWavelet(wavelet, sampleAt):
    n = wavelet.shape[0]
    for y in arange(n):
        for x in arange(n):
            y1, x1 = waveletIndToTimeInd(y, x, n)
            # kinda like n^2 for the whole image.
            n2 = len(x1) * len(y1)
            i = argwhere(sampleAt[y1, x1] == True)
            m = len(i)
            if m != 0:
                wavelet[y, x] = wavelet[y, x] * n2 / m
    return wavelet


nPower = 3
n = 2**nPower
initialApprox = 1

x = arange(n*n).reshape(n,n)
x = imread('./tumblr.gif').mean(axis=2)
x = imread('./tumblr128.png').mean(axis=2)
n = x.shape[0]
nPower = log2(n)

sampleAt = zeros((n,n))
sampleAt = asarray(sampleAt, dtype=bool)



h = haarMatrix(n)
waveletTerms = arange(n*n).reshape(n,n).T
pwr = makePwr(zeros((n,n))) + nPower


u_0 = 2**(initialApprox+0)
u_1 = 2**(initialApprox+1)
interestedIn = waveletTerms[:u_1, :u_1].flat[:]
sampleAt[::n/u_1, ::n/u_1] = True

#pdb.set_trace()

# wait. we have to look at interestedIn. level1 not interested for some node,
# but it's children we are interested in.

w = approxWavelet2D(x, interestedIn, sampleAt)
threshold = 10e-3
MAX_LEVEL = 2
for level in arange(MAX_LEVEL):
    threshold = 4e-3 * mean(x[sampleAt]) * 2**(-level)
    threshold = 8e-3
    # {20, 100}e-3 work well here
    i = seeWhereNonZero(w, threshold, pwr, level)
    interestedIn = putInterestedInIn(w, threshold, pwr, interestedIn, level)
    interestedIn = unique(interestedIn)
    makeSampleAtTrue(i, sampleAt.T)

 

    w = approxWavelet2D(x.T, interestedIn, sampleAt)
    w = scaleWavelet(w, sampleAt)

    print "----------------"
    print "threshold: ", threshold
    print "len(argwhere(sampleAt==True))", len(argwhere(sampleAt==True))
    print "len(interestedIn)", len(interestedIn)

# only works at higher levels because we need to see what indicies correspond
# to some pixel location


inte = zeros((n,n))
inte.T.flat[interestedIn] = 1
inte = inte * (pwr + 1)
time = h.T.dot(w).dot(h)
wExact = h.dot(x).dot(h.T)

S2imshow(sampleAt, 'sampled here')
#S2imshow(abs(w), 'abs(wavelet) approx')
#S2imshow(wExact, 'wavelet exact')
S2imshow(time, 'approx time')
S2imshow(x, 'exact (ish)')
u = 2**MAX_LEVEL
S2imshow(inte[0:u, 0:u], 'wavelet terms we\'re interested in')








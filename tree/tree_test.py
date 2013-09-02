
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



#x = imread('./lenna.png')
#x = mean(x, axis=2)

# we want to approximate the top m terms, meaning we have to use
# waveletIndToTimeInd(x, y) in the top m places (read: top quadrant)

# I *need* a linear system of equations
level = 3
#def ...
# gets a linear combination 

# we're only interested in *some* coefficients.
# using the variables we have, get a system of equations for the wavelet
#     coefficients we're interested in.

# so, look to see where where \phi and \psi are +/-?

# we want a linear combination for some pixel location

# did I just have an "aha!" moment? Could we find which indices are important
# then select the appropiate column/row from c/r?

def phi(x, pwr, shift):
    factor = (2**(pwr/2.0))
    if type(x) == int or type(x)==float or type(x)==np.int64:
        if (2**pwr)*x - shift >=0 and (2**pwr)*x - shift <= 1:
            return 1 * factor
        else:
            return 0

def psi(x, pwr, shift):
    factor = (2**(pwr/2.0))
    if type(x) == int or type(x) == float or type(x)==np.int64:
        if (2**pwr)*x - shift >=0 and (2**pwr)*x - shift <0.5:
            return factor
        if (2**pwr)*x - shift >=0.5 and (2**pwr)*x - shift <1:
            return -1 * factor
        else:
            return 0

def phiphi(x, y, pwr, shiftX, shiftY):
    return phi(x, pwr, shiftX) * phi(y, pwr, shiftY)
def psiphi(x, y, pwr, shiftX, shiftY):
    return psi(x, pwr, shiftX) * phi(y, pwr, shiftY)
def phipsi(x, y, pwr, shiftX, shiftY):
    return phi(x, pwr, shiftX) * psi(y, pwr, shiftY)
def psipsi(x, y, pwr, shiftX, shiftY):
    a = psi(x, pwr, shiftX)
    b = psi(y, pwr, shiftY)
    return a * b

def proofThat2Dworks():
    n = 8
    pwr = -3; j = 0
    m = zeros((n,n))
    f = arange(n*n).reshape(n,n)
    #np.random.shuffle(f)
    #f = rand(n,n)
    xx = []
    sampleAt = zeros((n,n))

    x1, y1 = int(1*n/4), int(1*n/4)
    x2, y2 = int(1*n/4), int(3*n/4)
    x3, y3 = int(3*n/4), int(1*n/4)
    x4, y4 = int(3*n/4), int(3*n/4)

    for x,y in [(x1, y1),(x2, y2),(x3, y3),(x4, y4)]:
        sampleAt[y,x] = True
    sampleAt = asarray(sampleAt, dtype=bool)

    # get the x,y coord's of all the True's
    pos = argwhere(sampleAt == True)

    # select the phi's and psi's we want
    shiftX = 0
    shiftY = 0

    i = 0
    for p in pos:
        x, y = p
        print x, y
        m[0,i] = phiphi(x, y, pwr, 0, 0)
        m[1,i] = psiphi(x, y, pwr, 0, 0)
        m[2,i] = phipsi(x, y, pwr, 0, 0)
        m[3,i] = psipsi(x, y, pwr, 0, 0)
        xx += [f[y, x]]
        i += 1
        
    xx = asarray(xx)

    xx = xx.T
    m = m[0:4, 0:4]
    m = m * n**2/4
    approx = m.dot(xx)
    approx = reshape(approx, (2,2))
    approx = approx.T


    h = haarMatrix(n)
    exact = h.dot(f).dot(h.T)
    exact = around(exact, decimals=2)
    exact = exact[0:2, 0:2]

    approx.shape = (2,2)
    approx = approx.T

    imshow(approx, interpolation='nearest')
    colorbar()
    title('\\textrm{Approx}')
    show()

    imshow(exact, interpolation='nearest')
    colorbar()
    title('\\textrm{Exact}')
    show()

    imshow(abs(exact-approx), interpolation='nearest')
    colorbar()
    title('\\textrm{abs(exact-approx)}')
    show()

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

def oldShift():
    n = 8
    log2n = int(log2(n))
    f = arange(n*n).reshape(n,n)

    i = arange(log2n)

    pwr = zeros((n,n))
    pwr = makePwr(pwr)

    shift = zeros((n,n))

    # get possible number of shifts -- use pwr?
    shifts = 2**(-1 * pwr) / n
    shifts = 1/shifts

    # get the shift for each index
    i = arange(n)
    s = shifts[0]
    j = argwhere(s[i] == s[i-1])
    # seeing where those indices are >2**level and <2**(level+1)

n = 8
power = 2
pixelPos = 5
def newShift(pixelPos, power, n):
    """
        pixelPos: where is the pixel, either in x or y axis?
        power: what percentage of the image? 
                2^1 = 2 --> 1/2 = 0.5 = half the image. 
                2^2 = 4 --> 1/4 = 0.25 = one quarter
        n: how large is the oringal image?
    """
    parts = 2**power
    p = pixelPos
    width = n/parts

    # see which part the pixel is in
    i = arange(parts) * width

    j = argwhere((p - i < width) & (p-i>=0))
    shifts = int(j)
    return shifts

def evalFunctionAtPixel(fu, m, row, shiftX, shiftY, power, pos):
    i = 0
    for i in arange(len(pos)):
        x, y = pos[i]
        m[row, i] = fu(x, y, power, shiftX, shiftY)
        i += 1
    return m
# we can go from space indices to wavelet shifts
# we know what power we want



def putNStrDown(strings, string, n):
    for i in arange(n):
        strings += [string]
    return strings

def flattenPartialMatrix(l, mat, coeffs, n):
    ret = zeros((n,n))
    j = 0
    for element in l:
        x = arange(n)
        y = arange(n)
        # get the power square
        power = element[2]
        power = int(power)
        x = x[0:2**(power+1)]
        y = y[0:2**(power+1)]

        # get the H/V/A/D square
        half = len(x) / 2
        if element[0] == 'H': 
            x = x[half:]
            y = y[:half]
        if element[0] == 'V': 
            x = x[:half]
            y = y[half:]
        if element[0] == 'D': 
            x = x[half:]
            y = y[half:]

        # get the vshift, hshift
        vshift = element[-1]
        hshift = element[-2]
        vshift = int(vshift)
        hshift = int(hshift)
        x = x[hshift]
        y = y[vshift]
        ret[y, x] = coeffs[j]
        j += 1
    return ret

def make2DhaarMatrix(n, l):
    m = zeros((len(l), len(pos)))
    j = 0
    for element in l:
        if element[0] == 'A': fu = phiphi
        if element[0] == 'H': fu = phipsi
        if element[0] == 'V': fu = psiphi
        if element[0] == 'D': fu = psipsi

        hShift = element[-2]
        vShift = element[-1]
        power  = element[2]

        power  = int(power)
        vShift = int(vShift)
        hShift = int(hShift)

        power = power - powerN

        # we have to change power around -- a simple subtract/add
        m = evalFunctionAtPixel(fu, m, j, hShift, vShift, power, pos)
        j += 1
        if j >= m.shape[0]: break
    return m

# H_1_23 corresponds to power 1, 2 horizontal shift, 3 vertical shift

def writeHVDOfPower(listOfStrings, power):
    """
        generates a list of strings that will be used for solving the linear
        system of equation. Our image is something like...

        .--------|----------|---------------------
        |        |          |                     |
        |  A     |  H_0_00  | H_1_00     H_1_10   |
        |        |          |                     |
        |-------------------|                     |
        |        |          |                     |
        |  V_0_00|  D_0_00  | H_1_01     H_1_11   |
        |        |          |                     |
        |------------------------------------------
        |                   |                     |
        | V_1_00   V_1_10   | D_1_00     D_1_10   |
        |                   |                     |
        |                   |                     |
        |                   |                     |
        | V_1_10   V_1_11   | D_1_10     D_1_11   |
        |                   |                     |
        .-------------------|---------------------

        power: how large do you want each square to be? e.g., if power=3, each
               "square" will be 3x3
    """
    for string in ['H_', 'V_', 'D_']:
        for vshift in arange(power):
            for hshift in arange(power):
                toPrint = string + str(power-1) + '_' + str(hshift) + str(vshift)
                listOfStrings += [toPrint]
    return listOfStrings

def oldMethod():
    seed(42)
    l = ['A_0_00']
    powerN = 4
    powerToApproxTo = 3
    # len(x) = 2**powerN
    n = 2**powerN

    # TODO:
    #   1. make the approximation work fully (we're just off by constants)
    #       a. we're off by a constant
    #   2. something is wrong with my phiphi/etc functions
    #   3. make more modular. 

    for p in arange(powerToApproxTo):
        # to be changed when we actual do the approximation
        l = writeHVDOfPower(l, 2**p)


    x = arange(n*n).reshape(n,n)

    sampleAt = zeros((n,n))
    sampleAt[::n/4, ::n/4] = 1
    # sampling at every pixel
    sampleAt[:, :] = 1
    sampleAt = asarray(sampleAt, dtype=bool)
    pos = argwhere(sampleAt == True)


    m = make2DhaarMatrix(n, l)

    # we have the matrix; now the vector?
    vec = x[pos[:,0], pos[:,1]]
    vec.shape = (-1, 1)


    mat = m.copy()
    coeffs = m.dot(vec)



    approx = flattenPartialMatrix(l, mat, coeffs, n)
    #approx = approx * 4


    space = idwt2_full(approx)
    exact = dwt2_full(x)
    exactS = x.copy()


    imshow(exact, interpolation='nearest')
    colorbar()
    title('\\textrm{Exact wavelet}')
    show()

    imshow(approx, interpolation='nearest')
    colorbar()
    title('\\textrm{Approx wavelet}')
    show()



    imshow(space, interpolation='nearest')
    colorbar()
    title('\\textrm{Approx}')
    show()

    imshow(exactS, interpolation='nearest')
    colorbar()
    title('\\textrm{Exact}')
    show()

def old():
    nPower = 5
    level = 4
    n = 2**nPower
    h = haarMatrix(n)
    i = arange(n*n)

    x = arange(n*n).reshape(n,n) / (n*n)
    x = imread('./lenna.png')
    x = mean(x, axis=2)
    y = x.copy()
    n = x.shape[0]
    h = haarMatrix(n)
    sampleAt = zeros((n,n))
    sampleAt[::2, ::2] = 1
    print sampleAt
    sampleAt = asarray(sampleAt, dtype=bool)
    #sampleAt[0:4, 0:4] = True


    # we have everything. now vectorize.
    x = x.T.flat[:]
    sampleAt = sampleAt.T.flat[:]
    #x = x[sampleAt]

    m = kron(h, h)
    #m = delete(m, i[logical_not(sampleAt)], axis=1)

    # we're only interested in the first 2**n x 2**n square
    ind = zeros((n, n))
    makePwr(ind)
    ind = ind.flat[:]

    # delete the columns corresponding to those powers
    #j = delete(m, argwhere(ind >= level), axis=0)
    j = m.copy()

    approx = j.dot(x)

    exact = h.dot(y).dot(h.T)

    approx = approx.reshape(2**level, 2**level).T
    z = zeros((n,n))

    z[:2**level, :2**level] = approx

    time = h.T.dot(z).dot(h)

def incorrectLevels():
    approxLevel = 2

    # we still need to delete where we're not interested in.

    # we should do...
    #   deleting unsampled indices.
    #   deleting level to ensure enough variables

    nPower      = 3
    n = 2**nPower
    x = arange(n*n).reshape(n,n) * 100 / (n * n)
    #x = imread('./lenna.png').mean(axis=2)
    n = x.shape[0]
    nPower = log2(n)

    # making the sample matrix
    sampleAt = zeros((n,n))
    sampleAt[::4, ::4] = 1
    sampleAt[0:4, 0:4] = 1
    sampleAt = asarray(sampleAt, dtype=bool)

    h = haarMatrix(n)

    # our matrix
    m = kron(h, h)

    # vec(c) = m.dot(vec(x))

    # deleting the specific rows to get highest approx terms
    pwr = makePwr(zeros((n,n))) + nPower
    pwr = pwr.flat[:]

    # actually deleting
    m = delete(m, argwhere(pwr >= approxLevel), axis=0)

    # now, delete the places we don't sample at

    # making vec(x)
    y = x.T.flat[:]
    s = sampleAt.T.flat[:]

    # making our samples
    y = y[s]

    # deleting the columns
    m = delete(m, argwhere(s==False), axis=1)

    # deleting those columns

    # we can now get vec(c) 
    c = m.dot(y)

    # reshaping that matrix
    c = c.reshape(2**approxLevel, 2**approxLevel).T

    # making the full approximation
    z = zeros((n,n))
    z[0:2**approxLevel, 0:2**approxLevel] = c
    z = h.T.dot(z).dot(h)



    imshow(x, interpolation='nearest')
    colorbar()
    title('\\textrm{Time domain exact}')
    show()

    imshow(c, interpolation='nearest')
    colorbar()
    title('\\textrm{Wavelet approx terms}')
    show()


    imshow(z, interpolation='nearest')
    colorbar()
    title('\\textrm{Time domain approx}')
    show()

def S2imshow(im, top):
    imshow(im, interpolation='nearest')
    axis('off')
    title('\\textrm{'+top+'}')
    colorbar()

    show()

nPower = 2
n = 2**nPower

x = arange(n*n).reshape(n,n)
waveletCoeffs = array([0, 1, 2, 3, n,n+1,n+2,n+3,2*n,2*n+1,2*n+2,2*n+3,3*n+0,3*n+1,3*n+2,3*n+3])

# w = h x (1D)
h = haarMatrix(n)

# vec(w) = m vec(x) = vec(c x r)
m = kron(h,h)

# deleting where we don't sample at
sampleAt = zeros((n,n))
sampleAt[::1, ::1] = 1
sampleAt = asarray(sampleAt, dtype=bool)

s = sampleAt.T.flat[:]

# our samples
y = x.T.flat[:][s]

# deleting the corresponding columns of m
m = delete(m, argwhere(s==False), axis=1)

i = arange(n*n)
i = delete(i, waveletCoeffs)

m = delete(m, i, axis=0)

# our actual approx, in flat form
terms = m.dot(y)

# now, put the flat back into a square and zeros otherwise
approx = zeros((n,n))

for i in arange(len(waveletCoeffs)):
    print i
    approx.T.flat[waveletCoeffs[i]] = terms[i]


exact = h.dot(x).dot(h.T)
#approx = approx.T
time = h.T.dot(approx).dot(h)

S2imshow(exact, 'exact')
S2imshow(approx, 'approx')
S2imshow(time, 'time')

 



from pylab import *
from tree import *


N = 32
h = haarMatrix(N)
#x = linspace(-1,1,N)
x = ones(N)

interestedIn = arange(6)
sampleAt = array([], dtype=int)

sampleAt = sampleInDetail(interestedIn, sampleAt, h   = h)
w_hat    = approxWavelet(x, sampleAt, interestedIn, h = h)

#def scale
# multiply x via sampleAt
i = arange(len(sampleAt)-1, dtype=int)
prod = sampleAt[i+1] - sampleAt[i]
prod = hstack((prod, N-sampleAt[-1]))
x_scaled = x[sampleAt] * prod

h = h[:, sampleAt]
h = h[interestedIn, :]

w_hat = h.dot(x_scaled)
#return w_hat


# exact
h = haarMatrix(N)
w = h.dot(x)



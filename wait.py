from __future__ import division
from pylab import *


# for 0xb174, the lowest possible wait time
# the wait times
wait = array([10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 41, 44, 47])
f1i4 = array([73, 68, 61, 55, 48, 43, 36, 30, 23, 15,  7,  0,  0])
#perc = perc / 100 # the percentages
f4i4 = array([ ])

figure()
plot(wait, f1i4, marker='o', c='b', label='\\textrm{FIR=1, IIR=4}')
title('\\textrm{Percentage of repeats} ($x[n] = x[n-1]$)')
ylabel('\\textrm{Percent repeat}')
xlabel('\\textrm{Wait time (ms)}')
legend(loc=0)
savefig('wait.png', dpi=300)
show()



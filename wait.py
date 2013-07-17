from __future__ import division
from pylab import *


# for 0xb174, the lowest possible wait time
# the wait times
wait = array([10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 41, 44, 47])
f1i4 = array([73, 68, 61, 55, 48, 43, 36, 30, 23, 15,  7,  0,  0])
#perc = perc / 100 # the percentages
wf4i4 = array([10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55,
    58, 61])
f4i4 = array([ 81, 75, 71, 66, 62, 58, 50, 48, 44, 34, 30, 25, 22, 17, 18,  7,
    3, 3])
f3i4  = array([58, 40, 20,  3,  1])
wf3i4 = array([20, 30, 40, 50, 60])


f7i4  = array([61, 59, 53, 44,  39,  35,  22,  21,  12])
wf7i4 = array([60, 70, 80, 90, 100, 110, 130, 150, 200])



figure()
plot(wait, f1i4, marker='o', c='b', label='\\textrm{FIR=1, IIR=4}')
plot(wf3i4, f3i4, marker='o', label='\\textrm{FIR=3, IIR=4}')
plot(wf4i4, f4i4, marker='o', label='\\textrm{FIR=4, IIR=4}')
plot(wf7i4, f7i4, marker='o', label='\\textrm{FIR=7, IIR=4}')

xlim(5, 85)


title('\\textrm{Percentage of repeats} ($x[n] = x[n-1]$)')
ylabel('\\textrm{Percent repeat}')
xlabel('\\textrm{Wait time (ms)}')
legend(loc='lower left')
savefig('wait.png', dpi=300)
show()



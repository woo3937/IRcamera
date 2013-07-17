from __future__ import division
from pylab import *


def gr(filename, repeat=1):
    file = open(filename)
    same = []

    for line in file.readlines():
        same += repeat * [float(line)]

    same = asarray(same)
    m = mean(same)
    same = same - m
    m = mean(same)
    s = std(same)
    return m, s, same

mf1i4, sf1i4, f1i4 = gr('./temp.rpi/IRcamera/FIR1_IIR4_noise.txt')
mf3i4, sf3i4, f3i4 = gr('./temp.rpi/IRcamera/FIR3_IIR4_noise.txt')
mf4i4, sf4i4, f4i4 = gr('./temp.rpi/IRcamera/FIR4_IIR4_noise.txt')
mf7i4, sf7i4, f7i4 = gr('./temp.rpi/IRcamera/FIR7_IIR4_noise.txt', repeat=10)



figure()


subplot(111)
hist(f1i4, bins=50, label='\\textrm{FIR=1, IIR=4}', histtype='step')
hist(f3i4, bins=50, label='\\textrm{FIR=3, IIR=4}', histtype='step')
hist(f4i4, bins=25, label='\\textrm{FIR=4, IIR=4}', histtype='step')
hist(f7i4, bins=12, alpha=0.5, label='\\textrm{FIR=7, IIR=4}', histtype='step')
legend(loc='best')



xlabel('\\textrm{Temperature Noise}')
ylabel('\\textrm{Frequency}')
title('\\textrm{Temperature over %dk measurements}' % (len(f1i4)/1000))
savefig('noise.png', dpi=300)
show()

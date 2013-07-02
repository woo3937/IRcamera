from __future__ import division
from pylab import *

file = './temp.rpi/IRcamera/noise.txt'
file = open(file)

same = []
for line in file.readlines():
    same += [float(line)]

same = asarray(same)
m = mean(same)
same = same - m
m = mean(same)
s = std(same)



figure()


subplot(111)
hist(same, bins=25)

xmin, xmax = xlim()
ymin, ymax = ylim()
x1 = array([m-s, m-s])
y1 = array([0  , ymax])
x2 = array([m, m ])
y2 = array([0, ymax])
x3 = array([m+s, m+s])
y3 = array([0  , ymax])
plot(x1, y1, 'r-.')
plot(x2, y2, 'r-')
plot(x3, y3, 'r-.')
xtext = 0.82 * (xmax - xmin) + xmin
ytext = 0.1 * ymax
#text(xtext, ytext, '\\textrm{mean = %0.2f}' % m + '\n \\textrm{std = %0.2f}'% s)
#text(xtext, ytext, '\\textrm{std = %0.2f}'% s)


xlabel('\\textrm{Temperature}')
ylabel('\\textrm{Frequency}')
title('\\textrm{Temperature over %dk measurements (FIR=1, IIR=4)}' % (len(same)/1000))
savefig('noise.png', dpi=300)
show()

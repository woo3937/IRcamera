from pylab import *
from pandas import read_csv

# read the data
noise = read_csv('./temp.rpi/IRcamera/noise.csv')
noise = array(noise)

wait = read_csv('./temp.rpi/IRcamera/wait.csv')
wait = array(wait)
wait = wait[:, -1]

# sort the data
i = argsort(noise[:,2])
i = argsort(wait)
xtix = noise[i[0:len(i)/2], 1]
noise = noise[i]
wait = wait[i]
wait *= 1000
noise = noise[:, 2]






# plot
fig = figure()
ax = fig.add_subplot(111)
ax2 = twinx()

ax.plot(noise, marker='o', label='\\textrm{Noise}')
ax2.plot(wait, c='g', marker='o', label='\\textrm{Settling time (s)}')
ax.legend(loc=2)
ax2.legend(loc=1)
#ax2.set_yscale('log')
ax2.set_ylim(40, 160)
ax.set_xticklabels(xtix, fontname='cursive')

title('\\textrm{Noise and settling time}')
ax.set_xlabel('\\textrm{Device mode \\small (sorted by settling time)}')
ax.set_ylabel('\\textrm{Noise standard deviation($^{\circ}$ C)')
ax2.set_ylabel('\\textrm{Settling time (ms)}')
savefig('./noise_and_wait.png', dpi=300)
show()

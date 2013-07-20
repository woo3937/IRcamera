# this requires that all of these packages be installed.
# -- sys and numpy come with the RPi by default
# -- pandas, matplotlib: sudo apt-get python-<name>
from sys import argv
from numpy import array
from pandas import read_csv

import matplotlib as mpl
mpl.use('Cairo')
import matplotlib.pyplot as plt

filename = argv[1]
print filename
df = read_csv('image.csv')
im = array(df)

fig = plt.figure()
plt.axis('off')
plt.imshow(im, cmap='jet')
fig.savefig(filename, dpi=100, bbox_inches='tight')


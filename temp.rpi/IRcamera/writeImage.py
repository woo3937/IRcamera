# this requires that all of these packages be installed.
# -- sys and numpy come with the RPi by default
# -- pandas, matplotlib: sudo apt-get python-<name>
from sys import argv
from numpy import array, rot90
from pandas import read_csv

import matplotlib as mpl
mpl.use('Cairo')
import matplotlib.pyplot as plt

filename = argv[1]
print filename
df = read_csv('image.csv')
im = array(df)

# depends on the hardware specification!
im = rot90(im, 3)

fig = plt.figure()
plt.axis('off')
plt.imshow(im, interpolation='nearest', cmap='jet')
fig.savefig(filename, dpi=300, bbox_inches='tight')


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
df = read_csv('image.csv', header=None)
im = array(df)

# it is currently (2013-08-07):
# vertical axis --->
# horiz    low            high 
# axis     left      
#  |                
#  |       right    
#  v                

print im.shape

# depends on the hardware specification!
im = rot90(im, 1)

width = im.shape[0]

fig = plt.figure()
plt.text(width*1.00,width*1.05,str(im.shape))
plt.axis('off')
plt.imshow(im, interpolation='nearest', cmap='jet')
cbr = plt.colorbar()
cbr.set_label("degrees Celcius")

fig.savefig(filename, dpi=300, bbox_inches='tight')


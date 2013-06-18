from __future__ import division
from pylab import *
import pandas as pd

#             FIR    IIF   wait (ms)
data = array([0b100, 0b100, 60])
part = array([0b001, 0b100, 10]); data = vstack((data, part))

from __future__ import division
from pylab import *
import pandas as pd

# the FOV is roughly constant -- around 5 degrees

def readCSV(filename):
#filename = './temp.rpi/IRcamera/FOV_b174.csv'
    dataFrame = pd.read_csv(filename)
    a = array(dataFrame)
    return a[:,0], a[:,1]

b174_temp, b174_deg = readCSV('./temp.rpi/IRcamera/FOV_b174.csv')
b274_temp, b274_deg = readCSV('./temp.rpi/IRcamera/FOV_b274.csv')
b374_temp, b374_deg = readCSV('./temp.rpi/IRcamera/FOV_b374.csv')
b474_temp, b474_deg = readCSV('./temp.rpi/IRcamera/FOV_b474.csv')

# getting the FOV
div = sqrt(2)
div = 3
b174_cut = (max(b174_temp)-min(b174_temp))/div + min(b174_temp)
b274_cut = (max(b274_temp)-min(b274_temp))/div + min(b274_temp)
b374_cut = (max(b374_temp)-min(b374_temp))/div + min(b374_temp)
b474_cut = (max(b474_temp)-min(b474_temp))/div + min(b474_temp)

b174_i = b174_temp > b174_cut
b174_FOV = max(b174_deg[b174_i]) - min(b174_deg[b174_i]) 

b274_i = b274_temp > b274_cut
b274_FOV = max(b274_deg[b274_i]) - min(b274_deg[b274_i]) 

b374_i = b374_temp > b374_cut
b374_FOV = max(b374_deg[b374_i]) - min(b374_deg[b374_i]) 

b474_i = b474_temp > b474_cut
b474_FOV = max(b474_deg[b474_i]) - min(b474_deg[b474_i]) 


plot(b174_deg, b174_temp, label='\\textrm{b174 (FOV = %.2f$^\circ$)}'%b174_FOV)
plot(b274_deg, b274_temp, label='\\textrm{b274 (FOV = %.2f$^\circ$)}'%b274_FOV)
plot(b374_deg, b374_temp, label='\\textrm{b374 (FOV = %.2f$^\circ$)}'%b374_FOV)
plot(b474_deg, b474_temp, label='\\textrm{b474 (FOV = %.2f$^\circ$)}'%b474_FOV)
plot([b174_deg[b174_i][0], b174_deg[b174_i][0]], [20, 100],   c='black')
plot([b174_deg[b174_i][-1], b174_deg[b174_i][-1]], [20, 100], c='black')
legend()
xlabel('\\textrm{Angle (degrees)}')
ylabel('\\textrm{Temperature (degrees celcius)}')
savefig('FOV.png', dpi=300)
show()


from __future__ import division
from pylab import *
import pandas as pd

def FOV():
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


    subplot(311)
    title('\\textrm{Field of View}')
    plot(b174_deg, b174_temp, label='\\textrm{FIR=1 (FOV = %.2f$^\circ$)}'%b174_FOV)
    plot(b274_deg, b274_temp, label='\\textrm{FIR=2 (FOV = %.2f$^\circ$)}'%b274_FOV)
    plot(b374_deg, b374_temp, label='\\textrm{FIR=3 (FOV = %.2f$^\circ$)}'%b374_FOV)
    plot(b474_deg, b474_temp, label='\\textrm{FIR=4 (FOV = %.2f$^\circ$)}'%b474_FOV)
    plot([b174_deg[b174_i][0], b174_deg[b174_i][0]], [20, 100],   c='black')
    plot([b174_deg[b174_i][-1], b174_deg[b174_i][-1]], [20, 100], c='black')
    plot([5.4, 10.54], [b174_cut, b174_cut])
    legend()
    xlabel('\\textrm{Angle (degrees)}')
    ylabel('\\textrm{Temperature (degrees celcius)}')
def noise():
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



    #figure()


    subplot(312)
    hist(f1i4, bins=50, label='\\textrm{FIR=1, IIR=4}', histtype='step')
    hist(f3i4, bins=50, label='\\textrm{FIR=3, IIR=4}', histtype='step')
    hist(f4i4, bins=25, label='\\textrm{FIR=4, IIR=4}', histtype='step')
    hist(f7i4, bins=12, alpha=0.5, label='\\textrm{FIR=7, IIR=4}', histtype='step')
    legend(loc='best')



    xlabel('\\textrm{Temperature Noise}')
    ylabel('\\textrm{Frequency}')
    title('\\textrm{Temperature over %dk measurements}' % (len(f1i4)/1000))
def wait():

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



    subplot(313)
    plot(wait, f1i4, marker='o', c='b', label='\\textrm{FIR=1, IIR=4}')
    plot(wf3i4, f3i4, marker='o', label='\\textrm{FIR=3, IIR=4}')
    plot(wf4i4, f4i4, marker='o', label='\\textrm{FIR=4, IIR=4}')
    plot(wf7i4, f7i4, marker='o', label='\\textrm{FIR=7, IIR=4}')

    xlim(5, 85)


    title('\\textrm{Percentage of repeats} ($x[n] = x[n-1]$)')
    ylabel('\\textrm{Percent repeat}')
    xlabel('\\textrm{Wait time (ms)}')
    legend(loc='lower left')

figure(figsize=(14,14))
FOV()
noise()
wait()
savefig('combined.png', dpi=300)
show()

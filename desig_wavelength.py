import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def one_phase_fit(cal_time, cal_abs):
    
    # Extract 3 points from the data and calculate p0
    x1, y1 = cal_time[5], cal_abs[5]
    x2, y2 = cal_time[10], cal_abs[10]
    x3, y3 = cal_time[60], cal_abs[60]
    tau0 = (x2-x1)/np.log((y3-y2)/(y3-y1))
    a0 = -((y3-y1)**(x2/(x2-x1)) / (y3-y2)**(x1/(x2-x1)))
    
    # a = Y0, tau = time constant, p = plateau
    def exp_func(x, a, tau, p):
        return (a-p)*np.exp(-(x/tau))+p
    
    # Curve fitting
    popt, pcov = curve_fit(exp_func, cal_time, cal_abs, p0=(a0, tau0, 0))
    print(popt)
    """
    Recommended p0:
    >10000 μs: (-0.1, 20000, -0.1)
    <10000 μs: (-0.1, 10, 0)
    """ 

    # Outputs
    fit_abs = [exp_func(i, *popt) for i in cal_time]
    fit_abs = [i*1000 for i in fit_abs]
    hftime = np.log(2) * popt[1]
    sigma = np.sqrt(np.diag(pcov))
    print("tau: {} μs".format(round(popt[1], 3)))
    print("hftime: {} μs".format(round(hftime, 3)))
    print(sigma)
    return fit_abs


def extract2D(df, option):

    # Scattered points of wavelengths >400 nm
    zdata = df[36:, 1:]
    
    # Find global extremum
    if option == 'min':
        waveindex, timeindex = np.unravel_index(np.argmin(zdata, axis=None), zdata.shape)
    elif option == 'max':
        waveindex, timeindex = np.unravel_index(np.argmax(zdata, axis=None), zdata.shape)
    
    zdata = zdata[waveindex, 0:]
    zdata = zdata*1000
    xdata = df[0, 1:]
    cri_wave = df[waveindex+36, 0]
    cri_time = df[0, timeindex+1]
    cri_abs = df[waveindex+36, timeindex+1]

    # One phase fitting
    cal_abs, cal_time = [], []
    for i in range(len(df[0, 0:])):
        if (df[0, i] >= cri_time):
            cal_time.append(df[0, i])
            cal_abs.append(df[waveindex+36, i])
    fit_abs = one_phase_fit(cal_time, cal_abs)
    print("critical value: {} at {} nm, {} μs".format(round(cri_abs, 3), cri_wave, cri_time))

    return xdata, zdata, cal_time, fit_abs, cri_wave


def designate_wave(df, desigwave):
    desigwave = int(desigwave)
    newdf = pd.DataFrame(columns=['Time', 'Abs'])
    newdf['Time'] = df[0, 1:]

    # Find actual wavelength
    for i in range(1, len(df)):
        if (desigwave < df[i,0]):
            newdf['Abs'] = (df[i, 1:])
            wave_real = df[i, 0]
            break
    
    newdf['Abs'] = [i*1000 for i in newdf['Abs']]
    return newdf['Time'], newdf['Abs'], wave_real


def plotting(x, z, fit_x, fit_z, wave):
    fig, ax = plt.subplots(figsize=(12.8, 9.6))
    ax.set_xlabel('Delay Time (μs)', fontsize=18, labelpad=12)
    ax.set_ylabel('ΔAbs. (mOD)', fontsize=18, labelpad=12)
    plt.plot(x, z, 'k')
    plt.plot(fit_x, fit_z, 'r')
    title = input_path[0:4]+'  '+str(wave)+' nm'
    plt.suptitle(title, y=0.93, fontsize=20)
    plt.show()
    return fig


if __name__ == '__main__':
    import sys
    import os
    input_path = sys.argv[1]
    df = pd.read_csv(input_path, skiprows=5, header=None, index_col=None)
    df = np.array(df)
    input_path = os.path.splitext(input_path)[0]

    # Switch between designate_wave or finding global extremum
    if sys.argv[2].isdigit() == True:
        desigwave = sys.argv[2]
        x, z, wave = designate_wave(df, desigwave)
        fit_x, fit_z = 0, 0
    elif sys.argv[2] == 'min' or sys.argv[2] == 'max':
        option = sys.argv[2]
        x, z, fit_x, fit_z, wave = extract2D(df, option)
    
    plot = plotting(x, z, fit_x, fit_z, wave)
    #plot.savefig(input_path+str(sys.argv[2])+".png", bbox_inches='tight')
    
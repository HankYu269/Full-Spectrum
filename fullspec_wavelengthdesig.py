import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit


def extract2D(df, option):

    plt.figure(figsize=(50, 100))
    df = np.array(df)

    # Scattered points of wavelengths >370 nm
    zdata = df[36:, 1:]
    
    # Find local minimum or maximum
    if option == 'min':
        wave = np.unravel_index(np.argmin(zdata, axis=None), zdata.shape)[0]
    elif option == 'max':
        wave = np.unravel_index(np.argmax(zdata, axis=None), zdata.shape)[0]
    
    zdata = zdata[wave, 0:]
    zdata = savgol_filter(zdata*1000, 9, 2)
    xdata = df[0, 1:]

    # Plotting
    ax = plt.axes()
    ax.set_xlabel('Time (μs)', fontsize=18, labelpad=12)
    ax.set_ylabel('ΔAbsorbance (mOD)', fontsize=18, labelpad=12)
    
    ax.plot(xdata, zdata)
    wave_df = df[wave+36, 0]
    title = input_path[0:4]+'  '+str(wave_df)+' nm'
    plt.suptitle(title, y=0.93, fontsize=20)
    plt.show()
    return xdata, zdata


def designate_wave(df, desigwave):
    
    plt.figure(figsize=(50, 100))
    df = np.array(df)
    desigwave = int(desigwave)

    newdf = pd.DataFrame(columns=['Time', 'Abs'])
    newdf['Time'] = df[0, 1:]
    for i in range(1, len(df)):
        if (desigwave < df[i,0]):
            newdf['Abs'] = (df[i, 1:])
            wave = df[i, 0]
            break
    newdf['Abs'] = savgol_filter(newdf['Abs'], 9, 2)

    # Plotting
    ax = plt.axes()
    ax.set_xlabel('Time (μs)', fontsize=18, labelpad=12)
    ax.set_ylabel('ΔAbsorbance (mOD)', fontsize=18, labelpad=12)
    
    ax.plot(newdf['Time'], newdf['Abs'])
    title = input_path[0:4]+'  '+str(wave)+' nm'
    plt.suptitle(title, y=0.93, fontsize=20)
    plt.show()

def one_phase_decay(df, option):
    df = np.array(df)

    # Scattered points of wavelengths >370 nm
    zdata = df[36:, 1:]

    # Find local minimum or maximum
    if option == 'min':
        cri_abs = np.min(zdata, axis=None)
        cri_waveindex, cri_timeindex = np.unravel_index(np.argmin(zdata, axis=None), zdata.shape)
        cri_wave = df[cri_waveindex+36, 0]
        cri_time = df[0, cri_timeindex+1]

    elif option == 'max':
        cri_abs = np.max(zdata, axis=None)
        cri_waveindex, cri_timeindex = np.unravel_index(np.argmax(zdata, axis=None), zdata.shape)
        cri_wave = df[cri_waveindex+36, 0]
        cri_time = df[0, cri_timeindex+1]

    # Set analysis interval
    cal_abs, cal_time = [], []
    for i in range(len(df[0, 0:])):
        if (df[0, i] >= cri_time):
            cal_time.append(df[0, i])
            cal_abs.append(df[cri_waveindex+36, i])
    
    # Curve Fitting
    # a = Y0, p = plateau
    def exp_func(x, a, k, p):
        return (a-p)*np.exp(-k*x)+p
    
    popt, pcov = curve_fit(exp_func, cal_time, cal_abs)
    print(popt)

    # Outputs
    fit_abs = [exp_func(i, *popt) for i in cal_time]
    hftime = np.log(2) * popt[1]
    #sigma = np.sqrt(np.diag(pcov))
    print("critical_value: {} at {} nm, {} μs".format(round(cri_abs, 3), cri_wave, cri_time))
    print("tau: {} μs".format(round(popt[2], 3)))
    print("hftime: {} μs".format(round(hftime, 3)))
    #print("sigma: {}".format(round(sigma, 3)))

    # Plotting
    plt.plot(cal_time, cal_abs)
    plt.show()
    return cal_time, fit_abs

# General plotting function still working on
def plotting(x, z, fit_x, fit_z):
    
    ax = plt.axes()
    ax.set_xlabel('Time (μs)', fontsize=18, labelpad=12)
    ax.set_ylabel('ΔAbsorbance (mOD)', fontsize=18, labelpad=12)
    
    ax.plot(x, z, 'k')
    ax.plot(fit_x, fit_z, 'r')
    waveaxis = df[36:, 0]
    title = input_path[0:4]+'  '+str(waveaxis[desigwave])+' nm'
    plt.suptitle(title, y=0.93, fontsize=20)
    plt.show()
    pass


if __name__ == '__main__':
    import sys
    import os
    input_path = sys.argv[1]
    df = pd.read_csv(input_path, skiprows=5, header=None, index_col=None)
    input_path = os.path.splitext(input_path)[0]

    # Switch between designate_wave or finding global extremum
    if len(sys.argv) == 2:
        print("Lack of designated wavelength or option")
    elif sys.argv[2].isdigit() == True:
        desigwave = sys.argv[2]
        designate_wave(df, desigwave)
    elif sys.argv[2] == 'min' or sys.argv[2] == 'max':
        option = sys.argv[2]
        #one_phase_decay(df, option)
        extract2D(df, option)
        #plotting(x, z, fit_x, fit_z)
    else:
        print("Value Error: option should be min or max")
        
    #plt.savefig(input_path+".png")
    

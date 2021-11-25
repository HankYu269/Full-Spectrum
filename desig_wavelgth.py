import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.optimize import OptimizeWarning


def one_phase_fit(cal_time, cal_abs):
    
    # Extract 3 points from the data and calculate p0
    x1, y1 = cal_time[5], cal_abs[5]
    x2, y2 = cal_time[10], cal_abs[10]
    x3, y3 = cal_time[-1], cal_abs[-1]
    tau0 = (x2-x1)/np.log((y3-y2)/(y3-y1))
    a0 = -((y3-y1)**(x2/(x2-x1)) / (y3-y2)**(x1/(x2-x1)))
    
    # a = Y0, tau = time constant, p = plateau
    def exp_func(x, a, tau, p):
        return (a-p)*np.exp(-(x/tau))+p
    
    # Curve fitting
    popt = curve_fit(exp_func, cal_time, cal_abs, p0=(a0, tau0, 0))[0]
    print(popt)

    # Outputs
    fit_abs = [exp_func(i, *popt) for i in cal_time]
    fit_abs = [i*1000 for i in fit_abs]
    tau = popt[1]/1000
    hftime = (np.log(2) * tau)
    print("tau: {} ms".format(round(tau, 3)))
    print("hftime: {} ms".format(round(hftime, 3)))
    text = "τ: {} ms".format(round(tau, 3))
    return fit_abs, text

def extract2D(df, option):

    # Points in wavelengths of 400~700 nm; find local extrema
    if option == 'g':
        for i in range(1, len(df)):
            if (df[i, 0] > 500):
                wavestart = i
                break
        zdata = df[wavestart:, 1:]
        waveidx, timeidx = np.unravel_index(np.argmin(zdata, axis=None), zdata.shape)
        zlist = zdata[waveidx, :]
        cri_wave = df[waveidx+wavestart, 0]
    elif option == 'm':
        for i in range(1, len(df)):
            if (df[i, 0] > 400):
                wavestart = i
                break
        for j in range(1, len(df)):
            if (df[j, 0] > 500):
                waveend = j
                break
        zdata = df[wavestart:waveend, 1:]
        waveidx, timeidx = np.unravel_index(np.argmax(zdata, axis=None), zdata.shape)
        zlist = zdata[waveidx, :]
        cri_wave = df[wavestart+waveidx, 0]
    elif option == 'o':
        for k in range(1, len(df)):
            if (df[k, 0] > 600):
                wavestart = k
                break
        zdata = df[wavestart:, 1:]
        waveidx, timeidx = np.unravel_index(np.argmax(zdata, axis=None), zdata.shape)
        zlist = zdata[waveidx, :]
        cri_wave = df[waveidx+wavestart, 0]
    
    zlist = zlist*1000
    xdata = df[0, 1:]
    cri_time = df[0, timeidx+1]
    cri_abs = df[waveidx+wavestart, timeidx+1]
    print("critical value: {} at {} nm, {} μs".format(cri_abs, cri_wave, cri_time))

    # One-phase fitting
    cal_abs, cal_time = [], []
    for i in range(len(df[0, 0:])):
        if (df[0, i] >= cri_time):
            cal_time.append(df[0, i])
            cal_abs.append(df[waveidx+wavestart, i])
    
    import warnings
    warnings.simplefilter("error", OptimizeWarning)
    try:
        fit_abs, text = one_phase_fit(cal_time, cal_abs)
    except OptimizeWarning:
        cal_time, fit_abs, text = 0, 0, ""
        print("OptimizeWarning: Covariance of the parameters could not be estimated")
    except:
        cal_time, fit_abs, text = 0, 0, ""
        print("Fitting failed ~ orz")
    finally:
        pass

    return xdata, zlist, cal_time, fit_abs, cri_wave, text

def designate_wave(df, desigwave):
    desigwave = int(desigwave)
    newdf = pd.DataFrame(columns=['Time', 'Abs'])
    newdf['Time'] = df[0, 1:]

    # Find the actual wavelength
    for i in range(1, len(df)):
        if (desigwave < df[i,0]):
            newdf['Abs'] = (df[i, 1:])
            wave_real = df[i, 0]
            break
    
    newdf['Abs'] = [i*1000 for i in newdf['Abs']]
    return newdf['Time'], newdf['Abs'], wave_real

def plotting(x, z, fit_x, fit_z, wave, text):
    fig, ax = plt.subplots(figsize=(12, 8))
    font = {'family': 'arial', 'size': 19}
    plt.plot(x, z, 'k')
    plt.plot(fit_x, fit_z, 'r')
    plt.xlabel('Delay Time (μs)', fontdict=font, labelpad=13)
    plt.ylabel('Δ Abs. (mAU)', fontdict=font, labelpad=20)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    title = input_path[0:4]+'  '+str(wave)+' nm'
    plt.title(title, y=1.03, fontfamily='arial', fontsize=24, fontweight='semibold')
    ax.set_aspect(0.6/ax.get_data_ratio(), adjustable='box')
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.75)
    props = dict(alpha=0.5, boxstyle='round', facecolor='white')
    ax.text(0.72, 0.15, text, bbox=props, fontsize=20, transform=ax.transAxes)
    ax.tick_params(width=1.75)
    plt.show()
    return fig


if __name__ == '__main__':
    import sys
    import os
    input_path = sys.argv[1]
    df = pd.read_csv(input_path, skiprows=5, header=None, index_col=None)
    df = np.array(df)
    input_path = os.path.splitext(input_path)[0]

    # Switch between wavelength designation or global extremum finding
    if sys.argv[2].isdigit() == True:
        desigwave = sys.argv[2]
        x, z, wave = designate_wave(df, desigwave)
        fit_x, fit_z, text = 0, 0, ""
    elif sys.argv[2] == 'g' or sys.argv[2] == 'm' or sys.argv[2] == 'o':
        option = sys.argv[2]
        x, z, fit_x, fit_z, wave, text = extract2D(df, option)
    
    plot = plotting(x, z, fit_x, fit_z, wave, text)
    plot.savefig(input_path+str(sys.argv[2])+".png", bbox_inches='tight')
    
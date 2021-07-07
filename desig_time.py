import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


def extract2D(df, option):

    # Scattered points of wavelengths >400 nm
    zdata = df[36:, 1:]
    
    # Find local minimum or maximum
    if option == 'min':
        timeindex = np.unravel_index(np.argmin(zdata, axis=None), zdata.shape)[1]
    elif option == 'max':
        timeindex = np.unravel_index(np.argmax(zdata, axis=None), zdata.shape)[1]
    
    zdata = zdata[0:, timeindex]
    zdata = savgol_filter(zdata*1000, 9, 2)
    ydata = df[36:, 0]
    time_real = df[0, timeindex+1]
    return ydata, zdata, time_real

def designate_time(df, desigtime):
    desigtime = int(desigtime)
    newdf = pd.DataFrame(columns=['Wavelength', 'Abs'])
    newdf['Wavelength'] = df[36:, 0]

    # Find actual wavelength
    for i in range(1, len(df)):
        if (desigtime < df[0, i]):
            newdf['Abs'] = (df[36:, i])
            time_real = df[0, i]
            break
    
    newdf['Abs'] = savgol_filter(newdf['Abs'], 9, 2)
    return newdf['Wavelength'], newdf['Abs'], time_real

def plotting(y, z, time):
    fig, ax = plt.subplots(figsize=(12.8, 9.6))
    ax.set_xlabel('Wavelength (nm)', fontsize=18, labelpad=12)
    ax.set_ylabel('ΔAbsorbance (mOD)', fontsize=18, labelpad=12)
    plt.plot(y, z, 'k')
    title = input_path[0:4]+'  '+str(time)+' μs'
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
    if len(sys.argv) == 2:
        print("Lack of designated time or option")
    elif sys.argv[2].isdigit() == True:
        desigtime = sys.argv[2]
        x, z, time = designate_time(df, desigtime)
    elif sys.argv[2] == 'min' or sys.argv[2] == 'max':
        option = sys.argv[2]
        x, z, time = extract2D(df, option)
    else:
        print("Value Error: option should be min or max")
    
    plot = plotting(x, z, time) 
    #plot.savefig(input_path+str(sys.argv[2])+".png", bbox_inches='tight')
    

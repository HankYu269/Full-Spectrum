import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def extract2D(df, option):

    # Scattered points in wavelengths of 400~700 nm
    for i in range(1, len(df)):
        if (df[i, 0] > 400):
            wavestart = i
            break
    zdata = df[wavestart:, 1:]
    
    # Find global extrema
    if option == 'min':
        timeidx = np.unravel_index(np.argmin(zdata, axis=None), zdata.shape)[1]
    elif option == 'max':
        timeidx = np.unravel_index(np.argmax(zdata, axis=None), zdata.shape)[1]
    
    zlist = zdata[:, timeidx]
    ydata = df[wavestart:, 0]
    time_real = df[0, timeidx+1]
    return ydata, zlist, time_real

def designate_time(df, desigtime):
    for i in range(1, len(df)):
        if (df[i, 0] > 400):
            wavestart = i
            break
    newdf = pd.DataFrame(columns=['Wavelength', 'Abs'])
    newdf['Wavelength'] = df[wavestart:, 0]

    # Find actual wavelength
    for i in range(1, len(df)):
        if (desigtime <= df[0, i]):
            newdf['Abs'] = (df[wavestart:, i])
            time_real = df[0, i]
            break
    
    newdf['Abs'] = [i*1000 for i in newdf['Abs']]
    return newdf['Wavelength'], newdf['Abs'], time_real

def plotting(y, z, time):
    fig, ax = plt.subplots(figsize=(12, 8))
    font = {'family': 'arial', 'size': 19}
    plt.plot(y, z, 'k')
    plt.xlabel('Wavelength (nm)', fontdict=font, labelpad=13)
    plt.ylabel('Δ Abs. (AU)', fontdict=font, labelpad=20)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    title = input_path[0:4]+'  '+str(time)+' μs'
    plt.title(title, y=1.03, fontfamily='arial', fontsize=24, fontweight='semibold')
    ax.set_aspect(0.6/ax.get_data_ratio(), adjustable='box')
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.75)
    ax.tick_params(width=1.75)
    plt.show()
    return fig

if __name__ == '__main__':
    import sys
    import os
    input_path = sys.argv[1]
    df = pd.read_csv(input_path, header=None) # Remove last 4 arguments when there are no rows to be skipped
    df = np.array(df)
    input_path = os.path.splitext(input_path)[0]

    # Switch between time designation or global extrema finding
    if sys.argv[2].isdigit() == True:
        desigtime = int(sys.argv[2])
        x, z, time = designate_time(df, desigtime)
    elif isinstance(sys.argv[2], str):
        option = sys.argv[2]
        x, z, time = extract2D(df, option)
    
    fig = plotting(x, z, time) 
    #fig.savefig(input_path+str(sys.argv[2])+".png", bbox_inches='tight')
    
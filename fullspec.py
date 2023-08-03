import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import sgolay2 as sg2
import sys

def time_replace(df, pts, final_delay):
    """
    Replace the timestamps with experimental delay times
    """
    sampling_period = final_delay/pts
    for i in range(len(df.iloc[0])):
        df.iloc[0,i] = sampling_period*(i-1)
    df.iloc[0, 0] = 0
    return df

def plot_2d(df_plot, title):
    """
    Draw and save a 2D temporal raster plot
    """
    xdata, ydata = np.meshgrid(df_plot[1:, 0], df_plot[0, 1:])
    ydata = ydata/1000
    df_transposed = df_plot.T
    zdata = df_transposed[1:, 1:]

    # 2D Savitzky-Golay filter
    #zdata = sg2.SGolayFilter2(window_size=11, poly_order=2)(zdata)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    font = {'family': 'arial', 'size': 18, 'weight':'semibold'}

    # Self-defined normalized colormap
    #g = ax.pcolormesh(xdata, ydata, zdata, cmap='bwr', shading='auto')
    divergent_norm = colors.CenteredNorm()
    gnorm = ax.pcolormesh(xdata, ydata, zdata, cmap='bwr', shading='auto', norm=divergent_norm)
    """
    Recommended cmaps: 'rainbow', 'coolwarm', 'bwr'
    """

    cb = fig.colorbar(gnorm, aspect=30)
    cb.ax.tick_params(labelsize='large')
    cb.set_label(label='Δ Abs. (AU)',fontdict=font, labelpad=15)
    
    plt.xlabel('Wavelength (nm)', fontdict=font, labelpad=15)
    plt.ylabel('Delay Time (ms)', fontdict=font, labelpad=20)
    plt.xticks([400, 450, 500, 550, 600, 650, 700], fontsize=14)
    plt.yticks(fontsize=14)
    plt.title(title, y=1.03, fontfamily='arial', fontsize=25, fontweight='bold')
    ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.75)
    ax.tick_params(width=1.75)
    plt.show()
    return fig


def plot_3d(df_plot, title, pov):
    """
    Draw and save a 3D surface plot
    """
    xdata, ydata = np.meshgrid(df_plot[0, 1:], df_plot[1:, 0])
    xdata = xdata/1000
    zdata = df_plot[1:, 1:]

    # 2D Savitzky-Golay filter
    #zdata = sg2.SGolayFilter2(window_size=11, poly_order=2)(zdata)

    fig = plt.figure(figsize=(12, 8))

    # Axis settings
    ax = plt.axes(projection='3d')
    ax.set_xlabel('Delay Time (ms)', fontsize=15, labelpad=17)
    ax.set_ylabel('Wavelength (nm)', fontsize=15, labelpad=17)
    ax.set_zlabel('ΔAbs. (AU)', fontsize=15, labelpad=17)

    # Self-defined standardized colormap
    #g = ax.plot_surface(xdata, ydata, zdata, cmap='bwr')
    divergent_norm = colors.CenteredNorm()
    g = ax.plot_surface(xdata, ydata, zdata, cmap='bwr', norm=divergent_norm)

    font = {'family': 'arial', 'size': 23, 'weight': 'semibold'}
    if pov == 'full':
        ax.view_init(20, -130)
        cb = fig.colorbar(g, aspect=30, shrink=0.8)
        plt.title(title, x=0.53, y=1.0, fontdict=font)
    elif pov == 'top':
        ax.view_init(89.9, -90.1)
        ax.set_zlabel('')
        ax.set_zticks([])
        cb = fig.colorbar(g, aspect=30, shrink=0.7, pad=-0.03)
        plt.title(title, x=0.55, y=1.0, fontdict=font)
    elif pov == 'time':
        ax.view_init(6, -92)
        cb = fig.colorbar(g, aspect=30, shrink=0.6, pad=-0.03)
        plt.title(title, x=0.55, y=0.95, fontdict=font)
    elif pov == 'wave':
        ax.view_init(6, 0)
        cb = fig.colorbar(g, aspect=30, shrink=0.6, pad=0.01)
        plt.title(title, x=0.55, y=0.95, fontdict=font)
    else:
        sys.exit('Wrong input!')

    cb.set_label(label='Δ Abs. (AU)',fontfamily='arial', fontsize=15, labelpad=17)
    plt.show()
    return fig

def designate_wave(df, desigwave):
    """
    Extract 2D time-dependent data at the designated wavelength
    """
    newdf = pd.DataFrame(columns=['Time', 'Abs'])
    newdf['Time'] = df[0, 1:]
    newdf['Time'] = [i/1000 for i in newdf['Time']]

    # Find the actual wavelength
    for i in range(1, len(df)):
        if (desigwave <= df[i, 0]):
            newdf['Abs'] = (df[i, 1:])
            wave_real = df[i, 0]
            break
    
    return newdf['Time'], newdf['Abs'], wave_real

def extract2D(df, state):
    """
    Extract 2D time-dependent data at the designated intermediate state
    """
    # Find local extrema
    if state == 'g':
        for i in range(1, len(df)):
            if (df[i, 0] > 500):
                wavestart = i
                break
        zdata = df[wavestart:, 1:]
        waveidx, timeidx = np.unravel_index(np.argmin(zdata, axis=None), zdata.shape)
        zlist = zdata[waveidx, :]
        cri_wave = df[waveidx+wavestart, 0]
    elif state == 'l':
        for i in range(1, len(df)):
            if (df[i, 0] > 500):
                wavestart = i
                break
        for j in range(1, len(df)):
            if (df[j, 0] > 550):
                waveend = j
                break
        zdata = df[wavestart:waveend, 1:]
        waveidx, timeidx = np.unravel_index(np.argmax(zdata, axis=None), zdata.shape)
        zlist = zdata[waveidx, :]
        cri_wave = df[wavestart+waveidx, 0]
    elif state == 'm':
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
    elif state == 'o':
        for k in range(1, len(df)):
            if (df[k, 0] > 600):
                wavestart = k
                break
        zdata = df[wavestart:, 1:]
        waveidx, timeidx = np.unravel_index(np.argmax(zdata, axis=None), zdata.shape)
        zlist = zdata[waveidx, :]
        cri_wave = df[waveidx+wavestart, 0]
    
    xdata = df[0, 1:]
    xdata = xdata/1000
    cri_time = df[0, timeidx+1]
    cri_abs = df[waveidx+wavestart, timeidx+1]
    print("critical value: {} at {} nm, {} μs".format(cri_abs, cri_wave, cri_time))

    return xdata, zlist, cri_wave

def plotting(x, z, wave):
    fig, ax = plt.subplots(figsize=(12, 8))
    font = {'family': 'arial', 'size': 19}
    plt.plot(x, z, 'k')
    plt.xlabel('Delay Time (ms)', fontdict=font, labelpad=13)
    plt.ylabel('Δ Abs. (AU)', fontdict=font, labelpad=20)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    title = input_path[0:4]+'  '+str(wave)+' nm'
    plt.title(title, y=1.03, fontfamily='arial', fontsize=24, fontweight='semibold')
    ax.set_aspect(0.6/ax.get_data_ratio(), adjustable='box')
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.75)
    ax.tick_params(width=1.75)
    plt.show()
    return fig

if __name__ == '__main__':
    import os
    import click

    input_path = sys.argv[1]
    df = pd.read_csv(input_path, skiprows=5, header=None, index_col=None)
    pts, final_delay = int(input("Number of measurements: ")),int(input("Final integration delay (µs): "))
    df = time_replace(df, pts, final_delay)
    input_path = os.path.splitext(input_path)[0]
    df.to_csv(input_path+"_corr.csv", header=None, index=None)
    print("A corrected .csv file was saved\nPlotting 2D raster plots ...")
    
    df_plot = np.array(df, dtype=float)
    title = str(input("Title: "))
    fig = plot_2d(df_plot, title)
    fig.savefig(input_path+"_2D.png", bbox_inches='tight', transparent=True)
    print("A 2D temporal raster plot was saved\nPlotting 3D surface plots ...")
    pov = str(input("Point of view (full, top, time, or wave): "))
    fig = plot_3d(df_plot, title, pov)
    fig.savefig(input_path+"_3D.png", bbox_inches='tight')
    print("A 3D surface plot was saved")

    if click.confirm("Continue to extract 2D data at a designated wavelength?", default=True):
        desigwave = int(input("Designated wavelength (nm): "))
        x, z, wave = designate_wave(df_plot, desigwave)
        fig = plotting(x, z, wave)
        #fig.savefig(input_path+str(wave)+".png", bbox_inches='tight')
    elif click.confirm("Continue to extract 2D data of a designated intermediate state?", default=True):
        state = str(input("Designated state (g, l, m, or o): "))
        x, z, wave = extract2D(df_plot, state)
        fig = plotting(x, z, wave)
        #fig.savefig(input_path+str(wave)+".png", bbox_inches='tight')
    else:
        pass

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import sgolay2 as sg2


def pic_draw(df, view):

    fig = plt.figure(figsize=(50, 100))
    title = input_path[0:4]

    # Scattered points of wavelengths >400 nm
    df = np.array(df)
    xdata, ydata = np.meshgrid(df[0, 1:], df[36:, 0])
    zdata = df[36:, 1:]
    zdata = zdata*1000

    # 2D Savitzky-Golay filter
    zdata = sg2.SGolayFilter2(window_size=9, poly_order=2)(zdata)
    
    ax = plt.axes(projection='3d')
    ax.set_xlabel('Time (μs)', fontsize=12, labelpad=15)
    ax.set_ylabel('Wavelength (nm)', fontsize=12, labelpad=15)
    ax.set_zlabel('ΔAbsorbance (mOD)', fontsize=12, labelpad=15)

    g = ax.plot_surface(xdata, ydata, zdata, cmap='rainbow')
    # Recommended cmaps: 'rainbow', 'coolwarm', and 'jet'

    # Figure refinements
    if view == 'full':
        ax.view_init(20, -130)
        cb = fig.colorbar(g, shrink=0.7)
        fig.suptitle(title, x=0.56, y=0.9, fontfamily='arial', fontsize=25, fontweight='semibold')
    elif view == 'top':
        ax.view_init(89.9, -90.1)
        ax.set_zticks([])
        ax.set_zlabel('')
        cb = fig.colorbar(g, shrink=0.7, pad=-0.03)
        fig.suptitle(title, x=0.61, y=0.85, fontfamily='arial', fontsize=25, fontweight='semibold')
    elif view == 'time':
        ax.view_init(6, 90)
        cb = fig.colorbar(g, shrink=0.7)
        fig.suptitle(title, x=0.53, y=0.83, fontfamily='arial', fontsize=25, fontweight='semibold')
    elif view == 'wavelength':
        ax.view_init(6, 0)
        cb = fig.colorbar(g, shrink=0.7)
        fig.suptitle(title, x=0.53, y=0.83, fontfamily='arial', fontsize=25, fontweight='semibold')
    else:
        print("Value Error: view should be full, top, time, or wavelength")
    
    # Set colorbar label
    cb.set_label(label='ΔAbsorbance (mOD)',fontsize=12, labelpad=15)
    
    plt.show()
    return fig


if __name__ == '__main__':
    import sys
    import os
    input_path = sys.argv[1]
    view = sys.argv[2]
    df = pd.read_csv(input_path, skiprows=5, header=None, index_col=None)
    input_path = os.path.splitext(input_path)[0]
    plot = pic_draw(df, view)
    #plot.savefig(input_path+view+".png", bbox_inches='tight')

"""
2D Savitzky-Golay filter refers to https://github.com/espdev/sgolay2
"""

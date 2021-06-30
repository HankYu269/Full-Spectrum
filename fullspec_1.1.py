import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def pic_draw(df, view):

    fig = plt.figure(figsize=(50, 100))
    title = input_path[0:4]

    # Data for 3-dimensional scattered points
    df = np.array(df)
    zdata = df[30:, 1:]
    zdata = zdata*1000
    xdata, ydata = np.meshgrid(df[0, 1:], df[30:, 0])
    
    ax = plt.axes(projection='3d')
    ax.set_xlabel('Time (μs)', fontsize=12, labelpad=15)
    ax.set_ylabel('Wavelength (nm)', fontsize=12, labelpad=15)
    ax.set_zlabel('ΔAbsorbance (mOD)', fontsize=12, labelpad=15)

    g = ax.plot_surface(xdata, ydata, zdata, cmap='rainbow')

    # Figure refinements
    titlefont = {'family': 'arial', 'size': 25, 'weight': 'semibold'}
    if view == 'general':
        ax.view_init(20, -130)
        cb = fig.colorbar(g, shrink=0.7)
        cb.set_label(label='ΔAbsorbance (mOD)',fontsize=12, labelpad=15)
        fig.suptitle(title, y=0.9, fontdict=titlefont)
    elif view == 'wavelength':
        ax.view_init(3, 0)
        cb = fig.colorbar(g, shrink=0.7)
        cb.set_label(label='ΔAbsorbance (mOD)',fontsize=12, labelpad=15)
        fig.suptitle(title, x=0.53, y=0.83, fontdict=titlefont)
    elif view == 'top':
        ax.view_init(89.9, -90.1)
        ax.set_zticks([])
        ax.set_zlabel('')
        cb = fig.colorbar(g, shrink=0.7, pad=-0.03)
        cb.set_label(label='ΔAbsorbance (mOD)',fontsize=12, labelpad=15)
        fig.suptitle(title, x=0.61, y=0.85, fontdict=titlefont)
    else:
        print("Value Error: view should be general, wavelength, or top")
    
    plt.show()
    return fig


if __name__ == '__main__':
    import sys
    import os
    input_path = sys.argv[1]
    view = sys.argv[2]
    df = pd.read_csv(input_path, skiprows=5, header=None, index_col=None)
    input_path = os.path.splitext(input_path)[0]
    result = pic_draw(df, view)
    #result.savefig(input_path+view+".png", bbox_inches='tight')

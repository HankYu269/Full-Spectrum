import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def pic_draw(df, view):

    fig = plt.figure(figsize=(50, 100))
    df = np.array(df)
    ax = plt.axes(projection='3d')

    # Data for 3-dimensional scattered points
    zdata = df[30:, 1:]
    zdata = zdata*1000
    xdata, ydata = np.meshgrid(df[0, 1:], df[30:, 0])
    
    ax.set_xlabel('Time (μs)', fontsize=17, labelpad=12)
    ax.set_ylabel('Wavelength (nm)', fontsize=17, labelpad=12)
    ax.set_zlabel('ΔAbs (mOD)', fontsize=17, labelpad=30)

    g = ax.plot_surface(xdata, ydata, zdata, cmap='rainbow')
    
    cb = fig.colorbar(g)
    cb.set_label(label='ΔAbs (mOD)', fontsize=17, rotation=0, y=1.05)
    
    title = input_path[0:4]
    fig.suptitle(title, y=0.9, fontsize=22)

    # Viewpoints
    if view == "general":
        ax.view_init(20, -150)
    elif view == "wavelength":
        ax.view_init(0, 0)
    elif view == "top":
        ax.view_init(89.9, -90.1)
        ax.set_zticks([])
        ax.set_zlabel("")
        fig.suptitle(title, x=0.55, y=0.9, fontsize=22)
    else:
        print("Value Error: view should be general, wavelength, or top")
    
    plt.show()


if __name__ == '__main__':
    import sys
    import os
    input_path = sys.argv[1]
    view = sys.argv[2]
    df = pd.read_csv(input_path, skiprows=5, header=None, index_col=None)
    input_path = os.path.splitext(input_path)[0]
    pic_draw(df, view)
    # plt.savefig(input_path+".png")

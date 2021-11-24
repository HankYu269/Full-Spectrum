import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import sgolay2 as sg2


def pic_draw(df, view):

    fig = plt.figure(figsize=(12, 8))

    # Scattered points at 400~700 nm
    df = np.array(df)
    for i in range(1, len(df)):
        if (df[i, 0] > 400):
            wavestart = i
            break
    
    xdata, ydata = np.meshgrid(df[0, 1:], df[wavestart:, 0])
    zdata = df[wavestart:, 1:]
    zdata = zdata*1000

    # 2D Savitzky-Golay filter
    zdata = sg2.SGolayFilter2(window_size=11, poly_order=2)(zdata)
    
    # Axis settings
    ax = plt.axes(projection='3d')
    if (df[0, -1] > 10000):
        plt.xticks(rotation=-20)

    if (df[0, -1] >= 900000):
        plt.xticks(rotation=0)
        ax.set_xlabel('Delay Time (s)', fontsize=15, labelpad=17)
        ax.xaxis.offsetText.set_color('None')
    else:
        ax.set_xlabel('Delay Time (μs)', fontsize=15, labelpad=17)
    ax.set_ylabel('Wavelength (nm)', fontsize=15, labelpad=17)
    ax.set_zlabel('ΔAbs. (mAU)', fontsize=15, labelpad=17)

    # Self-defined standardized colormap
    try:
        divergent_norm = colors.TwoSlopeNorm(vcenter=0.0, vmin=np.min(zdata), vmax=np.max(zdata))
        g = ax.plot_surface(xdata, ydata, zdata, cmap='bwr', norm=divergent_norm)
        """
        Recommended cmaps: ('rainbow',) 'coolwarm', 'bwr'
        """
    except:
        g = ax.plot_surface(xdata, ydata, zdata, cmap='bwr')
    finally:
        pass

    # Plot refinements
    #ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    #ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    #ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    font = {'family': 'arial', 'size': 23, 'weight': 'semibold'}
    title = input_path[0:4]
    if view == 'full':
        ax.view_init(20, -130)
        cb = fig.colorbar(g, aspect=30, shrink=0.8)
        plt.title(title, x=0.53, y=1.0, fontdict=font)
    elif view == 'top':
        ax.view_init(89.9, -90.1)
        ax.set_zlabel('')
        ax.set_zticks([])
        cb = fig.colorbar(g, aspect=30, shrink=0.7, pad=-0.03)
        plt.title(title, x=0.55, y=1.0, fontdict=font)
    elif view == 'time':
        ax.view_init(6, -92)
        cb = fig.colorbar(g, aspect=30, shrink=0.6, pad=-0.03)
        plt.title(title, x=0.55, y=0.95, fontdict=font)
    elif view == 'wavelength':
        ax.view_init(6, 0)
        cb = fig.colorbar(g, aspect=30, shrink=0.6, pad=0.01)
        plt.title(title, x=0.55, y=0.95, fontdict=font)

    cb.set_label(label='Δ Abs. (mAU)',fontfamily='arial', fontsize=15, labelpad=17)
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
    plot.savefig(input_path+view+".png", bbox_inches='tight')

"""
2D Savitzky-Golay filter cf. https://github.com/espdev/sgolay2
"""

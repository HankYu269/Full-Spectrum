import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import sgolay2 as sg2

def pic_draw(df):

    # Scattered points at 400~700 nm
    df = np.array(df)
    for i in range(1, len(df)):
        if (df[i, 0] > 400):
            wavestart = i
            break
    
    xdata, ydata = np.meshgrid(df[wavestart:, 0], df[0, 1:])
    df_transposed = df.T
    zdata = df_transposed[1:, wavestart:]
    zdata = zdata*1000

    # 2D Savitzky-Golay filter
    zdata = sg2.SGolayFilter2(window_size=21, poly_order=2)(zdata)
    
    # Plotting
    fig, ax = plt.subplots(figsize=(12, 8))
    #g = ax.pcolormesh(xdata, ydata, zdata, cmap='coolwarm', shading='auto')
    """
    Recommended cmaps: ('rainbow',) 'coolwarm', 'bwr'
    """

    # Self-defined standardized colormap
    divergent_norm = colors.TwoSlopeNorm(vcenter=0.0, vmin=np.min(zdata), vmax=np.max(zdata))
    gnorm = ax.pcolormesh(xdata, ydata, zdata, cmap='bwr', shading='auto', norm=divergent_norm)
    
    font = {'family': 'arial', 'size': 20}
    plt.xlabel('Wavelength (nm)', fontdict=font, labelpad=15)
    plt.ylabel('Delay Time (μs)', fontdict=font, labelpad=20)
    plt.xticks([400, 450, 500, 550, 600, 650, 700], fontsize=14)
    plt.yticks(fontsize=14)
    title = input_path[0:4]
    plt.title(title, y=1.03, fontfamily='arial', fontsize=25, fontweight='semibold')
    ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.75)
    ax.tick_params(width=1.75)
    cb = fig.colorbar(gnorm, aspect=30)
    cb.ax.tick_params(labelsize='large')
    cb.set_label(label='Δ Abs. (mAU)',fontdict=font, labelpad=15)
    plt.show()
    return fig


if __name__ == '__main__':
    import sys
    import os
    input_path = sys.argv[1]
    df = pd.read_csv(input_path, skiprows=5, header=None, index_col=None)
    input_path = os.path.splitext(input_path)[0]
    plot = pic_draw(df)
    plot.savefig(input_path+"2D.png", bbox_inches='tight')

"""
2D Savitzky-Golay filter cf. https://github.com/espdev/sgolay2
"""

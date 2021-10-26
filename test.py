import matplotlib.pyplot as plt
import numpy as np
# from jupyterthemes import jtplot
# jtplot.style('onedork')

def plot_trace(v0, alpha, file=None, **kwargs):
    # acceleration of gravity
    g = 9.8066

    # time to max height
    tp = v0 * np.sin(alpha) / g

    # converting to time range
    t = np.linspace(0, 2 * tp, 1000)

    # x axis
    x = v0 * np.cos(alpha) * t

    # y axis
    y = v0 * np.sin(alpha) * t - g * (t**2) / 2

    # change size for figure
    plt.figure(figsize=(20, 10))

    plt.plot(x, y, **kwargs)

    # xlim
    plt.xlim([-1, np.max(x) * 1.1])

    # ylim
    plt.ylim([-1, np.max(y) * 1.1])

    # axis labels
    plt.xlabel('X', fontsize=24)
    plt.ylabel('Y', fontsize=24)

    # chart title
    plt.title(f'v_0 = {v0}, α = {alpha}', fontsize=32)

    plt.grid(True)

    # set legend
    if 'label' in kwargs:
        plt.legend(loc='best', fontsize=32)

    if file is not None:
        plt.savefig(file)

plot_trace(100, 0.5, 'trace')
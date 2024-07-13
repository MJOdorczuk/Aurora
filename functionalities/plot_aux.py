import numpy as np
from matplotlib.pyplot import get_cmap as get_cmap
import pandas as pd


def background(df: pd.DataFrame, ax: any, limits: tuple[int, int, int, int], z: int, field: any, steps: int=10):
    '''
    Display background for the plot with the given field data with contour lines.

    Args:
        - `df` - dataframe containing the background data. It has to include three coordinates `Structured Coordinates:0`, `Structured Coordinates:1` and `Structured Coordinates:2`, and the background field data under label given by attribute `field`.
        - `ax` - axis object for plotting,
        - `limits` - tuple of four limits for the plot in the order of (`xlow`, `xhigh`, `ylow`, `yhigh`):
            - `xlow` - lower limit of the plot in x-direction (`Structured Coordinates:0`),
            - `xhigh` - upper limit of the plot in x-direction (`Structured Coordinates:0`),
            - `ylow` - lower limit of the plot in y-direction (`Structured Coordinates:1`),
            - `yhigh` - upper limit of the plot in y-direction (`Structured Coordinates:1`),
        - `z` - z (`Structured Coordinates:1`) coordinate of the slicing plane,
        - `field` - field to be displayed as the background,
        - `steps` - number of contour levels to be displayed over the plot.
    '''
    xlow, xhigh, ylow, yhigh = limits
    xs = df["Structured Coordinates:0"]
    ys = df["Structured Coordinates:1"]
    zs = df["Structured Coordinates:2"]
    df = df[(zs==z)&(xs>=xlow)&(xs<=xhigh)&(ys>=ylow)&(ys<=yhigh)]
    phi = df[field]
    grid_x = np.unique(df["Structured Coordinates:0"])
    grid_y = np.unique(df["Structured Coordinates:1"])

    X, Y = np.meshgrid(grid_x, grid_y)
    PHI = phi.to_numpy().reshape(X.shape)

    ax.pcolor(X, Y, PHI, cmap=get_cmap("gray"))
    min_phi, max_phi = PHI.min(), PHI.max()
    ax.contour(X, Y, PHI, np.arange(min_phi, max_phi, (max_phi - min_phi) / steps), cmap=get_cmap("gray"))
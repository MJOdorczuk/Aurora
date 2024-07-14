from scipy.ndimage import uniform_filter

def smooth(df, axis, n, field):
    '''
    Smooth field data along the sepcified axis by local averaging.

    Args:
        - `df` - dataframe containing the background data. It has to include three coordinates `Structured Coordinates:0`, `Structured Coordinates:1` and `Structured Coordinates:2`, and the background field data under label given by attribute `field`.
        - `axis` - axis, along the smoothing is done. 0 for `x`, 1 for `y` and 2 for `z`,
        - `n` - length of the averaging window,
        - `field` - field to be smoothed,
    '''
    ys = df["Structured Coordinates:1"]
    zs = df["Structured Coordinates:2"]
    ny = ys[ys > ys.min()].first_valid_index()
    nz = zs[zs > zs.min()].first_valid_index()
    nd2p = df[field].to_numpy().reshape(-1, nz // ny, ny)
    if axis == 0:
        window = (1, 1, n)
    elif axis == 1:
        window = (1, n, 1)
    else:
        window = (n, 1, 1)

    smoothed = uniform_filter(nd2p, size=window)
    return smoothed.reshape((-1,))
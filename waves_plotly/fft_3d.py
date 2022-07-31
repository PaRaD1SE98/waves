import numpy as np
import plotly.graph_objects as go


def plot(fft, data):
    p_min = np.unravel_index(np.argmin(data), data.shape)
    p_max = np.unravel_index(np.argmax(data), data.shape)
    kx, ky, freq = np.meshgrid(fft.KX, fft.KY, fft.FREQ)
    fig = go.Figure(data=[
        go.Volume(
            x=kx.flatten(),
            y=ky.flatten(),
            z=freq.flatten(),
            value=data.flatten(),
            isomin=data[p_min[0], p_min[1], p_min[2]],
            isomax=data[p_max[0], p_max[1], p_max[2]],
            opacity=0.2,
            colorscale='Viridis',
            surface_count=5,
        )])
    fig.show()

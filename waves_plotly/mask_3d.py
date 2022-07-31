import numpy as np
import plotly.graph_objects as go


def plot(fft, data):
    kx, ky, freq = np.meshgrid(fft.KX, fft.KY, fft.FREQ)
    fig = go.Figure(data=[
        go.Volume(
            x=kx.flatten(),
            y=ky.flatten(),
            z=freq.flatten(),
            value=data.flatten(),
            isomin=0,
            isomax=1,
            opacity=0.2,
            colorscale='Viridis',
            surface_count=5,
        )])
    fig.show()

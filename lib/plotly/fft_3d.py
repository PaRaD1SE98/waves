import numpy as np
import plotly.graph_objects as go


def plot(fft, data, title=None, surface_count=10, output=None):
    p_min = np.unravel_index(np.argmin(data), data.shape)
    p_max = np.unravel_index(np.argmax(data), data.shape)
    kx, ky, freq = np.meshgrid(fft.shifted_KX, fft.shifted_KY, fft.FREQ)
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
            surface_count=surface_count,
        )])
    fig.update_layout(
        title=dict(
            text=title,
            y=0.9,
            x=0.5,
            xanchor='center',
            yanchor='top'),
        scene=dict(
            zaxis=dict(range=[0, fft.smpl_props.sft / 2]),
            xaxis_title='kx[1/m]',
            yaxis_title='ky[1/m]',
            zaxis_title='frequency[Hz]',
        ),
        scene_aspectmode='manual',
        scene_aspectratio=dict(x=1, y=1, z=1),
    )
    fig.show()
    if output:
        fig.write_html(f'output/{title}_{output}.html', include_plotlyjs="cdn")

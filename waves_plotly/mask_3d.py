import numpy as np
import plotly.graph_objects as go


def plot(fft, data, title=None, surface_count=10, output=None):
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
        ),
        scene_aspectmode='manual',
        scene_aspectratio=dict(x=1, y=1, z=1),
    )
    fig.show()
    if output:
        fig.write_html(f'output/{title}_{output}.html', include_plotlyjs="cdn")

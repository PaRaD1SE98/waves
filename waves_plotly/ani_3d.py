import plotly.graph_objects as go
import numpy as np


def plot(data, fps=10, title=None, output=None):
    p_min = np.unravel_index(np.argmin(data.z), data.z.shape)
    p_max = np.unravel_index(np.argmax(data.z), data.z.shape)

    fig = go.Figure()
    for step in np.arange(0, len(data.T)):
        fig.add_trace(
            go.Surface(
                visible=False,
                x=data.x,
                y=data.y,
                z=data.z[:, :, step],
                colorscale="Viridis",
                cmax=data.z[p_max[0], p_max[1], p_max[2]],
                cmin=data.z[p_min[0], p_min[1], p_min[2]],
            )
        )

    fig.data[0].visible = True

    steps = []
    for i, _ in enumerate(fig.data):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)},
                  {"title": "Slider switched to time: " + str(i * data.sample_props.dt)}],  # layout attribute
        )
        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Time: "},
        pad={"t": len(data.T)},
        steps=steps
    )]

    fig.update_layout(
        title=dict(
            text=title,
            y=0.9,
            x=0.5,
            xanchor='center',
            yanchor='top'),
        scene=dict(
            xaxis=dict(range=[0, data.sample_props.x_max]),
            yaxis=dict(range=[0, data.sample_props.y_max]),
            zaxis=dict(tickmode='linear',
                       tick0=0,
                       dtick=0.5,
                       range=[data.z[p_min[0], p_min[1], p_min[2]], data.z[p_max[0], p_max[1], p_max[2]]]),
        ),
        scene_aspectmode='manual',
        scene_aspectratio=dict(x=1, y=1, z=1),
        sliders=sliders
    )
    fig.show()
    if output:
        fig.write_html(f'output/ani_3d_{output}.html', include_plotlyjs="cdn")

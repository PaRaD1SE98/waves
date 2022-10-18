import numpy as np
import plotly
from plotly import express as px


def plot(data, fps=10, title=None, aspect_ratio=1, output=None, **kwargs):
    p_min = np.unravel_index(np.argmin(data.z), data.z.shape)
    p_max = np.unravel_index(np.argmax(data.z), data.z.shape)
    x, y, t = np.meshgrid(data.X, data.Y, data.T, indexing='ij')
    fig = px.density_heatmap(x=x.flatten(), y=y.flatten(), z=data.z.flatten(),
                             title=title,
                             animation_frame=t.flatten(),
                             nbinsx=data.sample_props.sp[1],
                             nbinsy=data.sample_props.sp[2],
                             range_color=[data.z[p_min[0], p_min[1], p_min[2]], data.z[p_max[0], p_max[1], p_max[2]]],
                             color_continuous_scale=plotly.colors.sequential.Viridis)
    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=aspect_ratio,
    )
    # animation speed settings
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000 / fps  # ms
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 0  # ms
    fig.show()
    if output:
        fig.write_html(f'output/{title}_{output}.html', include_plotlyjs="cdn")

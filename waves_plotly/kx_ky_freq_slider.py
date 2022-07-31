import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
from plotly import express as px


def f_val_to_idx(smpl_props, v):
    return int(round(v * smpl_props.t_max))


def plot(smpl_props, fft, shifted_fft):
    p_min = np.unravel_index(np.argmin(shifted_fft), shifted_fft.shape)
    p_max = np.unravel_index(np.argmax(shifted_fft), shifted_fft.shape)
    kx, ky, freq = np.meshgrid(fft.KX, fft.KY, fft.FREQ, indexing='ij')
    data = {'kx': kx.flatten(),
            'ky': ky.flatten(),
            'amplitude': shifted_fft.flatten(),
            'frequency': freq.flatten()}
    df = pd.DataFrame(data)
    # fig = go.Figure()
    # for step in np.arange(0, len(fft.FREQ)):
    #     fig.add_trace(
    #         go.Histogram2d(
    #             visible=False,
    #             x=kx,
    #             y=ky,
    #             z=shifted_fft[:, :, step],
    #             colorscale="Viridis",
    #             xbins=dict(size=smpl_props.sp),
    #             ybins=dict(size=smpl_props.sp),
    #             zmax=shifted_fft[p_max[0], p_max[1], p_max[2]],
    #             zmin=shifted_fft[p_min[0], p_min[1], p_min[2]],
    #         )
    #     )
    #
    # fig.data[0].visible = True
    #
    # steps = []
    # for i, _ in enumerate(fig.data):
    #     step = dict(
    #         method="update",
    #         args=[{"visible": [False] * len(fig.data)},
    #               {"title": "Slider switched to frequency: " + str(i * smpl_props.sft / smpl_props.sp)}],
    #         # layout attribute
    #     )
    #     step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    #     steps.append(step)
    #
    # sliders = [dict(
    #     active=0,
    #     currentvalue={"prefix": "Frequency: "},
    #     pad={"t": len(fft.FREQ)},
    #     steps=steps
    # )]
    #
    # fig.update_layout(
    #     xaxis=dict(range=[0, data.sample_props.x_max]),
    #     yaxis=dict(range=[0, data.sample_props.y_max]),
    #     sliders=sliders
    # )
    fig = px.density_heatmap(df, x='kx', y='ky', z='amplitude',
                             animation_frame='frequency',
                             nbinsx=smpl_props.sp[1],
                             nbinsy=smpl_props.sp[2],
                             range_color=[shifted_fft[p_min[0], p_min[1], p_min[2]],
                                          shifted_fft[p_max[0], p_max[1], p_max[2]]],
                             color_continuous_scale=plotly.colors.sequential.Viridis)
    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
    )
    fig["layout"].pop("updatemenus")  # optional, drop animation buttons
    fig.show()

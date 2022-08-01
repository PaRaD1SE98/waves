import numpy as np
import pandas as pd
import plotly
from plotly import express as px


def f_val_to_idx(smpl_props, v):
    return int(round(v * smpl_props.t_max))


def plot(fft, shifted_fft, title=None, c_scale_lim=False, aspect_ratio=None, output=None):
    p_min = np.unravel_index(np.argmin(shifted_fft), shifted_fft.shape)
    p_max = np.unravel_index(np.argmax(shifted_fft), shifted_fft.shape)
    FREQ = np.linspace(0, fft.smpl_props.sft / 2, int(fft.smpl_props.spt / 2))
    kx, ky, freq = np.meshgrid(fft.KX, fft.KY, FREQ, indexing='ij')
    data = {'kx': kx.flatten(),
            'ky': ky.flatten(),
            'amplitude': shifted_fft[:, :, 0:int(fft.smpl_props.spt / 2)].flatten(),
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
    fig = px.density_heatmap(
        df, x='kx', y='ky', z='amplitude',
        title=title,
        animation_frame='frequency',
        nbinsx=fft.smpl_props.spx,
        nbinsy=fft.smpl_props.spy,
        range_color=[shifted_fft[p_min[0], p_min[1], p_min[2]],
                     shifted_fft[p_max[0], p_max[1], p_max[2]]] if c_scale_lim else None,
        color_continuous_scale=plotly.colors.sequential.Viridis
    )
    if aspect_ratio is not None:
        if aspect_ratio == 'as_sample':
            fig.update_yaxes(
                scaleanchor="x",
                scaleratio=fft.smpl_props.spy / fft.smpl_props.spx,
            )
        elif aspect_ratio == 'as_value':
            fig.update_yaxes(
                scaleanchor="x",
                scaleratio=fft.smpl_props.sfy / fft.smpl_props.sfx,
            )
        elif type(aspect_ratio) == float:
            fig.update_yaxes(
                scaleanchor="x",
                scaleratio=aspect_ratio,
            )
    fig["layout"].pop("updatemenus")  # optional, drop animation buttons
    fig.show()
    if output:
        fig.write_html(f'output/{title}_{output}.html', include_plotlyjs="cdn")

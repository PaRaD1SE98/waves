import numpy as np
import pandas as pd
import plotly
from plotly import express as px


def plot(fft, shifted_fft, title=None, c_scale_lim=False, aspect_ratio=None):
    """

    :param fft:
    :param shifted_fft: data array
    :param title: graph title
    :param c_scale_lim: limit the color scale
    :param aspect_ratio: available values:
    'as_sample': good when value scale in two plotting dimensions is very different,
    'as_value': good when sampling size in two plotting dimensions is very different,
    """
    p_min = np.unravel_index(np.argmin(shifted_fft), shifted_fft.shape)
    p_max = np.unravel_index(np.argmax(shifted_fft), shifted_fft.shape)

    kx, ky, freq = np.meshgrid(fft.KX, fft.KY, fft.FREQ, indexing='ij')
    data_fft = {'kx': kx.flatten(),
                'ky': ky.flatten(),
                'freq': freq.flatten(),
                'amplitude': shifted_fft.flatten()}
    df_fft = pd.DataFrame(data_fft)
    fig = px.density_heatmap(
        df_fft, 'kx', 'freq', 'amplitude',
        title=title,
        animation_frame='ky',
        nbinsx=fft.smpl_props.spx,
        nbinsy=fft.smpl_props.spt,
        range_color=[shifted_fft[p_min[0], p_min[1], p_min[2]],
                     shifted_fft[p_max[0], p_max[1], p_max[2]]] if c_scale_lim else None,
        color_continuous_scale=plotly.colors.sequential.Viridis
    )
    if aspect_ratio is not None:
        if aspect_ratio == 'as_sample':
            fig.update_yaxes(
                scaleanchor="x",
                scaleratio=fft.smpl_props.spt / fft.smpl_props.spx,
            )
        elif aspect_ratio == 'as_value':
            fig.update_yaxes(
                scaleanchor="x",
                scaleratio=fft.smpl_props.sft / fft.smpl_props.sfx,
            )
        elif type(aspect_ratio) == float:
            fig.update_yaxes(
                scaleanchor="x",
                scaleratio=aspect_ratio,
            )
    fig.show()

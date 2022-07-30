import numpy as np
import pandas as pd
import plotly

from plotly import express as px


def plot(smpl_props, fft, shifted_fft):
    p_min = np.unravel_index(np.argmin(shifted_fft), shifted_fft.shape)
    p_max = np.unravel_index(np.argmax(shifted_fft), shifted_fft.shape)

    kx, ky, freq = np.meshgrid(fft.KX, fft.KY, fft.FREQ, indexing='ij')
    data_fft = {'kx': kx.flatten(),
                'ky': ky.flatten(),
                'freq': freq.flatten(),
                'amplitude': shifted_fft.flatten()}
    df_fft = pd.DataFrame(data_fft)

    fig5 = px.density_heatmap(df_fft, 'ky', 'freq', 'amplitude',
                              animation_frame='kx',
                              nbinsx=smpl_props.sp,
                              nbinsy=smpl_props.sp,
                              range_color=[shifted_fft[p_min[0], p_min[1], p_min[2]],
                                           shifted_fft[p_max[0], p_max[1], p_max[2]]],
                              color_continuous_scale=plotly.colors.sequential.Viridis)
    fig5.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
    )
    fig5.show()

import numpy as np
import plotly
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def wave1(x, t):
    return np.cos(t - x) + np.cos(1.2 * t - 1.2 * x)


x = np.arange(0, 100)
t = np.arange(0, 100)
x, t = np.meshgrid(x, t)
z = wave1(x, t)
fig = go.Figure(data=[
    go.Scatter3d(x=x.flatten(), y=t.flatten(), z=z.flatten(),
                 mode='markers',
                 marker=dict(size=2, color=z.flatten(), colorscale='Reds'),
                 opacity=0.5),
    go.Surface(z=z)
])
fig.show()

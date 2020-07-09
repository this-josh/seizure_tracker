import pandas as pd
import plotly.graph_objects as go
import numpy as np
from typing import Dict, Union, List

from statistical_params import get_cluster_info, get_clusters, get_intervals


def make_fig_text(cluster_info: Dict[int, Dict[str, Union[pd.Timestamp, int]]]) -> List[List[str]]:
    """
    Create a list of the start and end times of each cluster

    Parameters
    ----------
    cluster_info : Dict[int, Dict[str, Union[pd.Timestamp, int]]]
        Dictionary containing info on each cluster

    Returns
    -------
    List[List[str]]
        A list of start and end times for each cluster
    """
    custom_text = []
    for index,row in cluster_info.iterrows():
        custom_text.append([row.start.strftime('%H:%M %d/%m/%Y'),row.end.strftime('%H:%M %d/%m/%Y')])
    return custom_text

def make_timeseries(cluster_info: Dict[int, Dict[str, Union[pd.Timestamp, int]]]) -> go.Figure:
    """
    Make bar chart showing all clusters against time

    Parameters
    ----------
    cluster_info : Dict[int, Dict[str, Union[pd.Timestamp, int]]]
        Info on each cluster

    Returns
    -------
    go.Figure
        A bar chart showing all clusters against time
    """
    ms_in_day = 86400000
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
                x=cluster_info.middle, y=cluster_info.number, width = [ms_in_day]*len(cluster_info),
                text = cluster_info.number,
                customdata = make_fig_text(cluster_info),
                textposition='auto',
                hovertemplate =
                'Cluster started: %{customdata[0]}'+
                '<br>Cluster finished: %{customdata[1]}</br>',
                name='Seizures',
                marker_color='Red'
            ))
    fig.add_trace(go.Scatter(
        x=cluster_info.middle,
        y=cluster_info.number,
        mode='lines',
        line=dict(color='red', width=1, dash='dot'),
        line_shape='spline'
    ))

    fig.update_layout(
        title_text='Bono seizure clusters over time',
        xaxis_title="Time",
        yaxis_title="Number of seizures in the cluster",
    )
    fig = sort_font(fig
    )
    return fig

def sort_font(fig: go.Figure) -> go.Figure:
    """
    Change the font size and remove legend

    Parameters
    ----------
    fig : go.Figure
        A plotly figure

    Returns
    -------
    go.Figure
        A plotly figure with the updates
    """
    fig.update_layout(
        font=dict(
            size=18,
        ),
        showlegend=False
    )
    return fig

def make_hist(interval_df: pd.DataFrame) -> go.Figure:
    """
    Make histogram for the time between clusters

    Parameters
    ----------
    interval_df : pd.DataFrame
        A df containing interval_days and prev_cluster_size

    Returns
    -------
    go.Figure
        A histogram showing the time between clusters
    """
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=interval_df.interval_days, xbins=dict(start=0, end=30, size=2), marker=dict(
                    color='red',
                ),opacity=0.5))

    fig.update_layout(xaxis = dict(
            tickmode = 'linear',
            tick0 = 1,
        ))
    fig.update_layout(
            title_text='Days since previous seizure',
            xaxis_title="Days",
            yaxis_title="Number of times this interval occured",
        )
    fig = sort_font(fig)
    return fig


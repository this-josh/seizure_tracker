import pandas as pd
import datetime as dt
import plotly.graph_objects as go
import numpy as np

def get_data(df_url, print_tail=False):
    df=pd.read_csv(df_url, names=['Seizure'])
    df['Seizure'] = pd.to_datetime(df['Seizure'])
    df = df.set_index('Seizure')
    if print_tail:
        print(df.tail())
    return df

def get_clusters(df, gap = np.timedelta64(2,'D')):
    clusters = []
    cont=True
    ii = 0
    while cont:
        a = df.index[ii]
        start = a-gap
        end= a+gap
        clusters.append(df[start:end])
        ii += len(df[start:end])
        if ii>= len(df):
            cont = False
    return clusters

def get_cluster_info(clusters):
    cluster_info = {}
    for cluster in clusters:
        cluster_info[len(cluster_info)] = {'start':cluster.iloc[0].name, 'end': cluster.iloc[-1].name, 'number': len(cluster), 'width':cluster.iloc[-1].name-cluster.iloc[0].name}
    cluster_info = pd.DataFrame.from_dict(cluster_info, orient='index')
    cluster_info.loc[:,'middle'] = cluster_info.loc[:,'start']+dt.timedelta(days=0.5)
    return cluster_info


def make_fig_text(cluster_info):
    custom_text = []
    for index,row in cluster_info.iterrows():
        custom_text.append([row.start.strftime('%H:%M %d/%m/%Y'),row.end.strftime('%H:%M %d/%m/%Y')])
    return custom_text

def make_fig(cluster_info):
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
        font=dict(
            size=18,
        ),
        showlegend=False
    )
    return fig


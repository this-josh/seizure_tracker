import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import flask
import plotly.graph_objects as go
from make_graphs import make_timeseries, make_hist
from statistical_params import most_recent_seizure, get_clusters, get_cluster_info, get_intervals
from inout import get_data


server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

df=get_data()
clusters = get_clusters(df)
cluster_info = get_cluster_info(clusters)
intervals = get_intervals(cluster_info)
days_since = most_recent_seizure(df)

fig = make_hist(intervals)
fig = make_timeseries(cluster_info)


app.title = 'Seizure Tracker'
app.layout = html.Div([

    html.H1(
        children='Seizure Tracker',
        style={
            'textAlign': 'center',
        }),

    html.Div(
        dcc.Markdown(f'''
        The last seizure was **{days_since}** days ago.
        '''), style={
            'textAlign': 'center',
        }),

    html.Div([
    dcc.RadioItems(
        id = 'graph-type',
        options=[
            {'label': 'Clusters over time', 'value': 'bars_timeseries'},
            {'label': 'Time since last cluster', 'value': 'bars_time_comparison'},
        ],
        value='bars_timeseries',
        labelStyle={'display': 'inline-block'}
    ),
    ]),    
    

    dcc.Graph(
        id='bono-seizures',
        config={'responsive':'auto'}
    ),

    
])



@app.callback(Output(component_id='bono-seizures', component_property='figure'), [Input(component_id='graph-type', component_property='value')])
def update_fig(fig_type: str) -> go.Figure:
    """
    Based upon the radio buttons, present the correct fig

    Parameters
    ----------
    fig_type : str
        The radio button selected

    Returns
    -------
    go.Figure
        The appropriate figure
    """
    if fig_type == 'bars_time_comparison':
        fig = make_hist(intervals)
        return fig
    fig = make_timeseries(cluster_info)

    return fig

application = app.server
if __name__ == '__main__':
    application.run(debug=True)#, port=8000)# host='192.168.1.213'
    # application.run(debug=False, port=8080)





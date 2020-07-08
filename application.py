import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import flask
import plotly.express as px
from make_graphs import get_data, make_timeseries, make_hist
from statistical_params import most_recent_seizure, get_clusters, get_cluster_info, get_intervals

external_style_sheet = 'https://codepen.io/chriddyp/pen/bWLwgP.css'
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)#, external_stylesheets=external_style_sheet)

df_url='https://docs.google.com/spreadsheets/d/e/2PACX-1vT1E1Y9IohHUf_WI6bOaJ162ZnRIv39tJbVF8C7Ow0-wqN-DDxslgTfhsUwvQUqoXn-grW89r_BRIyw/pub?gid=0&single=true&output=csv'
df=get_data(df_url, print_tail=False)
clusters = get_clusters(df)
cluster_info = get_cluster_info(clusters)
intervals = get_intervals(cluster_info)
days_since = most_recent_seizure(df)


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
        # figure=(),
        # responsive='auto',
        config={'responsive':'auto'}
        # config={'fullFrame':True, 'responsive': True, 'autosize':False, 'frameMargins':0.01}
    ),

    
    # style={'width': '100%', 'height': '98%'}),

])

# @app.callback(Output['new_graph', 'fig' ],
#     [Input('city', 'value')])
# def update_thing(city):
#     print(city)
#     #TODO: ADD RADio buttons for graph selection
#     if city == 'NYC':
#         df = px.data.iris()
#         fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
#         return fig

# print(help(app.callback))

@app.callback(Output(component_id='bono-seizures', component_property='figure'), [Input(component_id='graph-type', component_property='value')])
def update_fig(fig_type):
    if fig_type == 'bars_time_comparison':
        fig = make_hist(intervals)
        return fig
    fig = make_timeseries(cluster_info)
    # fig.update_layout(autosize=True)#, width=900, height=500)

    return fig

@app.callback(
    Output(component_id='my-output', component_property='children'),
    [Input(component_id='my-input', component_property='value')]
)
def update_output_div(input_value):
    print(input_value)
    return 'Output: {}'.format(input_value)


application = app.server
if __name__ == '__main__':
    application.debug = True
    application.run()# host='192.168.1.213'
    # application.run(debug=False, port=8080)



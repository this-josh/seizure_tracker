import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import flask
from make_graphs import get_data,get_clusters, get_cluster_info, make_fig


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

# df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')	


df_url='https://docs.google.com/spreadsheets/d/e/2PACX-1vT1E1Y9IohHUf_WI6bOaJ162ZnRIv39tJbVF8C7Ow0-wqN-DDxslgTfhsUwvQUqoXn-grW89r_BRIyw/pub?gid=0&single=true&output=csv'
df=get_data(df_url, print_tail=False)
clusters = get_clusters(df)
cluster_info = get_cluster_info(clusters)
fig = make_fig(cluster_info)
# fig.layout.height = 12000
fig.update_layout(autosize=True)#, width=900, height=500)

app.layout = html.Div([
    dcc.Graph(
        id='bono-seizures',
        figure=fig,
        # responsive='auto',
        config={'responsive':'auto'}
        # config={'fullFrame':True, 'responsive': True, 'autosize':False, 'frameMargins':0.01}
    )],
    style={'width': '100%', 'height':'98%'}
)

application = app.server
if __name__ == '__main__':
    application.debug = True
    application.run()# host='192.168.1.213'
    # application.run(debug=False, port=8080)


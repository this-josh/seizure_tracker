import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import flask
import os
from waitress import serve
import plotly.graph_objects as go
from trackerApp.make_graphs import make_timeseries, make_cluster_hist, make_time_hist
from trackerApp.statistical_params import (
    most_recent_seizure,
    get_clusters,
    get_cluster_info,
    get_intervals,
    likelihood_of_seizure,
    estimate_cluster_size,
)
from trackerApp.inout import get_data


server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
df = get_data(os.getenv("SEIZURE_SHEET"))
make_time_hist(df)
clusters = get_clusters(df)
cluster_info = get_cluster_info(clusters)
intervals = get_intervals(cluster_info)
days_since = most_recent_seizure(df)
likelihood, next_updates, next_likelihood = likelihood_of_seizure(days_since, intervals)
next_cluster_size = estimate_cluster_size(cluster_info, days_since)

if days_since >= 2:
    likelihood_message = f"""Making the current likelihood of a seizure **{likelihood}%**, this will update to {next_likelihood}% in {next_updates} days."""
    if isinstance(likelihood, str):
        likelihood_message = f"""Making the current likelihood of a seizure **{likelihood}**, this will update to {next_likelihood}% in {next_updates} days."""

elif days_since == 1:
    likelihood_message = f"""As the most recent seizure was only {days_since} day ago, it is possible the cluster is still active"""
elif days_since == 0:
    likelihood_message = f"""As the most recent seizure was today, it is possible the cluster is still active"""


app.title = "Seizure Tracker"
app.layout = html.Div(
    [
        html.H1(children="Seizure Tracker", style={"textAlign": "center",}),
        html.Div(
            dcc.Markdown(f"""The last seizure was **{days_since}** days ago"""),
            style={"textAlign": "center",},
        ),
        html.Div(dcc.Markdown(likelihood_message), style={"textAlign": "center",}),
        html.Div(dcc.Markdown(next_cluster_size), style={"textAlign": "center",}),
        html.Div(
            [
                dcc.RadioItems(
                    id="graph-type",
                    options=[
                        {"label": "Clusters over time", "value": "bars_timeseries"},
                        {
                            "label": "Time since last cluster",
                            "value": "bars_time_comparison",
                        },
                        {
                            "label": "Hour of the day seizures have occured",
                            "value": "seizure_hour_comparison",
                        },
                    ],
                    value="bars_timeseries",
                    labelStyle={"display": "inline-block"},
                ),
            ]
        ),
        dcc.Graph(id="bono-seizures", config={"responsive": "auto"}),
    ]
)


@app.callback(
    Output(component_id="bono-seizures", component_property="figure"),
    [Input(component_id="graph-type", component_property="value")],
)
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
    if fig_type == "bars_time_comparison":
        fig = make_cluster_hist(intervals)
        return fig
    elif fig_type == "seizure_hour_comparison":
        fig = make_time_hist(df)
        return fig
    fig = make_timeseries(cluster_info)

    return fig


application = app.server
if __name__ == "__main__":
    serve(application, url_scheme="https")

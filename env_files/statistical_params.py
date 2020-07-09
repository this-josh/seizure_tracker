import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta, datetime
import pytz
import time

def most_recent_seizure(df: pd.DataFrame):
    most_recent = df.index[-1]
    time_diff = datetime.now(pytz.timezone('Europe/London')) - most_recent
    return time_diff.days

def get_clusters(df, gap = timedelta(days=2)):
    clusters = []
    cont=True
    ii = 0
    while cont:
        a = df.index[ii]
        start = a - gap
        if ii == 0: 
            start = a
        end = a + gap
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
    cluster_info.loc[:, 'middle'] = cluster_info.loc[:, 'start'] + dt.timedelta(days=0.5)
    return cluster_info

def get_intervals(cluster_info):
    intervals = {}
    for index, row in cluster_info.iterrows():
        if index == 0:
            continue
        this_interval = (row.start - cluster_info.loc[index - 1].end).days
        intervals[index] = {'interval_days': this_interval, 'prev_cluster_size': cluster_info.loc[index - 1].number}
    intervals = pd.DataFrame.from_dict(intervals, orient='index')
    return intervals

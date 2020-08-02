import pandas as pd
import datetime as dt
import numpy as np
from datetime import timedelta, datetime
import pytz
import time
from typing import List, Dict, Union

def _remove_outliers(values: pd.Series, num_sd: int = 2) -> pd.Series:
    """
    Remove outliers from a list of values

    Parameters
    ----------
    values : pd.Series
        A list of values
    num_sd : int, optional
        The number of standard deviations from the median to remove, by default 2

    Returns
    -------
    pd.Series
        The input series with outliers removed
    """
    sd = np.std(values)
    median = np.median(values)
    lower_bound  = median - (num_sd*sd)
    upper_bound = median + (num_sd*sd)
    if lower_bound < 0:
        lower_bound = 0
    return values[np.logical_and(values>=lower_bound, values<=upper_bound)]

def most_recent_seizure(df: pd.DataFrame) -> int:
    """
    Find the number of days since the last seizure

    Parameters
    ----------
    df : pd.DataFrame
        A df from the google sheets csv

    Returns
    -------
    int
        The number of days since a seizure
    """
    
    most_recent = df.index[-1]
    time_diff = datetime.now(pytz.utc) - most_recent
    if time_diff.days < 0:
        return 0
    return time_diff.days

def get_clusters(df: pd.DataFrame, gap_days=2) -> List[pd.DataFrame]:
    """
    Take the seizures csv and group events into clusters

    Parameters
    ----------
    df : pd.DataFrame
        The google sheets csv data
    gap : int, optional
        The number of days after a seizure that a clustered is considered over, by default timedelta(days=2)

    Returns
    -------
    List[pd.DataFrame]
        A list containing a dataframe for each cluster
    """
    gap_days = timedelta(gap_days)
    clusters = []
    cont=True
    ii = 0
    while cont:
        a = df.index[ii]
        start = a - gap_days
        if ii == 0: 
            start = a
        end = a + gap_days
        clusters.append(df[start:end])
        ii += len(df[start:end])
        if ii>= len(df):
            cont = False
    return clusters

def get_cluster_info(clusters: List[pd.DataFrame]) -> Dict[int, Dict[str, Union[pd.Timestamp, int]]]:
    """
    Get info on each cluster (start, middle, end, size, and length)

    Parameters
    ----------
    clusters : List[pd.DataFrame]
        A list of df for each cluster event, from get_clusters

    Returns
    -------
    Dict[int, Dict[str, Union[pd.Timestamp, int]]]
        A dictionary containing the start, middle and end time of each cluster, the number of seizures in the cluster, and the length of each cluster
    """
    cluster_info = {}
    for cluster in clusters:
        cluster_info[len(cluster_info)] = {'start':cluster.iloc[0].name, 'end': cluster.iloc[-1].name, 'number': len(cluster), 'width':cluster.iloc[-1].name-cluster.iloc[0].name}
    cluster_info = pd.DataFrame.from_dict(cluster_info, orient='index')
    cluster_info.loc[:, 'middle'] = cluster_info.loc[:, 'start'] + dt.timedelta(days=0.5)
    return cluster_info

def get_intervals(cluster_info: Dict[int, Dict[str, Union[pd.Timestamp, int]]]) -> pd.DataFrame:
    """
    Given info on each cluster, find time between them

    Parameters
    ----------
    cluster_info : Dict[int, Dict[str, Union[pd.Timestamp, int]]]
        Cluster info from get_cluster_info

    Returns
    -------
    pd.DataFrame
        The number of days between clusters, and how large the previous cluster was
    """
    intervals = {}
    for index, row in cluster_info.iterrows():
        if index == 0:
            continue
        this_interval = (row.start - cluster_info.loc[index - 1].end).days
        intervals[index] = {'interval_days': this_interval, 'prev_cluster_size': cluster_info.loc[index - 1].number}
    intervals = pd.DataFrame.from_dict(intervals, orient='index')
    return intervals

def likelihood_of_seizure(days_since, intervals):
    """ compare days since and the histogram to find the likelihood of a seizure occuring within the next 48 hours."""
    interval_list = intervals.interval_days.sort_values()
    interval_list = _remove_outliers(interval_list, num_sd=2)
    intervals_lower = interval_list[interval_list<=days_since]
    likelihood = len(intervals_lower) / len(interval_list)
    return int(likelihood * 100)



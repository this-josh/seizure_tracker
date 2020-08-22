import pandas as pd
import numpy as np
import datetime as dt
import pytz


def make_df(days_ago: int, df_len: int) -> pd.DataFrame:
    """
    Make a dataframe similar to the online csv

    Parameters
    ----------
    days_ago : int
        How many days ago the df should start at
    df_len : int
        How long the df should be

    Returns
    -------
    pd.DataFrame
        A df with a datetime index
    """
    start_date = dt.datetime.now(pytz.utc) - dt.timedelta(days=days_ago)
    times = [start_date + dt.timedelta(days=day + 1) for day in range(df_len)]
    values = [[val, val + 1] for val in range(df_len)]
    df = pd.DataFrame(values, times)
    return df


def make_full_df(
    days_ago_start: int = 100,
    len_cluster: int = 2,
    num_clusters: int = 6,
    cluster_interval: int = 14,
) -> pd.DataFrame:
    df_all = pd.DataFrame()
    for val in range(num_clusters):
        df = make_df(days_ago_start, len_cluster)
        df_all = df_all.append(df)
        days_ago_start -= cluster_interval

    return df_all

import pandas as pd
import numpy as np
import datetime as dt
import pytz

from trackerApp.statistical_params import _remove_outliers, most_recent_seizure, get_clusters

def test_remove_outliers():
    """
    Test the method _remove_outliers. Test against np arrays as the series index can change.
    """
    values = pd.Series([-200.4, 0, 10.2, 20, 30, 40, 50, 60, 70, 80, 90, 300])
    values_no_outliers = pd.Series([0.0, 10.2, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]).to_numpy()
    np.testing.assert_array_equal(values_no_outliers, _remove_outliers(values).to_numpy())

def make_df(days_ago, df_len)->pd.DataFrame:
    start_date = dt.datetime.now(pytz.utc)- dt.timedelta(days=days_ago)
    times = [start_date+dt.timedelta(days=day+1) for day in range(df_len)]
    values = [[val, val + 1] for val in range(df_len)]
    df = pd.DataFrame(values, times)
    return df


def test_most_recent_seizure():
    """
    Test most_recent_seizure. If days ago is negative, should return 0.
    """
    df_len = 15
    days_ago = {18: 3,
                5: 0
    }
    for num_days_ago in days_ago:
        df = make_df(num_days_ago, df_len)
        assert most_recent_seizure(df) == days_ago[num_days_ago]


def test_get_clusters():
    days_ago_start = 100
    len_cluster = 2
    df_all = pd.DataFrame()
    num_clusters = 6
    for val in range(num_clusters):
        df = make_df(days_ago_start, len_cluster)
        df_all = df_all.append(df)
        days_ago_start -= 14

    clusters = get_clusters(df_all)
    # check it found the six clusters
    assert len(clusters) == num_clusters

    for cluster in clusters:
        assert len(cluster) == len_cluster
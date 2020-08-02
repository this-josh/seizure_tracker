import pandas as pd
import numpy as np
import datetime as dt
import pytz

from constructors import make_df, make_full_df

from trackerApp.statistical_params import _remove_outliers, most_recent_seizure, get_clusters,get_cluster_info

def test_remove_outliers():
    """
    Test the method _remove_outliers. Test against np arrays as the series index can change.
    """
    values = pd.Series([-200.4, 0, 10.2, 20, 30, 40, 50, 60, 70, 80, 90, 300])
    values_no_outliers = pd.Series([0.0, 10.2, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]).to_numpy()
    np.testing.assert_array_equal(values_no_outliers, _remove_outliers(values).to_numpy())


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
    num_clusters = 6
    len_cluster = 2
    df = make_full_df(len_cluster=len_cluster, num_clusters=num_clusters)
    clusters = get_clusters(df)
    # check it found the six clusters
    assert len(clusters) == num_clusters

    for cluster in clusters:
        assert len(cluster) == len_cluster
import pandas as pd
import numpy as np

from trackerApp.statistical_params import _remove_outliers

def test_remove_outliers():
    """
    Test the method _remove_outliers. Test against np arrays as the series index can change.
    """
    values = pd.Series([-200.4, 0, 10.2, 20, 30, 40, 50, 60, 70, 80, 90, 300])
    values_no_outliers = pd.Series([0.0, 10.2, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]).to_numpy()
    np.testing.assert_array_equal(values_no_outliers, _remove_outliers(values).to_numpy())
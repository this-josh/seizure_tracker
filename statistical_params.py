import pandas as pd
import time

def most_recent_seizure(df: pd.DataFrame):
    most_recent = df.index[-1]
    time_diff = pd.to_datetime('today') - most_recent
    return time_diff.days

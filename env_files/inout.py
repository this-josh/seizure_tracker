import pandas as pd

def get_data(df_url: str = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT1E1Y9IohHUf_WI6bOaJ162ZnRIv39tJbVF8C7Ow0-wqN-DDxslgTfhsUwvQUqoXn-grW89r_BRIyw/pub?gid=0&single=true&output=csv', print_tail: bool = False) -> pd.DataFrame:
    """Read the seizure csv, return as df with utc datetime index

    Parameters
    ----------
    df_url : str
        url for the seizure csv
    print_tail : bool, optional
        Whether the df tail should be printed, by default False

    Returns
    -------
    pd.DataFrame
        The csv as a dataframe with a datetime index
    """

    df=pd.read_csv(df_url, names=['Seizure'])
    df['Seizure'] = pd.to_datetime(df['Seizure'],utc=True)
    df = df.set_index('Seizure')
    if print_tail:
        print(df.tail())
    return df

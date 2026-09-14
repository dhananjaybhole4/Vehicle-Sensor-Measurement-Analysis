import pandas as pd

def get_columns_stats(df: pd.DataFrame, column) -> tuple[float, float]:
    """output the mean and standard deviation of the requested column in the given dataframe

    Args:
        df (pd.DataFrame): given data in the form of pandas DataFrame
        column: column names

    Returns:
        tuple[float, float]: [mean of the column, standard deviation of the column] 
    """
    mean = df[column].mean()
    std = df[column].std()

    return mean, std

def get_columns_stats_tool(df: pd.DataFrame, column: str) -> str:
    """output the mean and standard deviation of the requested column in the given dataframe in string

    Args:
        df (pd.DataFrame): given data in the form of pandas DataFrame
        column (str): column name

    Returns:
        str: mean and standard deviation
    """
    if column not in df.columns:
        return "column not found in dataframe"
    
    mean, std = get_columns_stats(df, column)
    return f"mean of the {column}: {mean} and standard deviation of the {column}: {std}"
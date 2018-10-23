"""Module to clean the data
"""
import numpy as np
from collections import Counter
import datetime
import pandas as pd
import random
from scipy import stats
import matplotlib.pyplot as plt


def MissingValues(df):
    """ the point of this function is to deal
    with missing data points in a data set.
    It creates a new column in the data identifying
    what points were missing.
    Argument:
        df { DataFrame }: The data matrix
    Return:
        df { DataFrame} without any none values
    """
    df_temp = df
    # It then fills the missing values with random values from the row
    x = 0
    for col_num in range(len(df.columns)):
        column = df[df.columns[col_num]]
        # if any values in the column are missing
        if pd.isnull(column).any():

            # identifies missing values
            logicalMissing = pd.isnull(column)
            logicalFilled = [not i for i in logicalMissing]
            # and fills them from a random point in the data
            ran = random.choice(column[logicalFilled].tolist())
            column.fillna(ran, inplace=True)
            # then fills in a new row indicating which values were missing
            x = x + 1
            val = df.columns[col_num]
            df.insert(x, val + '_MissingLogical', logicalMissing)
        x = x + 1
    return df


def DatetimeToEPOCH(df):
    """
    Convert values in datatime format to DataFrame
    Arguments:
        df is a dataframe
    Returns:
        (df)
            -df: dataframe
    """
    for column in df:
        # if the column contains datetimes
        if isinstance(df[column][0], datetime.datetime):
            # converts all datetimes to EPOCH
            try:
                df[column] = df[column].astype(np.int64) // 10**9
                df.rename(columns={column: column + '_EPOCH'}, inplace=True)
            except:
                continue
    return df
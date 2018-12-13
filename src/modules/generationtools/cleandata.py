"""Module to clean the data
"""
import numpy as np
from collections import Counter
import datetime
import operator
import math
import pandas as pd
import random
from scipy import stats
import matplotlib.pyplot as plt
from scipy.stats import truncnorm

def preprocess(df):
    columns, df = add_columns(df)
    distributions, df = homogenize(df)
    return columns, distributions, df

def add_columns(df):
    columns = []
    new_df = df

    for index, header in enumerate(df):
        col = df[header]
        logical_empty = pd.isnull(col)

        if logical_empty.any():
            # keep track of this column for postprocessing
            columns.append(index)
            # find where to add next column in new_df
            insertion_index = index + len(columns)
            new_column_name = df.columns[index] + "_MissingLogical"
            meta_column = [int(not i) for i in logical_empty]
            choices = [element for element in col if not math.isnan(element)]

            for i in range(len(df.index)):
                if not meta_column[i]:
                    element = random.choice(choices)
                    new_df.at[i, header] = element

            new_df.insert(insertion_index, new_column_name, meta_column)

    return columns, new_df


def homogenize(df):
    data_types = []
    limits = {}
    counter = 0
    for col in df:
        if(is_categorical(df[col])):
            # new_col, limit = categorical_convert(df[col])
            # data_types[col] = 
            # limits[counter] = limit
            counter += 1
            # df[col] = new_col

    return "memes", df

def postprocess(df, columns, distributions):
    df = removeColumns(df, columns)
    df = recategorize(df, distributions)

def removeColumns(df, columns):
    for column in columns:
        for index in range(len(df.index)):
            if df.at[index][df[column + 1]] == 0:
                df.at[index][df[column]] = math.nan
        df = df.drop(columns = [df.columns[column + 1]])
    return df

def recategorize(df, distributions):
    return df

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

def DateTimeToEPOCH(df):
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

def is_categorical(col):
    """Identifies if a column is categorical:
        1) If all ints or strings: Categorical
        2) All floats or a mix of floats & ints: Non categorical

    Arguments:
        col {DataFrame Column} -- The column to iterate through and classify

    Returns:
        Boolean -- True if it is categorical, False if not
    """

    float_found = False
    for item in col:
        if isinstance(item, float):
            float_found = True
        elif isinstance(item, int):
            continue
        else:
            return True # Found something that is not a float or int
    return not float_found # True if all ints, false if atleast one float found

def rank_categories(col):
    """Ranks the column values in most frequent descending order
    
    Arguments:
        col {Dataframe Column} -- The column to sort
    
    Returns:
        [List] -- List of tuples of the value and percentage it occurs
    """

    categories = {}
    # Count the occurances
    for item in col:
        if item in categories.keys():
            categories[item] += 1
        else:
            categories[item] = 1
    # Convert to percentage
    for key in categories:
        categories[key] = categories[key] / len(col)
    categories = sorted(categories.items(),key=operator.itemgetter(1), reverse=True)
    return categories

def categorical_convert(col):
    """Encodes categorical data into ML-usable data
    
    Arguments:
        col {Dataframe column} -- The column to encode
    
    Returns:
        Dataframe column -- An encoded column
    """

    categories = rank_categories(col)
    distributions = {}
    limits = {}
    a = 0
    # for each category
    for item in categories:
        b = a + item[1]
        mu = (a+b) / 2
        sigma = (b-a) / 6
        mu, sigma = (a + b) / 2, (b - a) / 6
        distributions[item[0]] = truncnorm((a - mu) / sigma, (b - mu) / sigma, mu, sigma)
        limits[b] = item[0]
        a = b
    # sample from the distributions and return that value
    # IGNORE LIMITS BECAUSE IDK WHAT THAT IS
    new_df = col.apply(lambda x: distributions[x].rvs())
    return distributions, new_df

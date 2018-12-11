"""Module that deals with categorical data
"""
import pandas as pd
import operator
from scipy.stats import truncnorm


def identify(col):
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
    return col.apply(lambda x: distributions[x].rvs()), limits


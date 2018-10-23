"""Module to generate the model
"""
import scipy
import scipy.stats
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import expon, truncnorm, beta, uniform


def findBestDistribution(df):
    """Finds the best fit for each column and returns the associated parameters

    Arguments:
        df { DataFrame } -- The data matrix

    Returns:
        (Best Distribution, pvalue, params)
            - Best Distribution: The name of the best fitted graph
            - pvalue: The associated Pvalue generated from the KSTest
            - params: The parameters associated with the best fitted graph (e.g. min&max, alpha&beta)
    """

    dist_names = ['truncnorm', 'beta', 'expon', 'uniform']
    best_dist_name = [0] * len(df.columns)
    pvalues = [0] * len(df.columns)
    params = [0] * len(df.columns)
    for col_num in range(len(df.columns)):
        dist_tests = []
        param_tests = {}
        column = df[df.columns[col_num]]
        for dist_name in dist_names:
            dist = getattr(scipy.stats, dist_name)
            # Fit the data to the shape
            param = dist.fit(column)
            param_tests[dist_name] = param
            # Apply kstest
            dist, pv = scipy.stats.kstest(column, dist_name, args=param)
            dist_tests.append((dist_name, pv))
        # Select best distribution (Highest pvalue)
        best_dist, best_pv = (max(dist_tests, key=lambda item: item[1]))
        best_param = param_tests[best_dist]
        best_dist_name[col_num] = best_dist
        pvalues[col_num] = best_pv
        params[col_num] = best_param
    return best_dist, pvalues, params

def memes():
    print("ok")

# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later)
data = pd.read_csv("BreadBasket_DMS.csv")
best_dist, pvalues, params = findBestDistribution(data)
print(best_dist)
print(pvalues)
print(params)
memes(data)
# Preview the first 5 lines of the loaded data 
print(data.head())
print(data.size)
print("abc")

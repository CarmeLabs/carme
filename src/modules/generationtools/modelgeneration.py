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
        (best_dist_name, pvalue, params)
            - best_dist_name: List of best fitted graph for each column
            - pvalue: The associated Pvalue generated from the KSTest
            - params: The parameters associated with the best fitted
                      graph (e.g. min&max, alpha&beta)
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
    return best_dist_name, pvalues, params

def findCovariances(df, dists, params):
    """Finds the covariances between columns using a multivariate Gaussian
    Copula, following these steps:
    1. Begin with columns 0, ..., n, and corresponding cdfs F_0, ..., F_n.
    2. Iterate by row vectors, where each row is X = (x_0, ..., x_n)
    3. Transform each row into a new row Y = invNorm(F_0(x_0)), ...,
       invNorm(F_n(x_n))
    4. Compute covariance matrix from new transformed table

    Arguments:
        df { DataFrame } -- The data matrix
        dists { List } -- List of best fit distribution names
        params { List } -- List of parameter tuples for each distribution

    Returns:
        covariance matrix of transformed table
    """
    transformed_data = []
    for index, row in df.iterrows():
        new_row = []
        for value, dist_name, param in zip(row, dists, params):
            # for each row, apply transformation
            dist = getattr(scipy.stats, dist_name)
            cdf = dist.cdf(value, *param)
            # prevent extreme or infinite values
            if cdf < 0.01:
                cdf = 0.01
            elif cdf > 0.99:
                cdf = 0.99
            print(scipy.stats.norm.ppf(cdf))
            new_row.append(scipy.stats.norm.ppf(cdf))
        transformed_data.append(new_row)
    data = list(map(list, zip(*transformed_data)))
    print(data)
    # calculate covariance matrix using numpy.cov
    cos = np.cov(data)
    return cos

'''
Sample use:

data = pd.read_csv("test.csv")
dists, pvalues, params = findBestDistribution(data)
cos = findCovariances(data, dists, params)
'''
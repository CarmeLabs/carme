"""Module to synthesize the data
"""
import modelgeneration as mg
import scipy
import scipy.stats
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import expon, truncnorm, beta, uniform, norm
from cleandata import MissingValues, DatetimeToEPOCH
from categorical import identify, categorical_convert

def sample(f, sigma):
    '''
    Returns a single sample row based on list of distributions and covariance
    matrix

    Arguments:
        f { tuple of two lists } -- two lists: the list of distributions and
        the corresponding list of lists of parameters

        sigma { matrix } -- covariance matrix returned by findCovariances()

    Returns:
        list representing a single generated fake data entry
    '''

    v = np.random.normal(0, 1, len(sigma))
    l = np.linalg.cholesky(sigma)
    u = np.matmul(l, v)
    x = [getattr(scipy.stats, f[0][k]).ppf(norm.cdf(u[k]), *f[1][k]) for k in range(len(u))]
    return x

def synthesize_table(file_in, file_out, lines = 0):
    '''
    Reads in an input file, synthesizes data, saves in new output file.
    If lines is not specified, output file will be the same size as input file.

    Arguments:
        file_in { string } -- path to input file (should be csv)

        sigma { matrix } -- covariance matrix returned by findCovariances()

    Returns:
        list representing a single generated fake data entry
    '''

    # read in file
    try:
        df = pd.read_csv(file_in)
    except Exception as e:
        print(e)
        return

    # Fix missing values in the DF & Change datetimes
    df = MissingValues(df)
    df = DatetimeToEPOCH(df)

    limits = {}
    counter = 0
    for col in df:
        if(identify(df[col])):
            new_col, limit = categorical_convert(df[col])
            limits[counter] = limit
            counter += 1
            df[col] = new_col
    
    # calculate distributions and covariances using tools in model_generation.py
    dists, pvalues, params = mg.findBestDistribution(df)
    f = (dists, params)
    sigma = mg.findCovariances(df, dists, params)

    # find number of lines
    if lines == 0: lines = len(df.index)

    # synthesize data and save
    new_df = pd.DataFrame(columns = list(df))
    for k in range(lines):
        new_df.loc[k] = sample(f, sigma)
    new_df.to_csv(file_out, index = False)


if __name__ == "__main__":
    synthesize_table("test.csv", "s_test.csv")
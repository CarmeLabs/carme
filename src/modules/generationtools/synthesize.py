"""Module to synthesize the data
"""
import scipy
import scipy.stats
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import expon, truncnorm, beta, uniform, norm
from .cleandata import MissingValues, DateTimeToEPOCH
from .categorical import identify, categorical_convert, undo_cat
from .modelgeneration import ModelGenerator as mg

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
        
        file_out { string } -- path to output file - will overwrite

        lines { integer } -- number of data points desired in output file - if 
        argument is not given, file_out will contain the same number of data
        points as file_in
    '''

    # read in file
    try:
        df = pd.read_csv(file_in)
    except Exception as e:
        print(e)
        return

    # Fix missing values in the DF & Change datetimes
    df = MissingValues(df)
    df = DateTimeToEPOCH(df)

    limits = {}
    for col in df:
        if(identify(df[col])):
            new_col, limit = categorical_convert(df[col])
            limits[col] = limit
            df[col] = new_col

    # calculate distributions and covariances using tools in model_generation.py
    dists, pvalues, params = mg.findBestDistribution(df)
    f = (dists, params)
    sigma = mg.findCovariances(df, dists, params)
    if lines == 0: lines = len(df.index)

    # synthesize data
    new_df = pd.DataFrame(columns = list(df))
    for k in range(lines):
        new_df.loc[k] = sample(f, sigma)
    
    for col in new_df.columns:
        if col in limits:
            new_df[col] = undo_cat(new_df[col], limits[col])

    new_df.to_csv(file_out, index = False)

"""Module that deals with categorical data
"""
import pandas as pd


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


def main():
    data = pd.read_csv('test.csv')    
    for col in data:
        print(identify(data[col]))

if __name__ == "__main__":
    main()
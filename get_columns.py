import pandas as pd

def return_columns(dataframe):
    columns_list = dataframe.columns.tolist()
    columns_dict = {}

    for i, column in enumerate(columns_list):
        columns_dict[i + 1] = columns_list[i]
    
    return columns_dict
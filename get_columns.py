import pandas as pd
import time

def return_columns():
    house_list = pd.read_csv(f'./data/house_list.csv')
    columns_list = house_list.columns.tolist()
    columns_dict = {}

    for i, column in enumerate(columns_list):
        columns_dict[i + 1] = columns_list[i]
    
    return columns_dict
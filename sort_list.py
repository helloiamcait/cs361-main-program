import ast
import pandas as pd
import time

def sort_list(param, direction):

    with open('./pipes/sorted_by.txt', 'r') as sorted_by_pipe:
        sorted_by = sorted_by_pipe.read()
    sorted_by_pipe.close()
    sorted_by_tuple = ast.literal_eval(sorted_by)

    # Sort house list by column and direction given in tuple
    house_list = pd.read_csv(f'./data/house_list.csv')
    house_list = house_list.sort_values(by=param, 
                                        ascending=direction)

    if direction is True:
        sort_dir = '▲'
    else:
        sort_dir = '▼'


    # Remove dir symbol from old sorted column
    old_sorted_by = sorted_by_tuple[0][:-2]
    house_list = house_list.rename(columns={sorted_by_tuple[0]:old_sorted_by})

    # Add dir symbol to new sorted column
    new_sorted_by = f"{param} {sort_dir}"
    house_list = house_list.rename(columns={param:new_sorted_by})
    house_list.to_csv("./data/house_list.csv", index=False)
    
    with open('./pipes/sorted_by.txt', 'w') as sorted_by_pipe:
        sorted_by_pipe.write(f'("{new_sorted_by}", {direction})')
    sorted_by_pipe.close()
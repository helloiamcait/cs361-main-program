import time
import pandas as pd

def get_high_score_item():
    """
    Checks a column in a dataframe for the highest numberical value.
    Adds the high score item ID (value in the first column of that row) to the pipe.
    """
    with open("../pipes/high_score_pipe.txt", "r") as high_score_pipe:
        df_and_col = high_score_pipe.read()
    high_score_pipe.close()

    if df_and_col != '':
        df_and_col_list = df_and_col.split(",")
        df_path = df_and_col_list[0]
        df = pd.read_csv(f'{df_path}')
        total_score_col = df_and_col_list[1]

        sorted_df = df.sort_values(by=total_score_col, ascending=False)
        high_score_address = sorted_df.iloc[0,0]

        with open("../pipes/high_score_pipe.txt", "w") as high_score_pipe:
            high_score_pipe.write(high_score_address)
        high_score_pipe.close()
    
if __name__ == "__main__":
    while True:
        get_high_score_item()
        time.sleep(2)



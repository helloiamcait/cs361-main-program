from datetime import datetime
import time

def get_days_since():
    with open("../pipes/days_since_pipe.txt", "r") as days_since_pipe:
        date_input = days_since_pipe.read()
    days_since_pipe.close()

    if date_input != '':    
        current_date = datetime.today()

        # Get given date string as integers
        date_format = "%Y-%m-%d"
        start_date = datetime.strptime(date_input, date_format)
        days_between = current_date-start_date
        
        with open("./pipes/days_since_pipe.txt", "w") as days_since_pipe:
            days_since_pipe.write(str(days_between.days))
        days_since_pipe.close()

if __name__ == "__main__":
    while True:
        get_days_since()
        time.sleep(2)
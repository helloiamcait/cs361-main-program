from tabulate import tabulate
import time
import pandas as pd
import ast
import sys
from fuzzywuzzy import process # type: ignore
from get_menu import return_menu
from get_columns import return_columns
from sort_list import sort_list

def display_intro():
    # Display a message introducing the program
    with open('./text/intro_msg.txt', 'r') as intro_txt:
        intro_msg = intro_txt.read()
    intro_txt.close()
    print(intro_msg)

def display_outtro():
    # Display a message introducing the program
    with open('./text/outro_msg.txt', 'r') as outro_txt:
        outro_msg = outro_txt.read()
    outro_txt.close()
    print(outro_msg)

def setup_priorities():
    house_list_df = pd.read_csv(f'./data/house_list.csv')
    house_columns_list = house_list_df.columns.tolist()
    if house_columns_list[-1] != "Total score":
        print("Before we begin, you need to add priority house characterstics and their importance to you.")

        valid_input = False
        while not valid_input:
            num_priorities = input("How many priorities would you like to add? ")
            if num_priorities.isdigit():
                valid_input = True
            else:
                print("Invalid input. Please enter a number.\n")

        for i in range(int(num_priorities)):
            _add_priority()
        add_priorities_to_house_list()


def main_menu():
    # Prompt user to select menu item
    print(f"\n----------------------------[     MAIN MENU     ]"\
        "----------------------------\n")
    selection = request_menu("main_menu")
    _main_menu_execute(selection)

def _main_menu_execute(selection):
    """Executes the action the user selected in the main menu."""
    if selection == "1":
        view_house_list()
    elif selection == "2":
        view_house()
    elif selection == "3":
        add_house()
    elif selection == "4":
        display_outtro()
        sys.exit()
    # Error message for invalid selection
    else:
        print(f"⚠️ {selection} is not a valid option. Please enter a number between 1–4.")
        
        # Promtp user to enter a valid selection number
        return_to_main_menu()


def view_house_list():
    print(f"\n-------------------------[     VIEW HOUSE LIST     ]"\
          "-------------------------\n")
    house_list = pd.read_csv(f'./data/house_list.csv')

    # Check if house list is empty
    if len(house_list) == 0:
        print("\nYour house list is empty.")
        return_to_main_menu()
    else:
        # Display House List header
        print(tabulate(house_list, headers = 'keys', tablefmt = 'fancy_outline'))

        valid_input = False
        while not valid_input:
            # Display House List menu
            selection = request_menu('view_house_list_menu')
            if selection == "1":
                _sort_list()
            elif selection == "2":
                return_to_main_menu()


def _sort_list():
    print(f"\n:::::: VIEW HOUSE LIST > SORT LIST ::::::\n")
    print(f"Choose one of the following parameters to sort by:")
    house_list = pd.read_csv(f'./data/house_list.csv')
    selected_col_tuple = choose_column(house_list)
    col_name = selected_col_tuple[0]
    col_num = selected_col_tuple[1]
        
    # Prompt user for sort direction
    print(f"\nChoose sort direction:\n")
    valid_sort_dir = False
    while not valid_sort_dir:
        print(f"1. Ascending\n2. Descending\n")
        sort_dir_input = input(f"Enter your choice (1–2): ")

        if sort_dir_input == "1":
            sort_dir_bool = True
            sort_dir_text = 'Ascending'
            valid_sort_dir = True
        elif sort_dir_input == "2":
            sort_dir_bool = False
            sort_dir_text = 'Descending'
            valid_sort_dir = True
        else:
            invalid_input_alert(sort_dir_input, 2)

    # Write sort by and direction parameters to sort_columns pipe
    sort_list(col_name, sort_dir_bool)

    # Display confirmation of sort
    print(f"\n✅ Your house list was successfully sorted by {col_name} ({sort_dir_text})!\n")
    view_house_list()


def add_house():
    # Display Add House header
    print(f"\n----------------------------[     ADD HOUSE     ]"\
          f"----------------------------\n")

    # Print column names and get dictionary of house list column names
    house_list_df = pd.read_csv(f'./data/house_list.csv')
    columns_dict = return_columns(house_list_df)

    # Get number of column names in columns dict
    num_columns = len(columns_dict)

    new_house_list = []
    # Prompt user for house parameters
    print("Enter the following information about the house (or enter ! to cancel)...")
    for num, col in columns_dict.items():
        if col == "Total score":
            total_score = get_total_score(new_house_list)
            new_house_list.append(total_score)
        else:
            new_house_list.append(get_input(f"{num}. {col}: "))
    
    confirm_valid = False
    while not confirm_valid:
        confirm_add = input(f"‼️ Are you sure you want to add this house your list (y/n)? ")
        if confirm_add.lower() == "y":
            confirm_valid = True
            house_list = pd.read_csv(f'./data/house_list.csv')
            house_list.loc[len(house_list)] = new_house_list
            house_list.to_csv("./data/house_list.csv", index=False)
            return_to_main_menu()
        elif confirm_add.lower() == "n": 
            confirm_valid = True
            return_to_main_menu()
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
        


def view_house(house_address=None):
    print(f"\n---------------------------[     VIEW HOUSE     ]"\
          f"---------------------------\n")

    # Get house list dataframe
    house_list_df = pd.read_csv(f'./data/house_list.csv')
    house_address_list = house_list_df.iloc[:, 0].tolist()

    if house_address == None:
        house_address = find_match(house_address_list, "house")
    
    _view_house_helper(house_address)

    # Display View House menu
    selection = request_menu("view_house_menu")
    # If Edit house is selected
    if selection == "1":
        _edit_house(house_address)    
    # If Remove house is selected
    elif selection == "2":
        _remove_house(house_address)
    # If Return to main menu is selected
    elif selection == "3":
        return_to_main_menu()

def _view_house_helper(house_address):
    # Get house list dataframe
    house_list_df = pd.read_csv(f'./data/house_list.csv')
    house_row_list = house_list_df[house_list_df.iloc[:, 0] == house_address].values.flatten().tolist()

    # Get dictionary of house list column names
    columns_dict = return_columns(house_list_df)

    # Get number of column names in columns dict
    num_columns = len(columns_dict)
    
    # Get column names and list numbered
    column_names = []
    for key, value in columns_dict.items():
        column_names.append(value)
    
    house_df = pd.DataFrame(house_row_list, column_names)
    print(f"\n")
    print(tabulate(house_df[1:], headers = [f"🏡 {house_df.iloc[0,0]}", ""] , tablefmt = 'simple'))
    print(f"\n")

def _edit_house(house_address):
    print(f"\n:::::: VIEW HOUSE > EDIT HOUSE ::::::")
    # Get house list dataframe
    house_list_df = pd.read_csv(f'./data/house_list.csv')
    selected_col_tuple = choose_column(house_list_df)
    col_name = selected_col_tuple[0]
    col_num = selected_col_tuple[1]
    address_col_head = house_list_df.columns[0]

    # Prompt the user for the new value
    new_val = input(f"Input the new {col_name} value: ")
    if new_val.isdigit():
        new_val = int(new_val)

        confirm_valid = False
        while not confirm_valid:
            # Confirm that the user wants to make the edit
            confirm_edit = input(f"‼️ Are you sure you want to edit {house_address}? (y/n): ")
            if confirm_edit.lower() == "y":
                confirm_valid = True
                # Get house list dataframe
                house_list_df = pd.read_csv(f'./data/house_list.csv')

                # Edit house parameter value
                house_list_df.loc[house_list_df[address_col_head] == house_address, col_name] = new_val
                house_list_df.to_csv("./data/house_list.csv", index=False)
                
                if col_num == "1":
                    print(f"\n✅ {new_val} house was successfully edited.\n")
                    view_house(new_val)
                else:
                    print(f"\n✅ {house_address} house was successfully edited.\n")
                    view_house(house_address)
            elif confirm_edit.lower() == "n":
                confirm_valid = True
                view_house(house_address)
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

def _remove_house(house_address):
    print(f"\n:::::: VIEW HOUSE > REMOVE HOUSE ::::::")
    # Get house list dataframe
    house_list_df = pd.read_csv(f'./data/house_list.csv')
    address_col_head = house_list_df.columns[0]

    confirm_valid = False
    while not confirm_valid:
        confirm_add = input(f"‼️ Are you sure you want to remove {house_address} from your list? (y/n): ")
        if confirm_add.lower() == "y":
            confirm_valid = True
            # Get house list dataframe
            house_list_df = pd.read_csv(f'./data/house_list.csv')

            # Remove house row from dataframe
            house_list_df = house_list_df[house_list_df[address_col_head] != house_address]
            house_list_df.to_csv("./data/house_list.csv", index=False)
            print(f"✅ {house_address} house was successfully removed from your house list.\n")
            return_to_main_menu()
        elif confirm_add.lower() == "n":
            confirm_valid = True
            view_house(house_address)
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    
# def view_priorities():
#     print(f"\n-------------------------[     VIEW PRIORITIES     ]"\
#           "-------------------------\n")
#     priority_df = pd.read_csv('./data/priorities.csv')

#     # Check if priorities list is empty
#     if len(priority_df) == 0:
#         print("\nYou have not set any priorities.")
#         print("Add a priority to get started.\n")
#         _add_priority()
#     else:
#         print(tabulate(priority_df, headers = 'keys', tablefmt = 'fancy_outline', showindex=False))
#     time.sleep(2)
#     return_to_main_menu()

def _add_priority():
    """
    Prompts the user for a priority name and weight for scoring each house.
    Adds the priority and weight to a CSV file.
    """
    priority_name = get_input("\nEnter a priority home characteristic: ")
    priority_weight = get_input("Enter a weight for this priority (1 = least important, 5 = most important): ")

    # Validate the priority weight input
    valid_input = False
    while not valid_input:
        if not priority_weight.isdigit or int(priority_weight) > 5 or int(priority_weight) < 1:
            invalid_input_alert(priority_weight, 5)
        else:
            valid_input = True
    
    confirm_valid = False
    while not confirm_valid:
        confirm_add = input(f"‼️ Are you sure you want to add this priority your list (y/n)? ")
        if confirm_add.lower() == "y":
            confirm_valid = True
            # Add priority and weight to CSV
            new_priority_df = pd.DataFrame([{"Priority": priority_name, "Weight": priority_weight}])
            new_priority_df.to_csv('./data/priorities.csv', mode="a", header=False, index=False)
        elif confirm_add.lower() == "n":
            confirm_valid = True
            _add_priority()
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def add_priorities_to_house_list():
    priority_list_df = pd.read_csv("./data/priorities.csv")
    num_of_priorities = len(priority_list_df)
    house_list_df = pd.read_csv("./data/house_list.csv")
    priority_row_index = 0

    for i in range(num_of_priorities):
        priority_name = priority_list_df.iloc[priority_row_index, 0]  # get priority name
        priority_row_index += 1
        house_list_df[priority_name] = ''    
    
    house_list_df["Total score"] = ''
    house_list_df.to_csv(f'./data/house_list.csv', index=False)

# def _edit_priority():
#     """
#     Prompts the user for a priority name and weight for scoring each house.
#     Adds the priority and weight to a CSV file.
#     """
#     print(f"\n:::::: VIEW HOUSE > EDIT PRIORITY ::::::")
#     priority_df = pd.read_csv('./data/priorities.csv')
    
#     # Prompt user for priority to change
#     priority_list = priority_df.iloc[:, 0].tolist()
#     priority_to_edit = find_match(priority_list, "priority")

#     # Get the priority parameter the user wants to change
#     selected_col_tuple = choose_column(priority_df)
#     col_name = selected_col_tuple[0]
#     col_num = selected_col_tuple[1]
#     priority_col_head = priority_df.columns[0]

#     # Prompt the user for the new value
#     new_val = input(f"Input the new {col_name} value: ")
#     if new_val.isdigit():
#         new_val = int(new_val)

#     # Confirm that the user wants to make the edit
#     confirm_edit = input(f"\n‼️ Are you sure you want to edit {priority_to_edit}? (y/n): ")
#     if confirm_edit.lower() == "y":
#         # Get house list dataframe
#         priority_df = pd.read_csv(f'./data/priorities.csv')

#         # Edit house parameter value
#         priority_df.loc[priority_df[priority_col_head] == priority_to_edit, col_name] = new_val
#         priority_df.to_csv("./data/priorities.csv", index=False)
        
#         if col_num == "1":
#             print(f"\n✅ {new_val} house was successfully edited.\n")
#             view_house(new_val)
#         else:
#             print(f"\n✅ {priority_to_edit} house was successfully edited.\n")
#             view_priorities()
#     else: 
#         view_priorities()

# def _remove_priority():
#     print(f"\n:::::: VIEW HOUSE > REMOVE PRIORITY ::::::")
#     # Get house list dataframe
#     priority_df = pd.read_csv(f'./data/priorities.csv')
#     priority_col_head = priority_df.columns[0]

#     #prompt user for priority to remove
#     priority_list = priority_df.iloc[:, 0].tolist()
#     priority_to_remove = find_match(priority_list, "priority")

#     confirm_add = input(f"‼️ Are you sure you want to remove {priority_to_remove} from your priorities? (y/n): ")
#     if confirm_add.lower() == "y":
#         # Remove house row from dataframe
#         priority_df = priority_df[priority_df[priority_col_head] != priority_to_remove]
#         priority_df.to_csv("./data/priorities.csv", index=False)
#         print(f"✅ {priority_to_remove} was successfully removed from your priority list.\n")
#         return_to_main_menu()
#     else: 
#         view_house(priority_to_remove)
#     view_priorities()

def request_menu(menu_name):
    print("Choose one of the following actions:\n")
    
    # Request menu options
    menu_len = return_menu(menu_name)

    valid_input = False

    while not valid_input:
        # Prompt user for main menu selection
        selection = get_input(f"\nEnter your choice (1–{menu_len}): ")
        if int(selection) > menu_len or int(selection) < 0:
            invalid_input_alert(selection, menu_len)
        else:
            valid_input = True
            return selection


def get_input(prompt):
    user_input = input(prompt)
    if user_input == "!":
        return_to_main_menu()
    return user_input


def choose_column(dataframe):
    """
    Display CSV column names as a numbered list.
    Prompt user to select column number.
    Return column name and number.
    """
    # Get dictionary of column names (with number as key)
    columns_dict = return_columns(dataframe)

    # Print columns as menu options
    for num, col in columns_dict.items():
        print(f"{num}. {col}")

    # Get number of column names in columns dict
    num_columns = len(columns_dict)

    # Prompt user until valid input is entered
    valid_input = False
    while not valid_input:
        col_num_selected = input(f"\nEnter your choice (1–{num_columns}): ")
        
        # Check if sort param is valid
        if col_num_selected.isnumeric() and int(col_num_selected) <= num_columns:
            col_name_selected = columns_dict[int(col_num_selected)]
            valid_input = True
        else:
            invalid_input_alert(col_num_selected, num_columns)
    
    return (col_name_selected, col_num_selected)


def return_to_main_menu():
    print("⮐ Returning to main menu...")
    time.sleep(0.5)
    main_menu()


def invalid_input_alert(selection, num_options):
    print(f"⚠️ {selection} is not a valid option. Please enter a number between 1–{num_options}.\n")


def find_match(list_to_search, list_name):
    """
    Prompts the user for a value to find in a list.
    Returns the matching value found in the list.
    """
    match_found = False
    while not match_found:
        # Prompt user for house address to view
        input_value = get_input(f"Enter the {list_name} (or enter ! to cancel): ")
        best_match = process.extractOne(input_value, list_to_search)

        value_found = best_match[0]
        if best_match[1] > 50:
            confirm_match = input(f"Did you mean {value_found}? (y/n): ")
            if confirm_match.lower() == "y":
                match_found = True
                return value_found
            else:
                return_to_main_menu()
        elif best_match[1] < 0:
            print(f"{value_found} is not in your {list_name} list.")
            return_to_main_menu()

def get_all_total_scores():
    """
    Returns column with total priority score for all houses in the house list.
    """
    pass

def get_total_score(house_info_list):
    """
    Returns total priority score for the house at the given address.
    """
    # Get the number of priorities
    priority_list_df = pd.read_csv("./data/priorities.csv")
    num_of_priorities = len(priority_list_df)
    priority_value_list = house_info_list[-num_of_priorities:]
    
    with open("weighted-scores-calculator-main/weighted-scores-calculator.txt", "w") as calculator_pipe:
        calculator_pipe.write(f"{house_info_list[0]}")
        for i in range(num_of_priorities):
            priority_name = priority_list_df.iloc[i, 0]
            priority_weight = priority_list_df.iloc[i, 1]  # get priority weight
            score = priority_value_list[i]
            calculator_pipe.write(f"\n{priority_name},{priority_weight},{score}")
    calculator_pipe.close()
    time.sleep(5)

    with open("weighted-scores-calculator-main/weighted-scores-calculator.txt", "r") as calculator_pipe:
        total_score_data = calculator_pipe.read()
    calculator_pipe.close()
    total_score_list = ast.literal_eval(total_score_data)

    with open("weighted-scores-calculator-main/weighted-scores-calculator.txt", "w") as calculator_pipe:
        calculator_pipe.write('')
    calculator_pipe.close()
    return total_score_list[1][-1]
    

if __name__ == "__main__":
    display_intro()
    setup_priorities()
    main_menu()
from tabulate import tabulate
import time
import pandas as pd
import sys
import ast
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


def main_menu():
    # Prompt user to select menu item
    print(f"\n----------------------------[     MAIN MENU     ]"\
        "----------------------------\n")
    selection = request_menu("main_menu")
    _main_menu_execute(selection)

def _main_menu_execute(selection):
    # Display house list
    if selection == "1":
        view_house_list()
    
    # View a house from the house list
    elif selection == "2":
        view_house()

    # Add a house to the house list
    elif selection == "3":
        add_house()

    # Exit program
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
    
    selected_col_tuple = choose_column()
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
    columns_dict = return_columns()

    # Get number of column names in columns dict
    num_columns = len(columns_dict)

    new_house_list = []
    # Prompt user for house parameters
    print("Enter the following information about the house (or enter ! to cancel)...")
    for num, col in columns_dict.items():
        new_house_list.append(get_input(f"{num}. {col}: "))

    confirm_add = input(f"\n‼️ Are you sure you want to add this house your list (y/n)? ")
    if confirm_add.lower() == "y":
        house_list = pd.read_csv(f'./data/house_list.csv')
        house_list.loc[len(house_list)] = new_house_list
        house_list.to_csv("./data/house_list.csv", index=False)
        return_to_main_menu()
    else: 
        return_to_main_menu()


def view_house(house_address=None):
    print(f"\n---------------------------[     VIEW HOUSE     ]"\
          f"---------------------------\n")

    # Get house list dataframe
    house_list_df = pd.read_csv(f'./data/house_list.csv')
    house_address_list = house_list_df.iloc[:, 0].tolist()

    if house_address == None:
        match_found = False
        while not match_found:
            # Prompt user for house address to view
            view_address = get_input("Enter the address of a house to view details (or enter ! to cancel): ")
            best_match = process.extractOne(view_address, house_address_list)

            house_address = best_match[0]
            if best_match[1] > 50:
                confirm_match = input(f"Did you mean {house_address}? (y/n): ")
                if confirm_match.lower() == "y":
                    match_found = True
                else:
                    return_to_main_menu()
            elif best_match[1] < 0:
                print(f"{house_address} is not in your house list.")
                return_to_main_menu()
    
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
    columns_dict = return_columns()

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
    print(f"\n:::::: VIEW HOUSE > EDIT HOUSE ::::::\n")
    # Get house list dataframe
    house_list_df = pd.read_csv(f'./data/house_list.csv')
    selected_col_tuple = choose_column()
    col_name = selected_col_tuple[0]
    col_num = selected_col_tuple[1]
    address_col_head = house_list_df.columns[0]

    # Prompt the user for the new value
    new_val = input(f"Input the new {col_name} value: ")
    if new_val.isdigit():
        new_val = int(new_val)

    # Confirm that the user wants to make the edit
    confirm_edit = input(f"\n‼️ Are you sure you want to edit {house_address}? (y/n): ")
    if confirm_edit.lower() == "y":
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
    else: 
        view_house(house_address)

def _remove_house(house_address):
    print(f"\n:::::: VIEW HOUSE > REMOVE HOUSE ::::::\n")
    # Get house list dataframe
    house_list_df = pd.read_csv(f'./data/house_list.csv')
    address_col_head = house_list_df.columns[0]

    confirm_add = input(f"\n‼️ Are you sure you want to remove {house_address} from your list? (y/n): ")
    if confirm_add.lower() == "y":
        # Get house list dataframe
        house_list_df = pd.read_csv(f'./data/house_list.csv')

        # Remove house row from dataframe
        house_list_df = house_list_df[house_list_df[address_col_head] != house_address]
        house_list_df.to_csv("./data/house_list.csv", index=False)
        print(f"✅ {house_address} house was successfully removed from your house list.\n")
        return_to_main_menu()
    else: 
        view_house(house_address)
    
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


def choose_column():
    # Get dictionary of house list column names (with number as key)
    columns_dict = return_columns()

    # Print columns as mennu options
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

if __name__ == "__main__":
    display_intro()
    main_menu()
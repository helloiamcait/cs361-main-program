import time
import pandas as pd
import sys


def display_intro():
    # Display a message introducing the program
    with open('./text/intro_msg.txt', 'r') as intro_txt:
        intro_msg = intro_txt.read()
    intro_txt.close()
    print(intro_msg)


def main_menu():
    # Prompt user to select menu item
    with open('./text/main_menu.txt', 'r') as main_menu_txt:
        main_manu = main_menu_txt.read()
    main_menu_txt.close()
    print(main_manu)

    selection = get_selection()
    execute_selection(selection)


def get_selection():
    return input("\nEnter your choice (1–4): ")


def execute_selection(selection):
    # Display house list
    if selection == "1":
        house_list = pd.read_csv(f'./data/house_list.csv')

        # Check if house list is empty
        if len(house_list) == 0:
            print("\nYour house list is empty.")
        else:
            print(f'\n{house_list}')
        main_menu()
    
    # View a house from the house list
    elif selection == "2":
        print("\nView house")
        main_menu()

    # Add a house to the house list
    elif selection == "3":
        add_house()
        main_menu()

    # Exit program
    elif selection == "4":
        sys.exit()
    
    # Error message for invalid selection
    else:
        print(f"⚠️ {selection} is not a valid option. Please enter a number between 1–4.")
        # Promtp user to enter a valid selection number
        valid_selection = get_selection()
        execute_selection(valid_selection)

def add_house():
    # Display Add House header
    with open('./text/add_house.txt', 'r') as add_house_txt:
        add_house = add_house_txt.read()
    add_house_txt.close()
    print(add_house)

    # Prompt user for house parameters
    print("Enter the following information about the house (or enter ! to cancel)...")
    
    # For each column in the house_list.csv (except DOM), prompt user for info
    address = get_input("Address: ")
    list_price = get_input("List price (in whole dollars, e.g. 500000): ")
    bedrooms = get_input("Number of bedrooms: ")
    bathrooms = get_input("Number of bathrooms: ")
    dom = get_input("DOM: ")
    list_date = get_input("Listing date (MM/DD/YY): ")

    confirm_add = input("‼️ Are you sure you want to add this house your list (y/n)? ")
    if confirm_add.lower() == "y":
        house_list = pd.read_csv(f'./data/house_list.csv')
        house_list.loc[len(house_list)] = [address, list_price, bedrooms, bathrooms, dom, list_date]
        house_list.to_csv("./data/house_list.csv", index=False)
        return_to_main_menu()
    else: 
        return_to_main_menu()

def get_input(prompt):
    user_input = input(prompt)
    if user_input == "!":
        return_to_main_menu()
    return user_input


def return_to_main_menu():
    print("⮐ Returning to main menu...")
    main_menu()

if __name__ == "__main__":
    display_intro()
    main_menu()
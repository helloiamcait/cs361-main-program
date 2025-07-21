import time
import pandas as pd

def display_intro():
    # Display a message introducing the program
    with open('./text/intro_msg.txt', 'r') as intro_txt:
        intro_msg = intro_txt.read()
    intro_txt.close()
    print(intro_msg)

def main_menu():
    while True:
        # Prompt user to select menu item
        with open('./text/main_menu.txt', 'r') as main_menu_txt:
            main_manu = main_menu_txt.read()
        main_menu_txt.close()
        print(main_manu)
        selection = input("Enter your choice (1–4): ")

        # Display house list
        if selection == "1":
            house_list = pd.read_csv(f'./data/house_list.csv')

            # Check if house list is empty
            if len(house_list) == 0:
                print("\nYour house list is empty.")
            else:
                print(f'\n{house_list}')
        
        elif selection == "4":
            return


if __name__ == "__main__":
    display_intro()
    main_menu()
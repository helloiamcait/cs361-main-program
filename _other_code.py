def view_priorities():
    print(f"\n-------------------------[     VIEW PRIORITIES     ]"\
          "-------------------------\n")
    priority_df = pd.read_csv('./data/priorities.csv')

    # Check if priorities list is empty
    if len(priority_df) == 0:
        print("\nYou have not set any priorities.")
        print("Add a priority to get started.\n")
        _add_priority()
    else:
        print(tabulate(priority_df, headers = 'keys', tablefmt = 'fancy_outline', showindex=False))
    time.sleep(2)
    return_to_main_menu()

def _edit_priority():
    """
    Prompts the user for a priority name and weight for scoring each house.
    Adds the priority and weight to a CSV file.
    """
    print(f"\n:::::: VIEW HOUSE > EDIT PRIORITY ::::::")
    priority_df = pd.read_csv('./data/priorities.csv')
    
    # Prompt user for priority to change
    priority_list = priority_df.iloc[:, 0].tolist()
    priority_to_edit = find_match(priority_list, "priority")

    # Get the priority parameter the user wants to change
    selected_col_tuple = choose_column(priority_df)
    col_name = selected_col_tuple[0]
    col_num = selected_col_tuple[1]
    priority_col_head = priority_df.columns[0]

    # Prompt the user for the new value
    new_val = input(f"Input the new {col_name} value: ")
    if new_val.isdigit():
        new_val = int(new_val)

    # Confirm that the user wants to make the edit
    confirm_edit = input(f"\n‼️ Are you sure you want to edit {priority_to_edit}? (y/n): ")
    if confirm_edit.lower() == "y":
        # Get house list dataframe
        priority_df = pd.read_csv(f'./data/priorities.csv')

        # Edit house parameter value
        priority_df.loc[priority_df[priority_col_head] == priority_to_edit, col_name] = new_val
        priority_df.to_csv("./data/priorities.csv", index=False)
        
        if col_num == "1":
            print(f"\n✅ {new_val} house was successfully edited.\n")
            view_house(new_val)
        else:
            print(f"\n✅ {priority_to_edit} house was successfully edited.\n")
            view_priorities()
    else: 
        view_priorities()

def _remove_priority():
    print(f"\n:::::: VIEW HOUSE > REMOVE PRIORITY ::::::")
    # Get house list dataframe
    priority_df = pd.read_csv(f'./data/priorities.csv')
    priority_col_head = priority_df.columns[0]

    #prompt user for priority to remove
    priority_list = priority_df.iloc[:, 0].tolist()
    priority_to_remove = find_match(priority_list, "priority")

    confirm_add = input(f"‼️ Are you sure you want to remove {priority_to_remove} from your priorities? (y/n): ")
    if confirm_add.lower() == "y":
        # Remove house row from dataframe
        priority_df = priority_df[priority_df[priority_col_head] != priority_to_remove]
        priority_df.to_csv("./data/priorities.csv", index=False)
        print(f"✅ {priority_to_remove} was successfully removed from your priority list.\n")
        return_to_main_menu()
    else: 
        view_house(priority_to_remove)
    view_priorities()

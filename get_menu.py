def return_menu(menu_name):
    menu_dict = {
        "main_menu": ["View house list", "View house", "Add house", "Draft email with list", "Get highest scoring house", "Exit"],
        "view_house_list_menu": ["Sort list", "Return to main menu"],
        "view_house_menu": ["Edit house", "Remove house", "Return to main menu"],
    }

    menu_list = menu_dict[menu_name]
    for i, option in enumerate(menu_list):
        print(f"{i + 1}. {option}")
    
    return len(menu_list)